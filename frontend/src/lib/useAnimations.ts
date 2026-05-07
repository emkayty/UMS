/**
 * UMS Frontend - Animation Hooks
 * Custom hooks for animations
 */

'use client';

import { useState, useEffect, useRef } from 'react';

// Count up animation
export function useCountUp(end: number, duration: number = 2000) {
  const [count, setCount] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);
  
  useEffect(() => {
    let start = 0;
    const increment = end / (duration / 16);
    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setCount(end);
        clearInterval(timer);
        setIsAnimating(false);
      } else {
        setCount(Math.floor(start));
      }
    }, 16);
    
    return () => clearInterval(timer);
  }, [end, duration]);
  
  return { count, isAnimating };
}

// Fade in animation
export function useFadeIn(delay: number = 0) {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);
  
  return { 
    isVisible,
    className: isVisible ? 'animate-fade-in' : 'opacity-0'
  };
}

// Stagger animation
export function useStagger(delay: number = 100) {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), delay);
    return () => clearTimeout(timer);
  }, [delay]);
  
  return { 
    isVisible,
    className: isVisible ? 'animate-fade-in' : 'opacity-0'
  };
}

// Default exports
export default { useCountUp, useFadeIn, useStagger };