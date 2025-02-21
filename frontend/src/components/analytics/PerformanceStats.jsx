import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  CircularProgress,
  useTheme
} from '@mui/material';
import {
  School as SchoolIcon,
  Assignment as AssignmentIcon,
  Timer as TimerIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';

const StatCard = ({ icon: Icon, title, value, subvalue, color }) => {
  const theme = useTheme();

  return (
    <Paper sx={{ p: 3, height: '100%' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Icon sx={{ color: theme.palette[color].main, mr: 1 }} />
        <Typography variant="h6" color="text.secondary">
          {title}
        </Typography>
      </Box>
      
      <Box sx={{ position: 'relative', display: 'inline-flex' }}>
        <CircularProgress
          variant="determinate"
          value={value}
          size={80}
          thickness={8}
          sx={{ color: theme.palette[color].main }}
        />
        <Box
          sx={{
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography variant="h6" component="div" color="text.primary">
            {Math.round(value)}%
          </Typography>
        </Box>
      </Box>

      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
        {subvalue}
      </Typography>
    </Paper>
  );
};

const PerformanceStats = ({ stats }) => {
  const {
    flashcards,
    quizzes,
    sessions
  } = stats;

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          icon={SchoolIcon}
          title="Flashcards"
          value={flashcards.avg_performance}
          subvalue={`${flashcards.total_reviews} cards reviewed`}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          icon={AssignmentIcon}
          title="Quizzes"
          value={quizzes.avg_score}
          subvalue={`${quizzes.total_attempts} quizzes taken`}
          color="secondary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          icon={TimerIcon}
          title="Study Sessions"
          value={sessions.avg_performance}
          subvalue={`${sessions.total_sessions} sessions completed`}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          icon={TrendingUpIcon}
          title="Overall Progress"
          value={(flashcards.avg_performance + quizzes.avg_score + sessions.avg_performance) / 3}
          subvalue="Combined performance"
          color="info"
        />
      </Grid>
    </Grid>
  );
};

export default PerformanceStats;
