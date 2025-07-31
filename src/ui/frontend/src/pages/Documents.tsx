import React, { useState, useEffect, useCallback } from 'react'
import {
  Typography,
  Card,
  CardContent,
  Button,
  Box,
  Alert,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Paper,
} from '@mui/material'
import {
  CloudUpload as UploadIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Description as DocIcon,
} from '@mui/icons-material'
import { useDropzone } from 'react-dropzone'
import { documentsApi } from '../services/api'
import { Document } from '../types'

export default function Documents() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null)
  const [viewDialogOpen, setViewDialogOpen] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    loadDocuments()
  }, [])

  const loadDocuments = async () => {
    try {
      setLoading(true)
      const data = await documentsApi.getDocuments()
      setDocuments(data)
    } catch (err) {
      console.error('Failed to load documents:', err)
      setMessage({ type: 'error', text: 'Failed to load documents' })
    } finally {
      setLoading(false)
    }
  }

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (!file) return

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setMessage({ type: 'error', text: 'Only PDF files are supported' })
      return
    }

    try {
      setUploading(true)
      await documentsApi.uploadDocument(file, 'financial')
      setMessage({ type: 'success', text: 'Document uploaded and analyzed successfully!' })
      await loadDocuments()
    } catch (err) {
      console.error('Failed to upload document:', err)
      setMessage({ type: 'error', text: 'Failed to upload document' })
    } finally {
      setUploading(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false
  })

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this document?')) return

    try {
      await documentsApi.deleteDocument(id)
      setMessage({ type: 'success', text: 'Document deleted successfully' })
      await loadDocuments()
    } catch (err) {
      console.error('Failed to delete document:', err)
      setMessage({ type: 'error', text: 'Failed to delete document' })
    }
  }

  const handleView = (doc: Document) => {
    setSelectedDoc(doc)
    setViewDialogOpen(true)
  }

  const formatFileSize = (bytes: number) => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    if (bytes === 0) return '0 Bytes'
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
  }

  const getDocumentTypeColor = (type: string) => {
    const colors: Record<string, 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info'> = {
      'credit_card': 'error',
      'bank_statement': 'primary',
      'investment': 'success',
      'tax_document': 'warning',
      'insurance': 'info',
      'loan': 'secondary',
      'other': 'default'
    }
    return colors[type] || 'default'
  }

  const parseAnalysisResult = (result: string) => {
    try {
      return JSON.parse(result)
    } catch {
      return null
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Document Analysis
      </Typography>
      
      <Typography variant="body1" color="textSecondary" paragraph>
        Upload your financial documents (PDF format) for AI-powered analysis and automatic categorization.
      </Typography>

      {message && (
        <Alert severity={message.type} sx={{ mb: 3 }} onClose={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Upload Area */}
        <Grid item xs={12}>
          <Paper
            {...getRootProps()}
            sx={{
              p: 4,
              textAlign: 'center',
              cursor: 'pointer',
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'grey.300',
              bgcolor: isDragActive ? 'action.hover' : 'background.paper',
              '&:hover': {
                bgcolor: 'action.hover',
                borderColor: 'primary.main',
              }
            }}
          >
            <input {...getInputProps()} />
            {uploading ? (
              <Box>
                <CircularProgress sx={{ mb: 2 }} />
                <Typography>Processing document...</Typography>
              </Box>
            ) : (
              <Box>
                <UploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  {isDragActive ? 'Drop your PDF here...' : 'Drag & drop a PDF file here'}
                </Typography>
                <Typography variant="body2" color="textSecondary" gutterBottom>
                  or click to select a file
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<UploadIcon />}
                  sx={{ mt: 2 }}
                  disabled={uploading}
                >
                  Choose File
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Documents List */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Uploaded Documents ({documents.length})
              </Typography>
              
              {loading ? (
                <Box display="flex" justifyContent="center" p={3}>
                  <CircularProgress />
                </Box>
              ) : documents.length === 0 ? (
                <Typography color="textSecondary" sx={{ textAlign: 'center', py: 3 }}>
                  No documents uploaded yet. Upload your first financial document to get started!
                </Typography>
              ) : (
                <List>
                  {documents.map((doc) => {
                    const analysis = parseAnalysisResult(doc.analysis_result || '{}')
                    return (
                      <ListItem key={doc.id} divider>
                        <DocIcon sx={{ mr: 2, color: 'text.secondary' }} />
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Typography variant="subtitle1">
                                {doc.filename}
                              </Typography>
                              <Chip
                                label={analysis?.document_type || doc.document_type}
                                size="small"
                                color={getDocumentTypeColor(analysis?.document_type || doc.document_type)}
                              />
                              {doc.processed && (
                                <Chip
                                  label="Processed"
                                  size="small"
                                  color="success"
                                  variant="outlined"
                                />
                              )}
                            </Box>
                          }
                          secondary={
                            <Box>
                              <Typography variant="body2" color="textSecondary">
                                Size: {formatFileSize(doc.file_size)} • 
                                Uploaded: {new Date(doc.created_at).toLocaleDateString()}
                              </Typography>
                              {analysis?.summary && (
                                <Typography variant="body2" color="textSecondary" sx={{ mt: 0.5 }}>
                                  Net: {analysis.summary.net_change ? 
                                    new Intl.NumberFormat('en-US', { 
                                      style: 'currency', 
                                      currency: 'USD' 
                                    }).format(analysis.summary.net_change) : 'N/A'}
                                  {analysis.transactions && ` • ${analysis.transactions.length} transactions`}
                                </Typography>
                              )}
                            </Box>
                          }
                        />
                        <ListItemSecondaryAction>
                          <IconButton
                            edge="end"
                            onClick={() => handleView(doc)}
                            sx={{ mr: 1 }}
                          >
                            <ViewIcon />
                          </IconButton>
                          <IconButton
                            edge="end"
                            onClick={() => handleDelete(doc.id)}
                            color="error"
                          >
                            <DeleteIcon />
                          </IconButton>
                        </ListItemSecondaryAction>
                      </ListItem>
                    )
                  })}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* View Document Dialog */}
      <Dialog
        open={viewDialogOpen}
        onClose={() => setViewDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Document Analysis: {selectedDoc?.filename}
        </DialogTitle>
        <DialogContent>
          {selectedDoc && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Analysis Results
              </Typography>
              <pre style={{ 
                whiteSpace: 'pre-wrap', 
                fontSize: '0.875rem',
                backgroundColor: '#f5f5f5',
                padding: '16px',
                borderRadius: '4px',
                overflow: 'auto',
                maxHeight: '400px'
              }}>
                {selectedDoc.analysis_result ? 
                  JSON.stringify(parseAnalysisResult(selectedDoc.analysis_result), null, 2) :
                  'No analysis results available'
                }
              </pre>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialogOpen(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}