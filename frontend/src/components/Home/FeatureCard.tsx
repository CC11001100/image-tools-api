import React from 'react';
import { 
  Card, 
  CardContent, 
  Box, 
  Button,
  Avatar,
  Typography,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { Feature } from '../../config/homeFeatures';

interface FeatureCardProps {
  feature: Feature;
}

export const FeatureCard: React.FC<FeatureCardProps> = ({ feature }) => {
  return (
    <Card 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        transition: 'transform 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 3,
        }
      }}
    >
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          height: 120,
          backgroundColor: `${feature.color}15`,
        }}
      >
        <Avatar
          sx={{
            bgcolor: feature.color,
            width: 60,
            height: 60,
          }}
        >
          {feature.icon}
        </Avatar>
      </Box>
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography gutterBottom variant="h6" component="h2">
          {feature.title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {feature.description}
        </Typography>
      </CardContent>
      <Box sx={{ p: 2, pt: 0 }}>
        <Button 
          component={RouterLink} 
          to={feature.link} 
          variant="contained" 
          color="primary" 
          fullWidth
          size="small"
          sx={{
            backgroundColor: feature.color,
            '&:hover': {
              backgroundColor: feature.color,
              filter: 'brightness(0.9)',
            }
          }}
        >
          试一试
        </Button>
      </Box>
    </Card>
  );
}; 