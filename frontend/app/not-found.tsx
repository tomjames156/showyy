import React, { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';

const NotFoundPage = () => {
  // Function to safely use search params
  const getSearchParams = () => {
    try {
      return useSearchParams();
    } catch (error) {
      console.error("Error using useSearchParams in 404:", error);
      return new URLSearchParams(); // Return empty params to avoid crashing
    }
  };

  const searchParams = getSearchParams(); // Use the safe function
  const query = searchParams.get('query');

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-200 mb-4">404</h1>
      <p className="text-2xl text-gray-600 dark:text-gray-400 mb-8">Page Not Found</p>
      <p className="text-md text-gray-600 dark:text-gray-400 mb-4">
        The requested page could not be found.
      </p>
      {query && (
        <p className="text-md text-gray-600 dark:text-gray-400 mb-8">
          You searched for: <span className="font-semibold text-blue-500">{query}</span>
        </p>
      )}
      <a
        href="/"
        className="text-blue-500 hover:text-blue-700 dark:text-blue-300 dark:hover:text-blue-500 transition-colors duration-200"
      >
        Go back to home
      </a>
    </div>
  );
};

const NotFound = () => {
    return (
      <Suspense fallback={<div>Loading 404 Page...</div>}>
          <NotFoundPage/>
      </Suspense>
    )
}

export default NotFound;
