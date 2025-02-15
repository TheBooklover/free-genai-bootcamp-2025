# Implementation Plan: Frontend Setup with React, TypeScript, and ShadCN

## Overview
This plan outlines the step-by-step process of setting up a modern frontend application using React, TypeScript, Tailwind CSS, and ShadCN/UI components.

## Prerequisites
- [x] Node.js installed (v16.0 or higher)
- [x] npm or yarn package manager
- [x] Code editor (VS Code recommended)
- [x] Basic knowledge of React and TypeScript

## Implementation Steps

### 1. Project Creation
- [x] Create new Vite project
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
```
This creates a new project with Vite's React + TypeScript template, providing the base structure.

### 2. Install Core Dependencies
- [x] Install Tailwind and its dependencies
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
These packages enable Tailwind CSS styling and PostCSS processing.

- [x] Install ShadCN/UI
```bash
npm install -D @shadcn/ui
npx shadcn-ui@latest init
```
This sets up ShadCN/UI component library and its configuration.

### 3. Install Additional Dependencies
- [x] Add routing and API client libraries
```bash
npm install @tanstack/react-query
npm install react-router-dom
npm install axios
```
These provide:
- ✓ React Query: API data fetching and caching
- ✓ React Router: Application routing
- ✓ Axios: HTTP client

### 4. Configure Project Structure
- [x] Create essential directories
```bash
mkdir -p src/{components,pages,lib,api}
```
This creates a organized structure:
- ✓ components/: Reusable UI components
- ✓ pages/: Route components
- ✓ lib/: Utility functions
- ✓ api/: API integration code

### 5. Setup API Client
- [x] Create API client configuration
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
- [x] Set up React Query client
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
- [x] Create router configuration
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
- [x] Add base layout component
```typescript:src/components/Layout.tsx
import { ReactNode } from 'react';
import { Outlet } from 'react-router-dom';
import AppSidebar from '@/components/Sidebar';
import Breadcrumbs from '@/components/Breadcrumbs';
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";

interface LayoutProps {
    children?: ReactNode;
}

export function Layout({ children }: LayoutProps) {
    return (
        <SidebarProvider>
            <div className="min-h-screen bg-background">
                <AppSidebar />
                <SidebarInset>
                    <Breadcrumbs />
                    <main className="container mx-auto py-6">
                        {children || <Outlet />}
                    </main>
                </SidebarInset>
            </div>
        </SidebarProvider>
    );
}
```
This provides a consistent layout structure integrating your existing sidebar and breadcrumbs components.

### 9. Testing Setup
- [x] Install testing libraries
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

- [x] Create test setup files
```typescript:src/test/setup.ts
import '@testing-library/jest-dom';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect method
expect.extend(matchers);

// Cleanup after each test case
afterEach(() => {
    cleanup();
});
```
This sets up the testing environment with React Testing Library and Vitest.

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