import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress
} from '@mui/material';
// import { useNavigate } from 'react-router-dom';

function TransactionsPage() {
  const [transactions, setTransactions] = useState([]);
  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [balanceLoading, setBalanceLoading] = useState(true);
  const [error, setError] = useState(null);
  const [transferDialogOpen, setTransferDialogOpen] = useState(false);
  const [transferRecipient, setTransferRecipient] = useState('');
  const [transferAmount, setTransferAmount] = useState('');
  const [transferLoading, setTransferLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('No token found. Please log in first.');
      setLoading(false);
      setBalanceLoading(false);
      return;
    }

    // Fetch transactions
    fetch('http://localhost:8000/transactions?page=1&limit=10', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch transactions');
        }
        return response.json();
      })
      .then((data) => {
        setTransactions(data.transactions || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });

    // Fetch balance
    fetch('http://localhost:8000/balance', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch balance');
        }
        return response.json();
      })
      .then((data) => {
        setBalance(data.balance);
        setBalanceLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setBalanceLoading(false);
      });
  }, []);

  if (loading || balanceLoading) return <p>Loading...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  // Handlers for opening/closing the transfer dialog
  const handleOpenTransferDialog = () => {
    setTransferDialogOpen(true);
  };

  const handleCloseTransferDialog = () => {
    setTransferDialogOpen(false);
    setTransferRecipient('');
    setTransferAmount('');
  };

  // Handle transfer submission
  const handleTransferSubmit = async () => {
    if (!transferRecipient || !transferAmount) {
        alert('Please enter both recipient username and amount.');
        return;
    }

    const token = localStorage.getItem('access_token');
    if (!token) {
        alert('No token found. Please log in first.');
        return;
    }

    setTransferLoading(true);

    try {
        const recipientUsername = transferRecipient;
        const amount = parseFloat(transferAmount);

        // Build the URL with query parameters
        const url = `http://localhost:8000/transfer?recipient_username=${encodeURIComponent(recipientUsername)}&amount=${amount}`;

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert('Transfer successful!');
            window.location.reload();
        } else {
            alert(data.detail || data.message || 'Transfer Failed');
        }
    } catch (error) {
        console.error('Transfer Error:', error);
        alert('Something went wrong during the transfer.');
    } finally {
        setTransferLoading(false);
        handleCloseTransferDialog();
    }
};

  return (
    <Box sx={{ margin: '20px', textAlign: 'center' }}>
      {/* Balance Section */}
      <Box
        sx={{
          backgroundColor: '#b9cefa', // Light blue background
          borderRadius: '16px',
          padding: '20px',
          display: 'inline-block',
          marginBottom: '20px'
        }}
      >
        <Typography variant="h2" gutterBottom style={{ color: '#0052ff' }}>
          {balance !== null ? `$${balance}` : 'Balance unavailable'}
        </Typography>
      </Box>

      {/* Transfer Funds Button on the Right */}
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 2 }}>
        <Button
          variant="contained"
          sx={{
            backgroundColor: '#0052ff',
            color: 'white',
            '&:hover': { backgroundColor: '#0042cc' }
          }}
          onClick={handleOpenTransferDialog}
        >
          Transfer Funds
        </Button>
      </Box>

      {/* Transfer Funds Dialog */}
      <Dialog open={transferDialogOpen} onClose={handleCloseTransferDialog}>
        <DialogTitle>Transfer Funds</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Recipient Username"
            type="text"
            fullWidth
            variant="standard"
            value={transferRecipient}
            onChange={(e) => setTransferRecipient(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Amount"
            type="number"
            fullWidth
            variant="standard"
            value={transferAmount}
            onChange={(e) => setTransferAmount(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseTransferDialog}>Cancel</Button>
          <Button onClick={handleTransferSubmit} disabled={transferLoading}>
            {transferLoading ? <CircularProgress size={24} /> : 'Submit'}
          </Button>
        </DialogActions>
      </Dialog>

      <Typography variant="h5" gutterBottom style={{ color: '#0052ff' }}>
        Transaction History
      </Typography>

      {transactions.length > 0 ? (
        <TableContainer component={Paper}>
          <Table aria-label="transactions table">
            <TableHead>
              <TableRow>
                <TableCell style={{ color: '#0052ff' }}>
                  <strong>Type</strong>
                </TableCell>
                <TableCell align="center" style={{ color: '#0052ff' }}>
                  <strong>Amount</strong>
                </TableCell>
                <TableCell style={{ color: '#0052ff' }}>
                  <strong>Date</strong>
                </TableCell>
                <TableCell style={{ color: '#0052ff' }}>
                  <strong>Description</strong>
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {transactions.map((txn) => {
                let textColor = 'inherit';
                if (txn.transaction_type === 'deposit') {
                  textColor = 'green';
                } else if (txn.transaction_type === 'withdrawal') {
                  textColor = 'red';
                }
                return (
                  <TableRow key={txn.id}>
                    <TableCell style={{ color: textColor }}>
                      {txn.transaction_type}
                    </TableCell>
                    <TableCell align="center" style={{ color: textColor }}>
                      {`$${txn.amount}`}
                    </TableCell>
                    <TableCell style={{ color: textColor }}>
                      {new Date(txn.transaction_date).toLocaleString()}
                    </TableCell>
                    <TableCell style={{ color: textColor }}>
                      {txn.description}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <Typography style={{ color: '#0052ff' }}>
          No transactions found.
        </Typography>
      )}
    </Box>
  );
}

export default TransactionsPage;
