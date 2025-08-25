/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },
  // Enable strict mode for better development experience
  reactStrictMode: true,
  
  // Optimize performance
  swcMinify: true,
  
  // Configure image domains if needed
  images: {
    domains: [],
  },
  
  // Environment variables that should be available in the browser
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
};

module.exports = nextConfig;