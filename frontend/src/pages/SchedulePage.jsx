import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Alert,
  Snackbar,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { addDays, startOfWeek, endOfWeek } from 'date-fns';

import ScheduleCalendar from '../components/schedule/ScheduleCalendar';
import SessionDialog from '../components/schedule/SessionDialog';

const SchedulePage = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSession, setSelectedSession] = useState(null);
  const [showGenerateDialog, setShowGenerateDialog] = useState(false);
  const [generatingSchedule, setGeneratingSchedule] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [dateRange, setDateRange] = useState({
    start: new Date(),
    end: addDays(new Date(), 7)
  });

  useEffect(() => {
    fetchSchedule();
  }, [currentDate]);

  const fetchSchedule = async () => {
    try {
      const start = startOfWeek(currentDate).toISOString();
      const end = endOfWeek(currentDate).toISOString();
      
      const response = await fetch(`/api/schedule?start_date=${start}&end_date=${end}`);
      if (!response.ok) throw new Error('Failed to fetch schedule');
      
      const data = await response.json();
      setSchedule(data.schedule);
    } catch (err) {
      setError('Failed to load schedule');
      showSnackbar('Failed to load schedule', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSchedule = async () => {
    try {
      setGeneratingSchedule(true);
      const response = await fetch('/api/schedule/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          start_date: dateRange.start.toISOString(),
          end_date: dateRange.end.toISOString()
        }),
      });

      if (!response.ok) throw new Error('Failed to generate schedule');
      
      const data = await response.json();
      showSnackbar('Schedule generated successfully', 'success');
      setShowGenerateDialog(false);
      fetchSchedule();
    } catch (err) {
      showSnackbar('Failed to generate schedule', 'error');
    } finally {
      setGeneratingSchedule(false);
    }
  };

  const handleCompleteSession = async (sessionId, data) => {
    try {
      const response = await fetch(`/api/schedule/sessions/${sessionId}/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Failed to complete session');
      
      showSnackbar('Session completed successfully', 'success');
      fetchSchedule();
    } catch (err) {
      showSnackbar('Failed to complete session', 'error');
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

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1">
          Study Schedule
        </Typography>
        <Button
          variant="contained"
          onClick={() => setShowGenerateDialog(true)}
        >
          Generate Schedule
        </Button>
      </Box>

      <Paper sx={{ p: 3 }}>
        <ScheduleCalendar
          currentDate={currentDate}
          sessions={schedule}
          onDateChange={setCurrentDate}
          onSessionClick={setSelectedSession}
        />
      </Paper>

      <SessionDialog
        session={selectedSession}
        open={Boolean(selectedSession)}
        onClose={() => setSelectedSession(null)}
        onComplete={handleCompleteSession}
      />

      <Dialog
        open={showGenerateDialog}
        onClose={() => setShowGenerateDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Generate Study Schedule</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <LocalizationProvider dateAdapter={AdapterDateFns}>
              <Box sx={{ mb: 3 }}>
                <DatePicker
                  label="Start Date"
                  value={dateRange.start}
                  onChange={(date) => setDateRange(prev => ({ ...prev, start: date }))}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </Box>
              <Box>
                <DatePicker
                  label="End Date"
                  value={dateRange.end}
                  onChange={(date) => setDateRange(prev => ({ ...prev, end: date }))}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                  minDate={dateRange.start}
                />
              </Box>
            </LocalizationProvider>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowGenerateDialog(false)}>
            Cancel
          </Button>
          <Button
            onClick={handleGenerateSchedule}
            variant="contained"
            disabled={generatingSchedule}
          >
            {generatingSchedule ? 'Generating...' : 'Generate'}
          </Button>
        </DialogActions>
      </Dialog>

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

export default SchedulePage;
