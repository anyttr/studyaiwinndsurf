import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Slider,
  TextField,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider
} from '@mui/material';
import {
  School as SchoolIcon,
  Assignment as AssignmentIcon,
  Book as BookIcon,
  PlayCircle as PlayCircleIcon,
  Timer as TimerIcon,
  Star as StarIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import { format } from 'date-fns';

const SessionTypeIcon = ({ type }) => {
  switch (type) {
    case 'flashcards':
      return <SchoolIcon />;
    case 'quiz':
      return <AssignmentIcon />;
    case 'microlearning':
      return <PlayCircleIcon />;
    case 'reading':
      return <BookIcon />;
    default:
      return null;
  }
};

const SessionDialog = ({ session, open, onClose, onComplete }) => {
  const [performanceScore, setPerformanceScore] = useState(session?.performance_score || 0);
  const [notes, setNotes] = useState(session?.notes || '');

  const handleComplete = () => {
    onComplete(session.id, {
      performance_score: performanceScore,
      notes: notes
    });
    onClose();
  };

  if (!session) return null;

  const getSessionColor = (type) => {
    switch (type) {
      case 'flashcards':
        return 'primary';
      case 'quiz':
        return 'secondary';
      case 'microlearning':
        return 'success';
      case 'reading':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <SessionTypeIcon type={session.session_type} />
          <Typography variant="h6">
            Study Session
          </Typography>
        </Box>
      </DialogTitle>
      <DialogContent>
        <List>
          <ListItem>
            <ListItemIcon>
              <TimerIcon />
            </ListItemIcon>
            <ListItemText
              primary="Time"
              secondary={`${format(new Date(session.start_time), 'HH:mm')} - ${format(new Date(session.end_time), 'HH:mm')}`}
            />
          </ListItem>

          <Divider component="li" />

          <ListItem>
            <ListItemText
              primary="Goal"
              secondary={session.goal_title}
            />
          </ListItem>

          <Divider component="li" />

          <ListItem>
            <ListItemText
              primary="Session Type"
              secondary={
                <Chip
                  icon={<SessionTypeIcon type={session.session_type} />}
                  label={session.session_type}
                  color={getSessionColor(session.session_type)}
                  size="small"
                  sx={{ mt: 1 }}
                />
              }
            />
          </ListItem>

          <Divider component="li" />

          <ListItem>
            <ListItemIcon>
              <StarIcon />
            </ListItemIcon>
            <ListItemText
              primary="Performance Score"
              secondary={
                <Box sx={{ mt: 2 }}>
                  <Slider
                    value={performanceScore}
                    onChange={(_, value) => setPerformanceScore(value)}
                    valueLabelDisplay="auto"
                    step={5}
                    marks
                    min={0}
                    max={100}
                    disabled={session.completed}
                  />
                </Box>
              }
            />
          </ListItem>

          <Divider component="li" />

          <ListItem>
            <ListItemText
              primary="Notes"
              secondary={
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Add your study notes here..."
                  disabled={session.completed}
                  sx={{ mt: 1 }}
                />
              }
            />
          </ListItem>

          {session.completed && (
            <>
              <Divider component="li" />
              <ListItem>
                <ListItemIcon>
                  <CheckCircleIcon color="success" />
                </ListItemIcon>
                <ListItemText
                  primary="Status"
                  secondary="Completed"
                />
              </ListItem>
            </>
          )}
        </List>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>
          Close
        </Button>
        {!session.completed && (
          <Button
            onClick={handleComplete}
            variant="contained"
            color="primary"
            startIcon={<CheckCircleIcon />}
          >
            Complete Session
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default SessionDialog;
