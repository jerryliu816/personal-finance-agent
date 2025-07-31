import axios from 'axios'
import { Settings, Document, FinancialProfile, ChatMessage, RAGDocument } from '../types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const settingsApi = {
  getSettings: (): Promise<Settings> => 
    api.get('/settings').then(res => res.data),
  
  updateSettings: (settings: Settings): Promise<Settings> =>
    api.post('/settings', settings).then(res => res.data),
}

export const documentsApi = {
  uploadDocument: (file: File, documentType: string = 'financial'): Promise<Document> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('document_type', documentType)
    
    return api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }).then(res => res.data)
  },
  
  getDocuments: (): Promise<Document[]> =>
    api.get('/documents').then(res => res.data),
  
  deleteDocument: (id: number): Promise<void> =>
    api.delete(`/documents/${id}`).then(res => res.data),
}

export const profileApi = {
  getProfile: (): Promise<FinancialProfile> =>
    api.get('/profile').then(res => res.data),
}

export const chatApi = {
  sendMessage: (message: string): Promise<{ response: string }> =>
    api.post('/chat', {
      message,
      timestamp: new Date().toISOString(),
    }).then(res => res.data),
  
  getChatHistory: (): Promise<ChatMessage[]> =>
    api.get('/chat/history').then(res => res.data),
}

export const ragApi = {
  uploadRAGDocument: (file: File): Promise<RAGDocument> => {
    const formData = new FormData()
    formData.append('file', file)
    
    return api.post('/rag/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }).then(res => res.data)
  },
  
  getRAGDocuments: (): Promise<RAGDocument[]> =>
    api.get('/rag/documents').then(res => res.data),
  
  deleteRAGDocument: (id: number): Promise<void> =>
    api.delete(`/rag/documents/${id}`).then(res => res.data),
}