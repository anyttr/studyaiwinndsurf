import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  TextField,
  Chip,
  IconButton,
  Stack,
  Divider,
  Alert,
  Paper,
  Avatar
} from '@mui/material';
import {
  ArrowUpward as UpvoteIcon,
  ArrowDownward as DownvoteIcon,
  Check as CheckIcon
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import ReactMarkdown from 'react-markdown';
import { useAuth } from '../../contexts/AuthContext';

const VoteButtons = ({ score, onVote, contentType, contentId }) => {
  const { user } = useAuth();
  
  const handleVote = async (value) => {
    if (!user) {
      // Redirect to login or show login dialog
      return;
    }
    
    try {
      await onVote(value);
    } catch (err) {
      console.error('Failed to vote:', err);
    }
  };

  return (
    <Stack direction="column" alignItems="center" spacing={1}>
      <IconButton onClick={() => handleVote(1)} size="small">
        <UpvoteIcon />
      </IconButton>
      <Typography variant="h6">{score}</Typography>
      <IconButton onClick={() => handleVote(-1)} size="small">
        <DownvoteIcon />
      </IconButton>
    </Stack>
  );
};

const Comment = ({ comment }) => (
  <Box sx={{ pl: 2, borderLeft: '2px solid', borderColor: 'divider', my: 1 }}>
    <Typography variant="body2">
      {comment.content}
    </Typography>
    <Typography variant="caption" color="text.secondary">
      – {comment.user.name}, {formatDistanceToNow(new Date(comment.created_at))} ago
    </Typography>
  </Box>
);

const Answer = ({ answer, onVote, onAccept, isQuestionOwner }) => {
  const [showCommentInput, setShowCommentInput] = useState(false);
  const [commentContent, setCommentContent] = useState('');
  const { user } = useAuth();

  const handleAddComment = async () => {
    try {
      const response = await fetch(`/api/answers/${answer.id}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: commentContent })
      });

      if (!response.ok) throw new Error('Failed to add comment');

      // Refresh the page or update the state
      window.location.reload();
    } catch (err) {
      console.error('Failed to add comment:', err);
    }
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <VoteButtons
            score={answer.vote_score}
            onVote={(value) => onVote(answer.id, value)}
            contentType="answer"
            contentId={answer.id}
          />
          
          <Box sx={{ flexGrow: 1 }}>
            <Box sx={{ mb: 2 }}>
              <ReactMarkdown>{answer.content}</ReactMarkdown>
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="caption" color="text.secondary">
                Answered by {answer.user.name} •{' '}
                {formatDistanceToNow(new Date(answer.created_at))} ago
              </Typography>
              
              {isQuestionOwner && !answer.is_accepted && (
                <Button
                  startIcon={<CheckIcon />}
                  onClick={() => onAccept(answer.id)}
                  size="small"
                >
                  Accept Answer
                </Button>
              )}
              
              {answer.is_accepted && (
                <Chip
                  icon={<CheckIcon />}
                  label="Accepted Answer"
                  color="success"
                  size="small"
                />
              )}
            </Box>

            {answer.comments.length > 0 && (
              <Box sx={{ mb: 2 }}>
                {answer.comments.map(comment => (
                  <Comment key={comment.id} comment={comment} />
                ))}
              </Box>
            )}

            {user && (
              <Box>
                {showCommentInput ? (
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <TextField
                      size="small"
                      fullWidth
                      placeholder="Add a comment..."
                      value={commentContent}
                      onChange={(e) => setCommentContent(e.target.value)}
                    />
                    <Button
                      variant="contained"
                      size="small"
                      onClick={handleAddComment}
                    >
                      Add
                    </Button>
                    <Button
                      size="small"
                      onClick={() => setShowCommentInput(false)}
                    >
                      Cancel
                    </Button>
                  </Box>
                ) : (
                  <Button
                    size="small"
                    onClick={() => setShowCommentInput(true)}
                  >
                    Add a comment
                  </Button>
                )}
              </Box>
            )}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

const QuestionDetail = () => {
  const { id } = useParams();
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [answerContent, setAnswerContent] = useState('');
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchQuestion();
  }, [id]);

  const fetchQuestion = async () => {
    try {
      const response = await fetch(`/api/questions/${id}`);
      if (!response.ok) throw new Error('Failed to fetch question');

      const data = await response.json();
      setQuestion(data);
    } catch (err) {
      setError('Failed to load question');
    } finally {
      setLoading(false);
    }
  };

  const handleQuestionVote = async (value) => {
    try {
      const response = await fetch(`/api/questions/${id}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ value })
      });

      if (!response.ok) throw new Error('Failed to vote');

      const data = await response.json();
      setQuestion(prev => ({
        ...prev,
        vote_score: data.score
      }));
    } catch (err) {
      console.error('Failed to vote:', err);
    }
  };

  const handleAnswerVote = async (answerId, value) => {
    try {
      const response = await fetch(`/api/answers/${answerId}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ value })
      });

      if (!response.ok) throw new Error('Failed to vote');

      await fetchQuestion(); // Refresh the entire question to get updated scores
    } catch (err) {
      console.error('Failed to vote:', err);
    }
  };

  const handleAcceptAnswer = async (answerId) => {
    try {
      const response = await fetch(`/api/answers/${answerId}/accept`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) throw new Error('Failed to accept answer');

      await fetchQuestion(); // Refresh to show accepted status
    } catch (err) {
      console.error('Failed to accept answer:', err);
    }
  };

  const handleSubmitAnswer = async (e) => {
    e.preventDefault();
    
    if (!user) {
      navigate('/login');
      return;
    }

    try {
      const response = await fetch(`/api/questions/${id}/answers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: answerContent })
      });

      if (!response.ok) throw new Error('Failed to submit answer');

      setAnswerContent('');
      await fetchQuestion(); // Refresh to show new answer
    } catch (err) {
      console.error('Failed to submit answer:', err);
    }
  };

  if (loading) return <Typography>Loading...</Typography>;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!question) return <Typography>Question not found</Typography>;

  return (
    <Box sx={{ py: 4 }}>
      {/* Question */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <VoteButtons
            score={question.vote_score}
            onVote={handleQuestionVote}
            contentType="question"
            contentId={question.id}
          />
          
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h4" gutterBottom>
              {question.title}
            </Typography>

            <Box sx={{ mb: 2 }}>
              <Typography variant="caption" color="text.secondary">
                Asked by {question.user.name} •{' '}
                {formatDistanceToNow(new Date(question.created_at))} ago
              </Typography>
            </Box>

            <Box sx={{ mb: 2 }}>
              <ReactMarkdown>{question.content}</ReactMarkdown>
            </Box>

            <Box sx={{ mb: 2 }}>
              {question.tags.map((tag) => (
                <Chip
                  key={tag}
                  label={tag}
                  size="small"
                  sx={{ mr: 0.5 }}
                />
              ))}
            </Box>
          </Box>
        </Box>
      </Paper>

      {/* Answers */}
      <Typography variant="h5" gutterBottom>
        {question.answer_count} Answer{question.answer_count !== 1 && 's'}
      </Typography>

      <Box sx={{ mb: 4 }}>
        {question.answers.map(answer => (
          <Answer
            key={answer.id}
            answer={answer}
            onVote={handleAnswerVote}
            onAccept={handleAcceptAnswer}
            isQuestionOwner={user?.id === question.user.id}
          />
        ))}
      </Box>

      {/* Add Answer */}
      <Box>
        <Typography variant="h5" gutterBottom>
          Your Answer
        </Typography>

        {user ? (
          <form onSubmit={handleSubmitAnswer}>
            <TextField
              fullWidth
              multiline
              rows={6}
              placeholder="Write your answer here..."
              value={answerContent}
              onChange={(e) => setAnswerContent(e.target.value)}
              sx={{ mb: 2 }}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={!answerContent.trim()}
            >
              Post Your Answer
            </Button>
          </form>
        ) : (
          <Alert severity="info">
            Please <Button onClick={() => navigate('/login')}>log in</Button> to answer this question.
          </Alert>
        )}
      </Box>
    </Box>
  );
};

export default QuestionDetail;
