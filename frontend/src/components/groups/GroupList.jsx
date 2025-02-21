import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Pagination,
  Chip,
  IconButton,
  InputAdornment
} from '@mui/material';
import {
  Search as SearchIcon,
  Group as GroupIcon,
  Language as LanguageIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const GroupList = () => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [language, setLanguage] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();

  useEffect(() => {
    fetchGroups();
  }, [searchQuery, language, page]);

  const fetchGroups = async () => {
    try {
      const params = new URLSearchParams({
        q: searchQuery,
        language,
        page,
        per_page: 12
      });

      const response = await fetch(`/api/groups/search?${params}`);
      if (!response.ok) throw new Error('Failed to fetch groups');

      const data = await response.json();
      setGroups(data.groups);
      setTotalPages(data.pages);
    } catch (err) {
      setError('Failed to load groups');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    setPage(1);
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
    setPage(1);
  };

  const handlePageChange = (e, value) => {
    setPage(value);
  };

  const handleJoinGroup = async (groupId, isPrivate) => {
    if (isPrivate) {
      navigate(`/groups/${groupId}/join`);
    } else {
      try {
        const response = await fetch(`/api/groups/${groupId}/join`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) throw new Error('Failed to join group');
        navigate(`/groups/${groupId}`);
      } catch (err) {
        setError('Failed to join group');
      }
    }
  };

  return (
    <Box sx={{ py: 4 }}>
      {/* Search and Filter Controls */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              placeholder="Search study groups..."
              value={searchQuery}
              onChange={handleSearch}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                )
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Language</InputLabel>
              <Select
                value={language}
                onChange={handleLanguageChange}
                label="Language"
              >
                <MenuItem value="">All Languages</MenuItem>
                <MenuItem value="en">English</MenuItem>
                <MenuItem value="ro">Romanian</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="contained"
              onClick={() => navigate('/groups/create')}
            >
              Create Group
            </Button>
          </Grid>
        </Grid>
      </Box>

      {/* Group Cards */}
      <Grid container spacing={3}>
        {groups.map((group) => (
          <Grid item xs={12} sm={6} md={4} key={group.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                '&:hover': {
                  boxShadow: 6
                }
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <GroupIcon sx={{ mr: 1 }} />
                  <Typography variant="h6" component="div">
                    {group.name}
                  </Typography>
                </Box>

                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{
                    mb: 2,
                    display: '-webkit-box',
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden'
                  }}
                >
                  {group.description}
                </Typography>

                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <LanguageIcon sx={{ fontSize: 'small', mr: 0.5 }} />
                  <Typography variant="body2" color="text.secondary">
                    {group.language === 'en' ? 'English' : 'Romanian'}
                  </Typography>
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Chip
                    size="small"
                    label={`${group.member_count} members`}
                    sx={{ mr: 1 }}
                  />
                  {group.is_private && (
                    <Chip
                      size="small"
                      label="Private"
                      color="secondary"
                    />
                  )}
                </Box>
              </CardContent>

              <Box sx={{ p: 2, pt: 0 }}>
                <Button
                  fullWidth
                  variant="contained"
                  onClick={() => handleJoinGroup(group.id, group.is_private)}
                >
                  {group.is_private ? 'Request to Join' : 'Join Group'}
                </Button>
              </Box>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Pagination */}
      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <Pagination
          count={totalPages}
          page={page}
          onChange={handlePageChange}
          color="primary"
        />
      </Box>
    </Box>
  );
};

export default GroupList;
