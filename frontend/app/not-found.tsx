import React from 'react';

// Create a separate component for the 404 page.  This is a React function component.
const NotFoundPage = () => {
  // Now useSearchParams is correctly inside a React function component.
  // const searchParams = useSearchParams(); // Removed:  useSearchParams not directly available in not-found.tsx
  // const searchTerm = searchParams.get('search'); // Removed

  return (
    <div>...Doesnt exist</div>
  );
};

//  Next.js special not-found export.  This *must* be the default export.
export default NotFoundPage;
