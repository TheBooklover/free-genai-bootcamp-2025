# Implementation Plan: Frontend Setup with React, TypeScript, and ShadCN

## Overview
This plan outlines the step-by-step process of setting up a modern frontend application using React, TypeScript, Tailwind CSS, and ShadCN/UI components.

## Prerequisites
- [ ] Node.js installed (v16.0 or higher)
- [ ] npm or yarn package manager
- [ ] Code editor (VS Code recommended)
- [ ] Basic knowledge of React and TypeScript

## Implementation Steps

### 1. Project Creation
- [ ] Create new Vite project
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```
This creates a new project with Vite's React + TypeScript template, providing the base structure.

### 2. Install Core Dependencies
- [ ] Install Tailwind and its dependencies
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
These packages enable Tailwind CSS styling and PostCSS processing.

- [ ] Install ShadCN/UI
```bash
npm install -D @shadcn/ui
npx shadcn-ui@latest init
```
This sets up ShadCN/UI component library and its configuration.

### 3. Install Additional Dependencies
- [ ] Add routing and API client libraries
```bash
npm install @tanstack/react-query
npm install react-router-dom
npm install axios
```
These provide:
- React Query: API data fetching and caching
- React Router: Application routing
- Axios: HTTP client

### 4. Configure Project Structure
- [ ] Create essential directories
```bash
mkdir -p src/{components,pages,lib,api}
```
This creates a organized structure:
- components/: Reusable UI components
- pages/: Route components
- lib/: Utility functions
- api/: API integration code

### 5. Setup API Client
- [ ] Create API client configuration
```typescript:src/lib/axios.ts
import axios from 'axios';

export const api = axios.create({
    baseURL: 'http://localhost:5000/api',
    headers: {
        'Content-Type': 'application/json',
    }
});
```
This creates a configured Axios instance for API calls.

### 6. Configure React Query
- [ ] Set up React Query client
```typescript:src/lib/react-query.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 5 * 60 * 1000, // 5 minutes
            cacheTime: 10 * 60 * 1000, // 10 minutes
        },
    },
});
```
This configures React Query for data fetching and caching.

### 7. Setup Routing
- [ ] Create router configuration
```typescript:src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './lib/react-query';

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <Routes>
                    {/* Routes will go here */}
                </Routes>
            </BrowserRouter>
        </QueryClientProvider>
    );
}
```
This sets up the basic routing structure with React Query integration.

### 8. Create Layout Component
- [ ] Add base layout component
```typescript:src/components/Layout.tsx
import { Outlet } from 'react-router-dom';

export function Layout() {
    return (
        <div className="min-h-screen bg-background">
            <header className="border-b">
                {/* Header content */}
            </header>
            <main className="container mx-auto py-6">
                <Outlet />
            </main>
        </div>
    );
}
```
This provides a consistent layout structure for all pages.

### 9. Testing Setup
- [ ] Install testing libraries
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

- [ ] Create test setup file
```typescript:src/test/setup.ts
import '@testing-library/jest-dom';
```
This sets up the testing environment.

## API Documentation

The frontend will communicate with these backend endpoints:

### GET /words
Fetches list of words
```typescript
interface Word {
    id: number;
    quebecois: string;
    standard_french: string;
    english: string;
    // ... other fields
}

// Example usage with React Query
const { data: words } = useQuery({
    queryKey: ['words'],
    queryFn: () => api.get('/words').then(res => res.data)
});
```

### GET /words/{wordId}
Fetches detailed word information
```typescript
// Example usage
const { data: wordDetails } = useQuery({
    queryKey: ['word', wordId],
    queryFn: () => api.get(`/words/${wordId}`).then(res => res.data)
});
```

## Additional Considerations
- [ ] Add error boundary components
- [ ] Implement loading states
- [ ] Add form validation library (e.g., Zod)
- [ ] Set up environment variables
- [ ] Add authentication state management
- [ ] Implement dark mode toggle 