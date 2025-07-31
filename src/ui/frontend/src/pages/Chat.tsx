import React, { useState, useEffect, useRef } from 'react'
import {
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Box,
  Alert,
  List,
  ListItem,
  Paper,
  Avatar,
  CircularProgress,
  Divider,
} from '@mui/material'
import {
  Send as SendIcon,
  Person as PersonIcon,
  SmartToy as BotIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material'
import { chatApi } from '../services/api'
import { ChatMessage } from '../types'

interface ChatBubbleProps {
  message: string
  isUser: boolean
  timestamp: string
}

function ChatBubble({ message, isUser, timestamp }: ChatBubbleProps) {
  return (
    <ListItem sx={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', px: 1 }}>
      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, maxWidth: '80%' }}>
        {!isUser && (
          <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
            <BotIcon fontSize="small" />
          </Avatar>
        )}
        <Paper
          sx={{
            p: 2,
            bgcolor: isUser ? 'primary.main' : 'grey.100',
            color: isUser ? 'white' : 'text.primary',
            borderRadius: 2,
          }}
        >
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
            {message}
          </Typography>
          <Typography
            variant="caption"
            sx={{
              display: 'block',
              mt: 0.5,
              opacity: 0.7,
              textAlign: isUser ? 'right' : 'left'
            }}
          >
            {new Date(timestamp).toLocaleTimeString()}
          </Typography>
        </Paper>
        {isUser && (
          <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
            <PersonIcon fontSize="small" />
          </Avatar>
        )}
      </Box>
    </ListItem>
  )
}

export default function Chat() {
  const [messages, setMessages] = useState<Array<{ message: string; response: string; timestamp: string }>>([])
  const [currentMessage, setCurrentMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadChatHistory()
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadChatHistory = async () => {
    try {
      const history = await chatApi.getChatHistory()
      setMessages(history.reverse()) // API returns newest first, we want oldest first
    } catch (err) {
      console.error('Failed to load chat history:', err)
      setError('Failed to load chat history')
    }
  }

  const handleSend = async () => {
    if (!currentMessage.trim() || loading) return

    const userMessage = currentMessage.trim()
    setCurrentMessage('')
    setLoading(true)
    setError(null)

    // Add user message immediately for better UX
    const timestamp = new Date().toISOString()
    const tempMessage = { message: userMessage, response: '', timestamp }
    setMessages(prev => [...prev, tempMessage])

    try {
      const response = await chatApi.sendMessage(userMessage)
      
      // Update the message with the response
      setMessages(prev => 
        prev.map(msg => 
          msg === tempMessage 
            ? { ...msg, response: response.response }
            : msg
        )
      )
    } catch (err) {
      console.error('Failed to send message:', err)
      setError('Failed to send message. Please check your API configuration.')
      
      // Remove the temporary message on error
      setMessages(prev => prev.filter(msg => msg !== tempMessage))
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSend()
    }
  }

  const handleClearHistory = () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      setMessages([])
    }
  }

  // Flatten messages for display
  const displayMessages = messages.flatMap(msg => [
    { content: msg.message, isUser: true, timestamp: msg.timestamp },
    ...(msg.response ? [{ content: msg.response, isUser: false, timestamp: msg.timestamp }] : [])
  ])

  return (
    <Box sx={{ height: 'calc(100vh - 120px)', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4">
          Financial Assistant
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={handleClearHistory}
          disabled={messages.length === 0}
        >
          Clear History
        </Button>
      </Box>
      
      <Typography variant="body1" color="textSecondary" paragraph>
        Ask questions about your finances. The assistant has access to your financial profile and can provide personalized advice.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Chat Messages */}
      <Card sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <CardContent sx={{ flexGrow: 1, overflow: 'auto', p: 1 }}>
          {displayMessages.length === 0 ? (
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              height: '100%',
              flexDirection: 'column',
              gap: 2
            }}>
              <BotIcon sx={{ fontSize: 64, color: 'text.secondary' }} />
              <Typography color="textSecondary" variant="h6">
                Welcome! Ask me anything about your finances.
              </Typography>
              <Typography color="textSecondary" variant="body2" sx={{ textAlign: 'center' }}>
                Try questions like:
                <br />• "What's my current net worth?"
                <br />• "How much did I spend on food last month?"
                <br />• "What are my biggest expenses?"
                <br />• "Should I invest more in stocks?"
              </Typography>
            </Box>
          ) : (
            <List sx={{ p: 0 }}>
              {displayMessages.map((msg, index) => (
                <ChatBubble
                  key={index}
                  message={msg.content}
                  isUser={msg.isUser}
                  timestamp={msg.timestamp}
                />
              ))}
              {loading && (
                <ListItem sx={{ display: 'flex', justifyContent: 'flex-start', px: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                    <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
                      <BotIcon fontSize="small" />
                    </Avatar>
                    <Paper sx={{ p: 2, bgcolor: 'grey.100', borderRadius: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <CircularProgress size={16} />
                        <Typography variant="body2" color="textSecondary">
                          Thinking...
                        </Typography>
                      </Box>
                    </Paper>
                  </Box>
                </ListItem>
              )}
            </List>
          )}
          <div ref={messagesEndRef} />
        </CardContent>
        
        <Divider />
        
        {/* Message Input */}
        <Box sx={{ p: 2 }}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              multiline
              maxRows={4}
              placeholder="Ask about your finances..."
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
              variant="outlined"
              size="small"
            />
            <Button
              variant="contained"
              onClick={handleSend}
              disabled={!currentMessage.trim() || loading}
              sx={{ minWidth: 'auto', px: 2 }}
            >
              {loading ? <CircularProgress size={20} /> : <SendIcon />}
            </Button>
          </Box>
          <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
            Press Enter to send, Shift+Enter for new line
          </Typography>
        </Box>
      </Card>
    </Box>
  )
}