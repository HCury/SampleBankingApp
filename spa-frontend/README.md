
# **Banking App - Frontend**

A modern, responsive banking application built with React and Material UI. This frontend interacts with the FastAPI-based backend to provide user authentication, balance checking, transactions, and fund transfers.

For more details on the backend API, please refer to the **Backend README**.

----------

## Features

 User Authentication - Secure login and signup with JWT authentication  
 Dashboard - Displays user balance and recent transactions  
 Fund Transfers - Send money to other users with real-time validation  
 Transaction History - View all deposits, withdrawals, and transfers  
 Responsive UI - Fully optimized for desktop and mobile  
 Material UI Styling - Clean, modern, and accessible design

----------

## Setup Instructions

All instructions below are for Windows machines.

### 1. Install Dependencies

Make sure you have Node.js and npm installed.

**B. Install dependencies**:

`npm install` 

----------

### 2. Start the Development Server

Run the following command to launch the frontend:

`npm start` 

The application will be available at: `http://localhost:3000`

To test out the backend, please ensure that your backend is running (see README.md for backend)

----------

## Routing Overview

-   `/` = Homepage with features and signup option 
-   `/login` = User login page
-   `/signup` = User registration page
-   `/transactions` = Transaction history and fund transfers
-   `/transfer` = Secure fund transfer page

----------

## **Technology Stack**

-   **React** - Frontend framework
-   **React Router** - Client-side navigation
-   **Material UI** - Styling and UI components
-   **Jest & React Testing Library** - Unit and integration testing
-   **Axios** - API requests to FastAPI backend