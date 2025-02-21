import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Snackbar,
  Tab,
  Tabs
} from '@mui/material';

import ProgressChart from '../components/analytics/ProgressChart';
import ActivityHeatmap from '../components/analytics/ActivityHeatmap';
import TopicProgress from '../components/analytics/TopicProgress';
import PerformanceStats from '../components/analytics/PerformanceStats';

const DashboardPage = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('/api/analytics/dashboard');
      if (!response.ok) throw new Error('Failed to fetch dashboard data');
      
      const data = await response.json();
      setDashboardData(data);
    } catch (err) {
      setError('Failed to load dashboard');
      showSnackbar('Failed to load dashboard data', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showSnackbar = (message, severity) => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!dashboardData) return null;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Learning Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Performance Statistics */}
        <Grid item xs={12}>
          <PerformanceStats stats={dashboardData.performance} />
        </Grid>

        {/* Progress Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <ProgressChart
              data={dashboardData.goals}
              title="Learning Progress"
            />
          </Paper>
        </Grid>

        {/* Activity Heatmap */}
        <Grid item xs={12}>
          <ActivityHeatmap data={dashboardData.activity} />
        </Grid>

        {/* Study Time Distribution */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Study Time Analysis
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1">
                  Total Study Time: {Math.round(dashboardData.study_time.total_time / 60)} hours
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Daily Average: {Math.round(dashboardData.study_time.average_daily_time)} minutes
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1">
                  Distribution by Activity Type:
                </Typography>
                {Object.entries(dashboardData.study_time.time_by_type).map(([type, time]) => (
                  <Typography key={type} variant="body2" color="text.secondary">
                    {type}: {Math.round(time / 60)} hours ({Math.round(time / dashboardData.study_time.total_time * 100)}%)
                  </Typography>
                ))}
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Topic Progress */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Tabs
              value={activeTab}
              onChange={(e, newValue) => setActiveTab(newValue)}
              sx={{ mb: 3 }}
            >
              <Tab label="All Topics" />
              <Tab label="Strengths & Weaknesses" />
            </Tabs>

            {activeTab === 0 ? (
              <Box sx={{ mt: 2 }}>
                <TopicProgress
                  topics={dashboardData.topics}
                  strengths={[]}
                  weaknesses={[]}
                />
              </Box>
            ) : (
              <Box sx={{ mt: 2 }}>
                <TopicProgress
                  topics={[]}
                  strengths={dashboardData.strengths_weaknesses.strengths}
                  weaknesses={dashboardData.strengths_weaknesses.weaknesses}
                />
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbar.severity}
          variant="filled"
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default DashboardPage;
