import React from 'react';
import {
  Box,
  Alert,
  Fade,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';

interface StatusAlertsProps {
  error: string | null;
  success: boolean;
  onClearError: () => void;
}

export const StatusAlerts: React.FC<StatusAlertsProps> = ({ error, success, onClearError }) => {
  return (
    <Box sx={{ mt: 2 }}>
      {error && (
        <Fade in={true}>
          <Alert 
            severity="error" 
            onClose={onClearError}
            sx={{ mb: 2 }}
          >
            {error}
          </Alert>
        </Fade>
      )}

      {success && !error && (
        <Fade in={true}>
          <Alert 
            severity="success" 
            icon={<CheckCircleIcon />}
            sx={{ mb: 2 }}
          >
            图片加载成功！
          </Alert>
        </Fade>
      )}
    </Box>
  );
};
