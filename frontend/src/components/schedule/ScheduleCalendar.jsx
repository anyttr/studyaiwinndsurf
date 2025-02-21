import React from 'react';
import {
  Box,
  Paper,
  Typography,
  IconButton,
  Tooltip,
  Chip,
  Grid
} from '@mui/material';
import {
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  School as SchoolIcon,
  Assignment as AssignmentIcon,
  Book as BookIcon,
  PlayCircle as PlayCircleIcon
} from '@mui/icons-material';
import { format, addDays, startOfWeek, addWeeks, isSameDay } from 'date-fns';

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

const TimeSlot = ({ session, onClick }) => {
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
    <Paper
      sx={{
        p: 1,
        mb: 1,
        cursor: 'pointer',
        bgcolor: session.completed ? 'action.selected' : 'background.paper',
        '&:hover': {
          bgcolor: 'action.hover',
        },
      }}
      onClick={() => onClick(session)}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
        <SessionTypeIcon type={session.session_type} />
        <Typography variant="subtitle2" sx={{ ml: 1 }}>
          {format(new Date(session.start_time), 'HH:mm')} - {format(new Date(session.end_time), 'HH:mm')}
        </Typography>
      </Box>
      <Typography variant="body2" noWrap>
        {session.goal_title}
      </Typography>
      <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
        <Chip
          size="small"
          label={session.session_type}
          color={getSessionColor(session.session_type)}
        />
        {session.completed && (
          <Chip
            size="small"
            label={`${session.performance_score}%`}
            color="success"
          />
        )}
      </Box>
    </Paper>
  );
};

const DayColumn = ({ date, sessions, onSessionClick }) => {
  const daysSessions = sessions.filter(session =>
    isSameDay(new Date(session.start_time), date)
  );

  return (
    <Box sx={{ flex: 1, minWidth: 0 }}>
      <Paper
        sx={{
          p: 1,
          mb: 2,
          textAlign: 'center',
          bgcolor: 'primary.main',
          color: 'primary.contrastText',
        }}
      >
        <Typography variant="subtitle2">
          {format(date, 'EEE')}
        </Typography>
        <Typography variant="h6">
          {format(date, 'd')}
        </Typography>
      </Paper>
      {daysSessions.map(session => (
        <TimeSlot
          key={session.id}
          session={session}
          onClick={onSessionClick}
        />
      ))}
    </Box>
  );
};

const ScheduleCalendar = ({
  currentDate,
  sessions,
  onDateChange,
  onSessionClick
}) => {
  const startDate = startOfWeek(currentDate);
  const days = Array.from({ length: 7 }, (_, i) => addDays(startDate, i));

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        mb: 3
      }}>
        <IconButton onClick={() => onDateChange(addWeeks(currentDate, -1))}>
          <ChevronLeftIcon />
        </IconButton>
        <Typography variant="h5">
          {format(currentDate, 'MMMM yyyy')}
        </Typography>
        <IconButton onClick={() => onDateChange(addWeeks(currentDate, 1))}>
          <ChevronRightIcon />
        </IconButton>
      </Box>

      <Box sx={{
        display: 'flex',
        gap: 2,
        overflowX: 'auto',
        pb: 2
      }}>
        {days.map(date => (
          <DayColumn
            key={date.toString()}
            date={date}
            sessions={sessions}
            onSessionClick={onSessionClick}
          />
        ))}
      </Box>

      <Grid container spacing={2} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6}>
          <Typography variant="subtitle2" gutterBottom>
            Session Types:
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip
              icon={<SchoolIcon />}
              label="Flashcards"
              color="primary"
              size="small"
            />
            <Chip
              icon={<AssignmentIcon />}
              label="Quiz"
              color="secondary"
              size="small"
            />
            <Chip
              icon={<PlayCircleIcon />}
              label="Microlearning"
              color="success"
              size="small"
            />
            <Chip
              icon={<BookIcon />}
              label="Reading"
              color="info"
              size="small"
            />
          </Box>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography variant="subtitle2" gutterBottom>
            Statistics:
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Completed: {sessions.filter(s => s.completed).length}/{sessions.length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Avg. Performance: {
                Math.round(
                  sessions
                    .filter(s => s.completed && s.performance_score)
                    .reduce((acc, s) => acc + s.performance_score, 0) /
                  sessions.filter(s => s.completed && s.performance_score).length
                ) || 0
              }%
            </Typography>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ScheduleCalendar;
