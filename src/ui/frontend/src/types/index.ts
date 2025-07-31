export interface Settings {
  id?: number
  llm_provider: string
  llm_api_key: string
  gmail_server?: string
  gmail_username?: string
  gmail_password?: string
  auto_check_email: boolean
  check_interval: number
  created_at?: string
  updated_at?: string
}

export interface Document {
  id: number
  filename: string
  filepath: string
  document_type: string
  analysis_result?: string
  file_size: number
  processed: boolean
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  message: string
  response: string
  timestamp: string
}

export interface FinancialProfile {
  total_assets: number
  total_liabilities: number
  net_worth: number
  monthly_income: number
  monthly_expenses: number
  investment_portfolio: Record<string, number>
  credit_accounts: Array<{
    name: string
    balance: number
    limit: number
    rate: number
  }>
  recent_transactions: Array<{
    date: string
    description: string
    amount: number
    category: string
    subcategory: string
  }>
  last_updated: string
}

export interface RAGDocument {
  id: number
  filename: string
  filepath: string
  content?: string
  chunk_count: number
  processed: boolean
  created_at: string
}