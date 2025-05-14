'use client'

import React, { createContext, useState, useEffect } from 'react';
import { UserData } from '@/app/lib/definitions';
import { useSearchParams } from 'next/navigation'; // Import useParams

interface AppContextProps {
  profile: UserData | null;
  setProfile: (profile: UserData | null) => void;
  loading: boolean; // Add loading state to context
  error: string | null;   // Add error state to context
}

export const ProfileContext = createContext<AppContextProps | undefined>(undefined);

export function ProfileContextProvider({ children }: { children: React.ReactNode }) {
  const [profile, setProfile] = useState<UserData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams()
  const username = searchParams.get('username') // Get username

  useEffect(() => {
    const fetchProfile = async () => {
        console.log("Yeah")
      if (!username) {
        setLoading(false);
        return; // Important: Exit the function!
      }

      setLoading(true);
      setError(null);
      try {
        // Replace with your actual API endpoint
        const response = await fetch(`https://showyy.onrender.com/profile/${username}/`);
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

    // Only fetch if username is available
    if (username) {
      fetchProfile();
    } else {
       setLoading(false); // Set loading to false if no username
    }
  }, [username]); // Dependency array: fetch again if username changes

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