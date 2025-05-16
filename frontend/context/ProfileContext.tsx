'use client'

import React, { createContext, useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { UserData } from '@/app/lib/definitions';
import { head } from 'framer-motion/client';

interface AppContextProps {
  profile: UserData | null;
  setProfile: (profile: UserData | null) => void;
  loading: boolean; // Add loading state to context
  error: string | null;   // Add error state to context
}

export const ProfileContext = createContext<AppContextProps | undefined>(undefined);

export function ProfileContextProvider({ children }: { children: React.ReactNode }) {
  const searchParams = useSearchParams()
  const [profile, setProfile] = useState<UserData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const username = searchParams.get("username")

  useEffect(() => {
    const fetchProfile = async () => {

      try {
        // Replace with your actual API endpoint
        const response = await fetch(`https://showyy.onrender.com/portfolios/`, {
          method: 'POST',
          headers: {
          }
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch profile: ${response.status}`);
        }
        const data: UserData = await response.json();
        setProfile(data);
      } catch (err: any) {
        setError(err.message || 'An error occurred while fetching profile.');
      } finally {
        setLoading(false);
      }
    };

    if (username) {
      fetchProfile();
    } else {
       setLoading(false); // Set loading to false if no username
    }
  }, [username]);;

  const contextValue = {
    profile,
    setProfile,
    loading, // Include loading state in context
    error,   // Include error state in context
  };

  return (
    <ProfileContext.Provider value={contextValue}>
      {children}
    </ProfileContext.Provider>
  );
}