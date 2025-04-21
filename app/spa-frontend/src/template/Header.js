import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function Header() {
  const token = localStorage.getItem('access_token');
  const isLoggedIn = Boolean(token);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/'; 
  };

  return (
    <Box sx={{ position: 'relative', marginBottom: '2rem' }}>
      {/* MyBank Brand at the top-left, outside of the AppBar */}
      <Typography
        variant="h4"
        component={RouterLink}
        to="/"
        sx={{
          position: 'absolute',
          top: 10,
          left: 20,
          textDecoration: 'none',
          color: '#0052ff',
          fontWeight: 'bold',
        }}
      >
        Bank of Henrique
      </Typography>

      {/* Centered, pill-shaped AppBar for navigation */}
      <AppBar
        position="static"
        sx={{
          background: 'linear-gradient(90deg, #0052ff 0%, #70a1ff 100%)',
          width: 'fit-content',
          margin: '3rem auto', 
          borderRadius: '9999px',
          boxShadow: 3,
          padding: '0.5rem 1rem',
        }}
      >
        <Toolbar>
          <Box sx={{ display: 'flex', gap: 2 }}>
            {isLoggedIn ? (
              <>
                <Button component={RouterLink} to="/transactions" sx={{ color: 'white' }}>
                  Transactions
                </Button>
                <Button onClick={handleLogout} sx={{ color: 'white' }}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button component={RouterLink} to="/login" sx={{ color: 'white' }}>
                  Login
                </Button>
                <Button component={RouterLink} to="/signup" sx={{ color: 'white' }}>
                  Sign Up
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Header;
