import { useState } from 'react';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface UseNotificationReturn {
  // 状态
  isOpen: boolean;
  message: string;
  type: NotificationType;
  
  // 操作方法
  showNotification: (message: string, type?: NotificationType) => void;
  showError: (message: string) => void;
  showSuccess: (message: string) => void;
  showWarning: (message: string) => void;
  showInfo: (message: string) => void;
  hideNotification: () => void;
}

export const useNotification = (): UseNotificationReturn => {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [type, setType] = useState<NotificationType>('info');

  const showNotification = (message: string, type: NotificationType = 'info') => {
    setMessage(message);
    setType(type);
    setIsOpen(true);
  };

  const showError = (message: string) => {
    showNotification(message, 'error');
  };

  const showSuccess = (message: string) => {
    showNotification(message, 'success');
  };

  const showWarning = (message: string) => {
    showNotification(message, 'warning');
  };

  const showInfo = (message: string) => {
    showNotification(message, 'info');
  };

  const hideNotification = () => {
    setIsOpen(false);
  };

  return {
    isOpen,
    message,
    type,
    showNotification,
    showError,
    showSuccess,
    showWarning,
    showInfo,
    hideNotification,
  };
}; 