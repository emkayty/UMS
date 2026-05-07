"use client";

import React from "react";
import { clsx } from "clsx";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: "default" | "bordered" | "elevated";
}

export function Card({ children, className, variant = "default" }: CardProps) {
  const baseStyles = "rounded-lg p-4 transition-all";
  const variants = {
    default: "bg-white dark:bg-gray-800",
    bordered: "border border-gray-200 dark:border-gray-700",
    elevated: "shadow-lg dark:shadow-gray-900",
  };
  return <div className={clsx(baseStyles, variants[variant], className)}>{children}</div>;
}

export function CardHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={clsx("font-semibold text-lg mb-2", className)}>{children}</div>;
}

export function CardContent({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={clsx("text-gray-600 dark:text-gray-300", className)}>{children}</div>;
}

export function CardFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={clsx("mt-4 pt-2 border-t", className)}>{children}</div>;
}
