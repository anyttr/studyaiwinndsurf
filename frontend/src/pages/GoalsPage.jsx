import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Dialog,
  Tab,
  Tabs,
  CircularProgress,
  Alert,
  Snackbar
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import GoalForm from '../components/goals/GoalForm';
import GoalList from '../components/goals/GoalList';
import GoalSuggestions from '../components/goals/GoalSuggestions';

const GoalsPage = () => {
  const [goals, setGoals] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openForm, setOpenForm] = useState(false);
  const [selectedGoal, setSelectedGoal] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  useEffect(() => {
    fetchGoals();
    fetchSuggestions();
  }, []);

  const fetchGoals = async () => {
    try {
      const response = await fetch('/api/goals');
      if (!response.ok) throw new Error('Failed to fetch goals');
      const data = await response.json();
      setGoals(data.goals);
    } catch (err) {
      setError('Failed to load goals');
      showSnackbar('Failed to load goals', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchSuggestions = async () => {
    try {
      const response = await fetch('/api/goals/suggestions');
      if (!response.ok) throw new Error('Failed to fetch suggestions');
      const data = await response.json();
      setSuggestions(data.suggestions);
    } catch (err) {
      showSnackbar('Failed to load suggestions', 'error');
    }
  };

  const handleSubmit = async (formData) => {
    try {
      const url = selectedGoal ? `/api/goals/${selectedGoal.id}` : '/api/goals';
      const method = selectedGoal ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Failed to save goal');
      
      showSnackbar(
        selectedGoal ? 'Goal updated successfully' : 'Goal created successfully',
        'success'
      );
      
      setOpenForm(false);
      setSelectedGoal(null);
      fetchGoals();
    } catch (err) {
      showSnackbar('Failed to save goal', 'error');
    }
  };

  const handleEdit = (goal) => {
    setSelectedGoal(goal);
    setOpenForm(true);
  };

  const handleDelete = async (goalId) => {
    try {
      const response = await fetch(`/api/goals/${goalId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete goal');
      
      showSnackbar('Goal deleted successfully', 'success');
      fetchGoals();
    } catch (err) {
      showSnackbar('Failed to delete goal', 'error');
    }
  };

  const handleAcceptSuggestion = (suggestion) => {
    setSelectedGoal(null);
    setOpenForm(true);
    // Pre-fill the form with suggestion data
    handleSubmit(suggestion);
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
          Learning Goals
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setSelectedGoal(null);
            setOpenForm(true);
          }}
        >
          Create New Goal
        </Button>
      </Box>

      <Tabs
        value={activeTab}
        onChange={(e, newValue) => setActiveTab(newValue)}
        sx={{ mb: 4 }}
      >
        <Tab label="My Goals" />
        <Tab label="Suggestions" />
      </Tabs>

      {activeTab === 0 && (
        <GoalList
          goals={goals}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      )}

      {activeTab === 1 && (
        <GoalSuggestions
          suggestions={suggestions}
          onAccept={handleAcceptSuggestion}
        />
      )}

      <Dialog
        open={openForm}
        onClose={() => {
          setOpenForm(false);
          setSelectedGoal(null);
        }}
        maxWidth="md"
        fullWidth
      >
        <GoalForm
          onSubmit={handleSubmit}
          initialData={selectedGoal}
        />
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

export default GoalsPage;
