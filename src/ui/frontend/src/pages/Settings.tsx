import React, { useState, useEffect } from 'react'
import {
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Box,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Grid,
  Divider,
  CircularProgress,
} from '@mui/material'
import { Save as SaveIcon } from '@mui/icons-material'
import { settingsApi } from '../services/api'
import { Settings as SettingsType } from '../types'

export default function Settings() {
  const [settings, setSettings] = useState<SettingsType>({
    llm_provider: 'openai',
    llm_api_key: '',
    gmail_server: '',
    gmail_username: '',
    gmail_password: '',
    auto_check_email: false,
    check_interval: 60,
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    loadSettings()
  }, [])

  const loadSettings = async () => {
    try {
      setLoading(true)
      const data = await settingsApi.getSettings()
      setSettings(data)
    } catch (err) {
      console.error('Failed to load settings:', err)
      setMessage({ type: 'error', text: 'Failed to load settings' })
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      await settingsApi.updateSettings(settings)
      setMessage({ type: 'success', text: 'Settings saved successfully!' })
    } catch (err) {
      console.error('Failed to save settings:', err)
      setMessage({ type: 'error', text: 'Failed to save settings' })
    } finally {
      setSaving(false)
    }
  }

  const handleChange = (field: keyof SettingsType) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | any
  ) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value
    setSettings(prev => ({
      ...prev,
      [field]: value
    }))
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      {message && (
        <Alert severity={message.type} sx={{ mb: 3 }} onClose={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* LLM Configuration */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                AI Language Model Configuration
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth>
                    <InputLabel>LLM Provider</InputLabel>
                    <Select
                      value={settings.llm_provider}
                      label="LLM Provider"
                      onChange={handleChange('llm_provider')}
                    >
                      <MenuItem value="openai">OpenAI GPT-4</MenuItem>
                      <MenuItem value="anthropic">Anthropic Claude</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="API Key"
                    type="password"
                    value={settings.llm_api_key}
                    onChange={handleChange('llm_api_key')}
                    helperText="Your API key for the selected LLM provider"
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Email Configuration */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Email Configuration
              </Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                Configure email settings to automatically check for and process financial documents
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Gmail Server"
                    value={settings.gmail_server || ''}
                    onChange={handleChange('gmail_server')}
                    placeholder="imap.gmail.com"
                    helperText="IMAP server address"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Username"
                    value={settings.gmail_username || ''}
                    onChange={handleChange('gmail_username')}
                    placeholder="your-email@gmail.com"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Password/App Password"
                    type="password"
                    value={settings.gmail_password || ''}
                    onChange={handleChange('gmail_password')}
                    helperText="Use app password for Gmail"
                  />
                </Grid>
                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Check Interval (minutes)"
                    type="number"
                    value={settings.check_interval}
                    onChange={handleChange('check_interval')}
                    inputProps={{ min: 1, max: 1440 }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.auto_check_email}
                        onChange={handleChange('auto_check_email')}
                      />
                    }
                    label="Automatically check email for financial documents"
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Security Notice */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom color="warning.main">
                Security Notice
              </Typography>
              <Typography variant="body2" color="textSecondary">
                All API keys and passwords are encrypted and stored locally on your device. 
                This application does not send your credentials to any external servers except 
                for the configured LLM provider APIs for document analysis.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Save Button */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              startIcon={saving ? <CircularProgress size={20} /> : <SaveIcon />}
              onClick={handleSave}
              disabled={saving || !settings.llm_api_key}
              size="large"
            >
              {saving ? 'Saving...' : 'Save Settings'}
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  )
}