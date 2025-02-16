import * as React from "react"
import { ThemeProvider } from "@/components/theme-provider"
import { RouterProvider } from '@tanstack/react-router'
import { NavigationProvider } from './contexts/NavigationContext'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './lib/react-query'
import { router } from './router'

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