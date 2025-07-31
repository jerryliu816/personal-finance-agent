import React, { useState, useEffect } from 'react'
import {
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemText,
  Chip,
} from '@mui/material'
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts'
import { profileApi } from '../services/api'
import { FinancialProfile } from '../types'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']

export default function Dashboard() {
  const [profile, setProfile] = useState<FinancialProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadProfile()
  }, [])

  const loadProfile = async () => {
    try {
      setLoading(true)
      const data = await profileApi.getProfile()
      setProfile(data)
      setError(null)
    } catch (err) {
      console.error('Failed to load profile:', err)
      setError('Failed to load financial profile')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>
  }

  if (!profile) {
    return (
      <Alert severity="info">
        No financial data available. Upload some documents to get started!
      </Alert>
    )
  }

  const portfolioData = Object.entries(profile.investment_portfolio).map(([symbol, value]) => ({
    name: symbol,
    value,
  }))

  const netWorthData = [
    { name: 'Assets', value: profile.total_assets },
    { name: 'Liabilities', value: profile.total_liabilities },
  ]

  const formatCurrency = (value: number) => 
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Financial Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Net Worth
              </Typography>
              <Typography variant="h5" color={profile.net_worth >= 0 ? 'success.main' : 'error.main'}>
                {formatCurrency(profile.net_worth)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Monthly Income
              </Typography>
              <Typography variant="h5" color="success.main">
                {formatCurrency(profile.monthly_income)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Monthly Expenses
              </Typography>
              <Typography variant="h5" color="error.main">
                {formatCurrency(profile.monthly_expenses)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Monthly Savings
              </Typography>
              <Typography 
                variant="h5" 
                color={profile.monthly_income - profile.monthly_expenses >= 0 ? 'success.main' : 'error.main'}
              >
                {formatCurrency(profile.monthly_income - profile.monthly_expenses)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Net Worth Chart */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Assets vs Liabilities
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={netWorthData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip formatter={(value) => formatCurrency(Number(value))} />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Investment Portfolio */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Investment Portfolio
              </Typography>
              {portfolioData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={portfolioData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${formatCurrency(value)}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {portfolioData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => formatCurrency(Number(value))} />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <Typography color="textSecondary">
                  No investment data available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Transactions */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Transactions
              </Typography>
              {profile.recent_transactions.length > 0 ? (
                <List>
                  {profile.recent_transactions.slice(0, 10).map((txn, index) => (
                    <ListItem key={index} divider>
                      <ListItemText
                        primary={txn.description}
                        secondary={`${txn.date} • ${txn.category}`}
                      />
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Chip
                          label={txn.category}
                          size="small"
                          variant="outlined"
                        />
                        <Typography
                          variant="h6"
                          color={txn.amount >= 0 ? 'success.main' : 'error.main'}
                        >
                          {formatCurrency(txn.amount)}
                        </Typography>
                      </Box>
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography color="textSecondary">
                  No recent transactions available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}