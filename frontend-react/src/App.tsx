import * as React from "react"
import { ThemeProvider } from "@/components/theme-provider"
import { RouterProvider } from 'react-router-dom'
import { NavigationProvider } from './contexts/NavigationContext'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { router } from './router'

const queryClient = new QueryClient()

export function App() {
  const routerContent = <RouterProvider router={router} />;

  return (
    <div className="app-root">
      <NavigationProvider>
        <QueryClientProvider client={queryClient}>
          <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            {routerContent}
          </ThemeProvider>
        </QueryClientProvider>
      </NavigationProvider>
    </div>
  )
}

export default App;