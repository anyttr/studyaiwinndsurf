import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Stack,
  Divider
} from '@mui/material';
import { Lightbulb as LightbulbIcon } from '@mui/icons-material';
import { format, addDays } from 'date-fns';

const GoalSuggestionCard = ({ suggestion, onAccept }) => {
  const handleAccept = () => {
    onAccept({
      ...suggestion,
      target_date: new Date(suggestion.target_date)
    });
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <LightbulbIcon color="warning" />
          <Typography variant="h6" component="div">
            {suggestion.title}
          </Typography>
        </Box>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {suggestion.description}
        </Typography>

        {suggestion.metadata?.topics && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Related Topics:
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap">
              {suggestion.metadata.topics.map((topic, index) => (
                <Chip
                  key={index}
                  label={topic}
                  size="small"
                  sx={{ mb: 1 }}
                />
              ))}
            </Stack>
          </Box>
        )}

        <Divider sx={{ my: 2 }} />

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            Suggested completion: {format(new Date(suggestion.target_date), 'MMM d, yyyy')}
          </Typography>
          <Button
            variant="contained"
            color="primary"
            size="small"
            onClick={handleAccept}
          >
            Accept Suggestion
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

const GoalSuggestions = ({ suggestions, onAccept }) => {
  if (!suggestions?.length) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <LightbulbIcon color="disabled" sx={{ fontSize: 48, mb: 2 }} />
        <Typography variant="h6" color="text.secondary">
          No goal suggestions available
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Keep learning and we'll suggest personalized goals based on your progress!
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
        Suggested Learning Goals
      </Typography>
      {suggestions.map((suggestion, index) => (
        <GoalSuggestionCard
          key={index}
          suggestion={suggestion}
          onAccept={onAccept}
        />
      ))}
    </Box>
  );
};

export default GoalSuggestions;
