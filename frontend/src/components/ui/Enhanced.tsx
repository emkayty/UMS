import React, { useState, useEffect } from "react";

interface ToastProps {
  message: string;
  type?: "success" | "error" | "warning" | "info";
  duration?: number;
  onClose?: () => void;
}

export function Toast({ message, type = "info", duration = 3000, onClose }: ToastProps) {
  const [isVisible, setIsVisible] = useState(true);
  const [isLeaving, setIsLeaving] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLeaving(true);
      setTimeout(() => {
        setIsVisible(false);
        onClose?.();
      }, 300);
    }, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const types = {
    success: "bg-green-500",
    error: "bg-red-500",
    warning: "bg-yellow-500",
    info: "bg-blue-500",
  };

  if (!isVisible) return null;

  return (
    <div
      role="alert"
      aria-live="polite"
      className={`fixed bottom-4 right-4 ${types[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300 ${
        isLeaving ? "opacity-0 translate-y-4" : "opacity-100 translate-y-0"
      }`}
    >
      <p className="font-medium">{message}</p>
    </div>
  );
}

interface ToastManagerProps {
  toasts: ToastProps[];
  removeToast: (index: number) => void;
}

export function ToastManager({ toasts, removeToast }: ToastManagerProps) {
  return (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      {toasts.map((toast, index) => (
        <Toast key={index} {...toast} onClose={() => removeToast(index)} />
      ))}
    </div>
  );
}

// Notification Badge
interface NotificationBadgeProps {
  count: number;
  max?: number;
}

export function NotificationBadge({ count, max = 99 }: NotificationBadgeProps) {
  const displayCount = count > max ? `${max}+` : count;
  
  if (count <= 0) return null;
  
  return (
    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
      {displayCount}
    </span>
  );
}

// Progress Bar
interface ProgressProps {
  value: number;
  max?: number;
  color?: string;
  showLabel?: boolean;
}

export function Progress({ value, max = 100, color = "bg-blue-600", showLabel }: ProgressProps) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  
  return (
    <div className="w-full" role="progressbar" aria-valuenow={value} aria-valuemax={max}>
      {showLabel && (
        <div className="flex justify-between text-sm mb-1">
          <span>{value}</span>
          <span className="text-gray-500">{Math.round(percentage)}%</span>
        </div>
      )}
      <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
        <div
          className={`${color} h-full rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

// Tabs
interface Tab {
  id: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string;
  onChange: (tabId: string) => void;
}

export function Tabs({ tabs, activeTab, onChange }: TabsProps) {
  return (
    <div className="flex border-b border-gray-200" role="tablist">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          role="tab"
          aria-selected={activeTab === tab.id}
          aria-disabled={tab.disabled}
          disabled={tab.disabled}
          onClick={() => onChange(tab.id)}
          className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-colors ${
            activeTab === tab.id
              ? "border-blue-600 text-blue-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          } ${tab.disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
        >
          {tab.icon}
          {tab.label}
        </button>
      ))}
    </div>
  );
}

// Accordion
interface AccordionItem {
  id: string;
  title: string;
  content: React.ReactNode;
}

interface AccordionProps {
  items: AccordionItem[];
  allowMultiple?: boolean;
}

export function Accordion({ items, allowMultiple = false }: AccordionProps) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    const newOpen = new Set(openItems);
    if (newOpen.has(id)) {
      newOpen.delete(id);
    } else if (!allowMultiple) {
      newOpen.clear();
      newOpen.add(id);
    } else {
      newOpen.add(id);
    }
    setOpenItems(newOpen);
  };

  return (
    <div className="space-y-2">
      {items.map((item) => (
        <div key={item.id} className="border rounded-lg overflow-hidden">
          <button
            onClick={() => toggle(item.id)}
            aria-expanded={openItems.has(item.id)}
            className="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 transition-colors"
          >
            <span className="font-medium">{item.title}</span>
            <span className={`transform transition-transform ${openItems.has(item.id) ? "rotate-180" : ""}`}>
              ▼
            </span>
          </button>
          {openItems.has(item.id) && (
            <div className="p-4 border-t">{item.content}</div>
          )}
        </div>
      ))}
    </div>
  );
}
"