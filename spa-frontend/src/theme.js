// theme.js
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#0052ff', 
    },
    secondary: {
      main: '#b9cefa',
    },
  },
  typography: {
    fontFamily: "'Poppins', sans-serif",
    h2: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 500,
    },
  },
});

export default theme;
