/** @type {import('next').NextConfig} */
const nextConfig = {
    
    module: {
        rules: [
          {
            test: /\.(png|jpe?g|gif)$/i,
            type: 'asset/resource', // Or 'asset/inline' for small images
          },
        ],
      },
};

export default nextConfig;
