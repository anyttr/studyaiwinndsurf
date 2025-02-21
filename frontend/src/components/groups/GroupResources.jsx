import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Tooltip,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Description as DescriptionIcon,
  Link as LinkIcon,
  School as SchoolIcon,
  VideoLibrary as VideoIcon,
  Delete as DeleteIcon,
  Edit as EditIcon
} from '@mui/icons-material';
import { format } from 'date-fns';

const ResourceTypeIcons = {
  flashcard_deck: SchoolIcon,
  note: DescriptionIcon,
  link: LinkIcon,
  video: VideoIcon
};

const ResourceDialog = ({ open, onClose, onSubmit, initialData = {} }) => {
  const [formData, setFormData] = useState({
    title: '',
    resource_type: 'note',
    content: '',
    url: '',
    ...initialData
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit}>
        <DialogTitle>
          {initialData.id ? 'Edit Resource' : 'Add Resource'}
        </DialogTitle>
        
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            margin="normal"
          />

          <FormControl fullWidth margin="normal">
            <InputLabel>Resource Type</InputLabel>
            <Select
              name="resource_type"
              value={formData.resource_type}
              onChange={handleChange}
              label="Resource Type"
            >
              <MenuItem value="note">Note</MenuItem>
              <MenuItem value="flashcard_deck">Flashcard Deck</MenuItem>
              <MenuItem value="link">Link</MenuItem>
              <MenuItem value="video">Video</MenuItem>
            </Select>
          </FormControl>

          {formData.resource_type === 'link' || formData.resource_type === 'video' ? (
            <TextField
              fullWidth
              label="URL"
              name="url"
              value={formData.url}
              onChange={handleChange}
              required
              margin="normal"
            />
          ) : (
            <TextField
              fullWidth
              label="Content"
              name="content"
              value={formData.content}
              onChange={handleChange}
              required
              margin="normal"
              multiline
              rows={4}
            />
          )}
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained">
            {initialData.id ? 'Save Changes' : 'Add Resource'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

const GroupResources = ({ groupId }) => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingResource, setEditingResource] = useState(null);

  useEffect(() => {
    fetchResources();
  }, [groupId]);

  const fetchResources = async () => {
    try {
      const response = await fetch(`/api/groups/${groupId}/resources`);
      if (!response.ok) throw new Error('Failed to fetch resources');
      
      const data = await response.json();
      setResources(data);
    } catch (err) {
      console.error('Failed to load resources:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddResource = async (formData) => {
    try {
      const response = await fetch(`/api/groups/${groupId}/resources`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('Failed to add resource');

      const newResource = await response.json();
      setResources([...resources, newResource]);
      setDialogOpen(false);
    } catch (err) {
      console.error('Failed to add resource:', err);
    }
  };

  const handleEditResource = async (formData) => {
    try {
      const response = await fetch(`/api/groups/${groupId}/resources/${editingResource.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('Failed to update resource');

      const updatedResource = await response.json();
      setResources(resources.map(r => 
        r.id === updatedResource.id ? updatedResource : r
      ));
      setDialogOpen(false);
      setEditingResource(null);
    } catch (err) {
      console.error('Failed to update resource:', err);
    }
  };

  const handleDeleteResource = async (resourceId) => {
    if (!window.confirm('Are you sure you want to delete this resource?')) return;

    try {
      const response = await fetch(`/api/groups/${groupId}/resources/${resourceId}`, {
        method: 'DELETE'
      });

      if (!response.ok) throw new Error('Failed to delete resource');

      setResources(resources.filter(r => r.id !== resourceId));
    } catch (err) {
      console.error('Failed to delete resource:', err);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6">
          Study Resources
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditingResource(null);
            setDialogOpen(true);
          }}
        >
          Add Resource
        </Button>
      </Box>

      <Grid container spacing={3}>
        {resources.map((resource) => {
          const Icon = ResourceTypeIcons[resource.resource_type] || DescriptionIcon;

          return (
            <Grid item xs={12} sm={6} md={4} key={resource.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Icon sx={{ mr: 1 }} />
                    <Typography variant="h6" component="div" sx={{ flex: 1 }}>
                      {resource.title}
                    </Typography>
                    <Box>
                      <Tooltip title="Edit">
                        <IconButton
                          size="small"
                          onClick={() => {
                            setEditingResource(resource);
                            setDialogOpen(true);
                          }}
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete">
                        <IconButton
                          size="small"
                          onClick={() => handleDeleteResource(resource.id)}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    <Chip
                      size="small"
                      label={resource.resource_type.replace('_', ' ')}
                      sx={{ mr: 1 }}
                    />
                    <Typography variant="caption" color="text.secondary">
                      Added by {resource.created_by.name} on{' '}
                      {format(new Date(resource.created_at), 'MMM d, yyyy')}
                    </Typography>
                  </Box>

                  {resource.resource_type === 'link' || resource.resource_type === 'video' ? (
                    <Button
                      variant="outlined"
                      startIcon={<LinkIcon />}
                      href={resource.url}
                      target="_blank"
                      fullWidth
                    >
                      Open Resource
                    </Button>
                  ) : (
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{
                        display: '-webkit-box',
                        WebkitLineClamp: 3,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden'
                      }}
                    >
                      {resource.content}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <ResourceDialog
        open={dialogOpen}
        onClose={() => {
          setDialogOpen(false);
          setEditingResource(null);
        }}
        onSubmit={editingResource ? handleEditResource : handleAddResource}
        initialData={editingResource}
      />
    </Box>
  );
};

export default GroupResources;
