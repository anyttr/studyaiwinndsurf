import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  IconButton,
  Grid,
  Chip,
  Menu,
  MenuItem
} from '@mui/material';
import {
  MoreVert as MoreVertIcon,
  School as SchoolIcon,
  Assignment as AssignmentIcon,
  Book as BookIcon
} from '@mui/icons-material';
import { format } from 'date-fns';

const GoalTypeIcon = ({ type }) => {
  switch (type) {
    case 'EXAM_PREP':
      return <SchoolIcon />;
    case 'TOPIC_MASTERY':
      return <AssignmentIcon />;
    case 'GENERAL_UNDERSTANDING':
      return <BookIcon />;
    default:
      return null;
  }
};

const GoalCard = ({ goal, onEdit, onDelete }) => {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleEdit = () => {
    handleMenuClose();
    onEdit(goal);
  };

  const handleDelete = () => {
    handleMenuClose();
    onDelete(goal.id);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'primary';
      case 'completed':
        return 'success';
      case 'abandoned':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <GoalTypeIcon type={goal.goal_type} />
            <Typography variant="h6" component="div">
              {goal.title}
            </Typography>
          </Box>
          <IconButton onClick={handleMenuOpen}>
            <MoreVertIcon />
          </IconButton>
        </Box>

        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {goal.description}
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Progress
          </Typography>
          <LinearProgress
            variant="determinate"
            value={goal.progress}
            sx={{ height: 8, borderRadius: 4 }}
          />
          <Typography variant="body2" color="text.secondary" align="right">
            {Math.round(goal.progress)}%
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Chip
            label={goal.status}
            color={getStatusColor(goal.status)}
            size="small"
          />
          <Typography variant="caption" color="text.secondary">
            Due: {format(new Date(goal.target_date), 'MMM d, yyyy')}
          </Typography>
        </Box>
      </CardContent>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleEdit}>Edit</MenuItem>
        <MenuItem onClick={handleDelete}>Delete</MenuItem>
      </Menu>
    </Card>
  );
};

const GoalList = ({ goals, onEdit, onDelete }) => {
  return (
    <Grid container spacing={3}>
      {goals.map((goal) => (
        <Grid item xs={12} sm={6} md={4} key={goal.id}>
          <GoalCard
            goal={goal}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        </Grid>
      ))}
    </Grid>
  );
};

export default GoalList;
