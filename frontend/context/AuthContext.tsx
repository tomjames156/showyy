'use client'

import React, { createContext, useState, useCallback, useEffect } from 'react';
import { Cookies } from 'react-cookie'; // Import the react-cookie library

const cookies = new Cookies();

// Define the type for your context value
interface AuthContextProps {
  token: string | null;
  setToken: (token: string | null) => void;
  isLoggedIn: boolean;
  login: (token: string) => void;
  logout: () => void;
}

// Create the context
const AuthContext = createContext<AuthContextProps | null>(null);

const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setTokenState] = useState<string | null>(null);

    //Use useEffect to run this code only on the client side
    useEffect(() => {
        const storedToken = cookies.get('jwt_token');
        if (storedToken) {
            setTokenState(storedToken);
        }
    }, []);

  // Use useCallback for memoization
  const setToken = useCallback((newToken: string | null) => {
    setTokenState(newToken);
        if (newToken) {
          cookies.set('jwt_token', newToken, {
            path: '/', //  Make the cookie available across the entire domain
            // secure: true,  //  Only send over HTTPS (recommended for production)
            // httpOnly: true, //  Prevent client-side JavaScript access (recommended)
            // maxAge: 2592000, // Example: 30 days (in seconds)
          });
        } else {
          cookies.remove('jwt_token', { path: '/' });
        }
  }, []);

  const login = useCallback((newToken: string) => {
    setToken(newToken);
  }, [setToken]);

  const logout = useCallback(() => {
    setToken(null);
  }, [setToken]);

  const isLoggedIn = !!token;

  const contextValue = {
    token,
    setToken,
    isLoggedIn,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export { AuthProvider, useAuth };
