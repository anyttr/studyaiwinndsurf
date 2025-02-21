import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Chip,
  IconButton,
  InputAdornment,
  Pagination,
  Stack,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Skeleton
} from '@mui/material';
import {
  Search as SearchIcon,
  ArrowUpward as UpvoteIcon,
  ArrowDownward as DownvoteIcon,
  Visibility as ViewIcon,
  Comment as CommentIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';

const QuestionCard = ({ question }) => {
  const navigate = useNavigate();

  return (
    <Card 
      sx={{ 
        cursor: 'pointer',
        '&:hover': { boxShadow: 3 }
      }}
      onClick={() => navigate(`/questions/${question.id}`)}
    >
      <CardContent>
        <Grid container spacing={2}>
          {/* Stats */}
          <Grid item xs={2} sm={1}>
            <Stack spacing={1} alignItems="center">
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h6">{question.vote_score}</Typography>
                <Typography variant="caption">votes</Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h6">{question.answer_count}</Typography>
                <Typography variant="caption">answers</Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h6">{question.view_count}</Typography>
                <Typography variant="caption">views</Typography>
              </Box>
            </Stack>
          </Grid>

          {/* Content */}
          <Grid item xs={10} sm={11}>
            <Typography variant="h6" gutterBottom>
              {question.title}
            </Typography>

            <Typography
              variant="body2"
              color="text.secondary"
              sx={{
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden',
                mb: 2
              }}
            >
              {question.content}
            </Typography>

            <Box sx={{ mb: 2 }}>
              {question.tags.map((tag) => (
                <Chip
                  key={tag}
                  label={tag}
                  size="small"
                  sx={{ mr: 0.5, mb: 0.5 }}
                />
              ))}
            </Box>

            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <Typography variant="caption" color="text.secondary">
                Asked by {question.user.name} •{' '}
                {formatDistanceToNow(new Date(question.created_at))} ago
              </Typography>
              <Chip
                size="small"
                label={question.language === 'en' ? 'English' : 'Romanian'}
              />
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

const QuestionList = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [language, setLanguage] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [trendingTags, setTrendingTags] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchQuestions();
    fetchTrendingTags();
  }, [searchQuery, selectedTags, language, page]);

  const fetchQuestions = async () => {
    try {
      const params = new URLSearchParams({
        q: searchQuery,
        language,
        page,
        per_page: 10
      });

      selectedTags.forEach(tag => params.append('tags', tag));

      const response = await fetch(`/api/questions/search?${params}`);
      if (!response.ok) throw new Error('Failed to fetch questions');

      const data = await response.json();
      setQuestions(data.questions);
      setTotalPages(data.pages);
    } catch (err) {
      setError('Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  const fetchTrendingTags = async () => {
    try {
      const response = await fetch('/api/tags/trending');
      if (!response.ok) throw new Error('Failed to fetch trending tags');

      const data = await response.json();
      setTrendingTags(data);
    } catch (err) {
      console.error('Failed to load trending tags:', err);
    }
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    setPage(1);
  };

  const handleTagClick = (tag) => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter(t => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
    setPage(1);
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
    setPage(1);
  };

  return (
    <Box sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs>
            <Typography variant="h4" component="h1">
              Questions
            </Typography>
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              onClick={() => navigate('/questions/ask')}
            >
              Ask Question
            </Button>
          </Grid>
        </Grid>
      </Box>

      {/* Search and Filters */}
      <Grid container spacing={2} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            placeholder="Search questions..."
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
        <Grid item xs={12} md={3}>
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
      </Grid>

      {/* Trending Tags */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="subtitle1" gutterBottom>
          Trending Tags
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {trendingTags.map(([tag, count]) => (
            <Chip
              key={tag}
              label={`${tag} (${count})`}
              onClick={() => handleTagClick(tag)}
              color={selectedTags.includes(tag) ? 'primary' : 'default'}
            />
          ))}
        </Box>
      </Box>

      {/* Questions List */}
      <Stack spacing={2}>
        {loading ? (
          Array.from(new Array(5)).map((_, index) => (
            <Skeleton
              key={index}
              variant="rectangular"
              height={200}
              sx={{ borderRadius: 1 }}
            />
          ))
        ) : questions.length > 0 ? (
          questions.map(question => (
            <QuestionCard key={question.id} question={question} />
          ))
        ) : (
          <Typography variant="body1" color="text.secondary" align="center">
            No questions found
          </Typography>
        )}
      </Stack>

      {/* Pagination */}
      {totalPages > 1 && (
        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
          <Pagination
            count={totalPages}
            page={page}
            onChange={(e, value) => setPage(value)}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
};

export default QuestionList;
