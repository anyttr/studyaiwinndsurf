import React from 'react';
import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
  Divider,
  Grid
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon
} from '@mui/icons-material';
import { format, parseISO } from 'date-fns';

const ProgressItem = ({ topic, confidence, lastReviewed, reviewCount }) => (
  <ListItem>
    <ListItemText
      primary={
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Typography variant="subtitle2">
            {topic}
          </Typography>
          <Chip
            size="small"
            label={`${Math.round(confidence)}%`}
            color={confidence >= 70 ? 'success' : confidence >= 40 ? 'warning' : 'error'}
            sx={{ ml: 1 }}
          />
        </Box>
      }
      secondary={
        <Box sx={{ mt: 1 }}>
          <LinearProgress
            variant="determinate"
            value={confidence}
            sx={{
              height: 8,
              borderRadius: 4,
              mb: 1
            }}
          />
          <Typography variant="caption" color="text.secondary">
            Last reviewed: {lastReviewed ? format(parseISO(lastReviewed), 'MMM d, yyyy') : 'Never'} 
            • Reviews: {reviewCount}
          </Typography>
        </Box>
      }
    />
  </ListItem>
);

const TopicProgress = ({ topics, strengths, weaknesses }) => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Topic Progress Overview
          </Typography>
          <List>
            {topics.map((topic, index) => (
              <React.Fragment key={index}>
                <ProgressItem {...topic} />
                {index < topics.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 3, height: '100%' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <TrendingUpIcon color="success" sx={{ mr: 1 }} />
            <Typography variant="h6">
              Strengths
            </Typography>
          </Box>
          <List>
            {strengths.map((topic, index) => (
              <React.Fragment key={index}>
                <ListItem>
                  <ListItemText
                    primary={topic.topic}
                    secondary={
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="body2" color="success.main">
                          Confidence: {Math.round(topic.confidence)}%
                        </Typography>
                        {topic.mastered_date && (
                          <Typography variant="caption" color="text.secondary">
                            Mastered on: {format(parseISO(topic.mastered_date), 'MMM d, yyyy')}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                </ListItem>
                {index < strengths.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      </Grid>

      <Grid item xs={12} md={6}>
        <Paper sx={{ p: 3, height: '100%' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <TrendingDownIcon color="error" sx={{ mr: 1 }} />
            <Typography variant="h6">
              Areas for Improvement
            </Typography>
          </Box>
          <List>
            {weaknesses.map((topic, index) => (
              <React.Fragment key={index}>
                <ListItem>
                  <ListItemText
                    primary={topic.topic}
                    secondary={
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="body2" color="error.main">
                          Confidence: {Math.round(topic.confidence)}%
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Reviews needed: {topic.review_count}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
                {index < weaknesses.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default TopicProgress;
