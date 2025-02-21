import React, { useState } from 'react';
import { Box, Button, FormControl, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

const GoalForm = ({ onSubmit, initialData = {} }) => {
  const [formData, setFormData] = useState({
    goal_type: initialData.goal_type || 'EXAM_PREP',
    title: initialData.title || '',
    description: initialData.description || '',
    target_date: initialData.target_date || new Date(),
    target_score: initialData.target_score || '',
    metadata: initialData.metadata || {}
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleDateChange = (date) => {
    setFormData(prev => ({
      ...prev,
      target_date: date
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
      <Typography variant="h5" gutterBottom>
        {initialData.id ? 'Edit Learning Goal' : 'Create New Learning Goal'}
      </Typography>

      <FormControl fullWidth margin="normal">
        <InputLabel>Goal Type</InputLabel>
        <Select
          name="goal_type"
          value={formData.goal_type}
          onChange={handleChange}
          required
        >
          <MenuItem value="EXAM_PREP">Exam Preparation</MenuItem>
          <MenuItem value="TOPIC_MASTERY">Topic Mastery</MenuItem>
          <MenuItem value="GENERAL_UNDERSTANDING">General Understanding</MenuItem>
        </Select>
      </FormControl>

      <TextField
        fullWidth
        margin="normal"
        name="title"
        label="Goal Title"
        value={formData.title}
        onChange={handleChange}
        required
      />

      <TextField
        fullWidth
        margin="normal"
        name="description"
        label="Description"
        multiline
        rows={4}
        value={formData.description}
        onChange={handleChange}
      />

      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <DateTimePicker
          label="Target Date"
          value={formData.target_date}
          onChange={handleDateChange}
          renderInput={(params) => (
            <TextField {...params} fullWidth margin="normal" required />
          )}
        />
      </LocalizationProvider>

      {formData.goal_type === 'EXAM_PREP' && (
        <TextField
          fullWidth
          margin="normal"
          name="target_score"
          label="Target Score"
          type="number"
          inputProps={{ min: 0, max: 100, step: 0.1 }}
          value={formData.target_score}
          onChange={handleChange}
        />
      )}

      <Box sx={{ mt: 3 }}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
        >
          {initialData.id ? 'Update Goal' : 'Create Goal'}
        </Button>
      </Box>
    </Box>
  );
};

export default GoalForm;
