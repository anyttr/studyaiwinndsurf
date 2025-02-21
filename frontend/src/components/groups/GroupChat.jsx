import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  IconButton,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
  CircularProgress,
  Button
} from '@mui/material';
import {
  Send as SendIcon,
  AttachFile as AttachFileIcon,
  Reply as ReplyIcon
} from '@mui/icons-material';
import { format } from 'date-fns';

const GroupChat = ({ groupId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [replyTo, setReplyTo] = useState(null);
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchMessages();
    // Set up WebSocket connection here
  }, [groupId]);

  const fetchMessages = async () => {
    try {
      const response = await fetch(`/api/groups/${groupId}/messages`);
      if (!response.ok) throw new Error('Failed to fetch messages');
      
      const data = await response.json();
      setMessages(data);
    } catch (err) {
      console.error('Failed to load messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      const response = await fetch(`/api/groups/${groupId}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          content: newMessage,
          parent_id: replyTo?.id
        })
      });

      if (!response.ok) throw new Error('Failed to send message');

      const message = await response.json();
      setMessages([...messages, message]);
      setNewMessage('');
      setReplyTo(null);
    } catch (err) {
      console.error('Failed to send message:', err);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`/api/groups/${groupId}/messages/file`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('Failed to upload file');

      const message = await response.json();
      setMessages([...messages, message]);
    } catch (err) {
      console.error('Failed to upload file:', err);
    }
  };

  const MessageContent = ({ message }) => (
    <Box>
      {message.parent_id && (
        <Box
          sx={{
            pl: 2,
            borderLeft: '2px solid',
            borderColor: 'primary.main',
            mb: 1
          }}
        >
          <Typography variant="body2" color="text.secondary">
            Replying to{' '}
            {messages.find(m => m.id === message.parent_id)?.user.name}
          </Typography>
        </Box>
      )}
      
      {message.message_type === 'text' ? (
        <Typography variant="body1">{message.content}</Typography>
      ) : message.message_type === 'file' ? (
        <Button
          variant="outlined"
          startIcon={<AttachFileIcon />}
          href={message.content}
          target="_blank"
        >
          Download File
        </Button>
      ) : null}
    </Box>
  );

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper sx={{ height: '70vh', display: 'flex', flexDirection: 'column' }}>
      {/* Messages List */}
      <List sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
        {messages.map((message, index) => (
          <React.Fragment key={message.id}>
            <ListItem
              alignItems="flex-start"
              sx={{
                flexDirection: 'column',
                alignItems: 'flex-start'
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <ListItemAvatar>
                  <Avatar>{message.user.name[0]}</Avatar>
                </ListItemAvatar>
                <Box>
                  <Typography variant="subtitle2">
                    {message.user.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {format(new Date(message.created_at), 'MMM d, h:mm a')}
                  </Typography>
                </Box>
              </Box>
              
              <Box sx={{ pl: 7 }}>
                <MessageContent message={message} />
                
                <IconButton
                  size="small"
                  onClick={() => setReplyTo(message)}
                  sx={{ mt: 1 }}
                >
                  <ReplyIcon fontSize="small" />
                </IconButton>
              </Box>
            </ListItem>
            {index < messages.length - 1 && <Divider variant="inset" />}
          </React.Fragment>
        ))}
        <div ref={messagesEndRef} />
      </List>

      {/* Reply Preview */}
      {replyTo && (
        <Box
          sx={{
            p: 2,
            bgcolor: 'action.hover',
            display: 'flex',
            alignItems: 'center'
          }}
        >
          <Typography variant="body2" sx={{ flex: 1 }}>
            Replying to {replyTo.user.name}
          </Typography>
          <IconButton size="small" onClick={() => setReplyTo(null)}>
            <CloseIcon fontSize="small" />
          </IconButton>
        </Box>
      )}

      {/* Message Input */}
      <Box
        component="form"
        onSubmit={handleSendMessage}
        sx={{
          p: 2,
          bgcolor: 'background.default',
          display: 'flex',
          alignItems: 'center'
        }}
      >
        <IconButton
          component="label"
          sx={{ mr: 1 }}
        >
          <AttachFileIcon />
          <input
            type="file"
            hidden
            ref={fileInputRef}
            onChange={handleFileUpload}
          />
        </IconButton>

        <TextField
          fullWidth
          placeholder="Type a message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          variant="outlined"
          size="small"
          sx={{ mr: 1 }}
        />

        <IconButton
          type="submit"
          color="primary"
          disabled={!newMessage.trim()}
        >
          <SendIcon />
        </IconButton>
      </Box>
    </Paper>
  );
};

export default GroupChat;
