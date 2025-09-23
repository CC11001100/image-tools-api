import React from 'react';
import { Snackbar, Alert } from '@mui/material';
import { NotificationType } from '../hooks/useNotification';

interface NotificationProviderProps {
  children: React.ReactNode;
  notification?: {
    isOpen: boolean;
    message: string;
    type: NotificationType;
    onClose: () => void;
  };
}

export const NotificationProvider: React.FC<NotificationProviderProps> = ({
  children,
  notification,
}) => {
  const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    notification?.onClose();
  };

  return (
    <>
      {children}
      
      {/* 通知 Snackbar */}
      {notification && (
        <Snackbar
          open={notification.isOpen}
          autoHideDuration={6000}
          onClose={handleClose}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
          <Alert 
            onClose={handleClose} 
            severity={notification.type} 
            sx={{ 
              width: '100%',
              maxWidth: '500px',
              boxShadow: 3,
              '& .MuiAlert-message': {
                fontSize: '0.95rem',
                lineHeight: 1.4
              },
              '& .MuiAlert-icon': {
                fontSize: '1.25rem'
              }
            }}
          >
            {notification.message}
          </Alert>
        </Snackbar>
      )}
    </>
  );
}; 