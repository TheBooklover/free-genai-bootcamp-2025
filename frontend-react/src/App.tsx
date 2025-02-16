import { ThemeProvider } from "@/components/theme-provider"
import { RouterProvider } from '@tanstack/react-router'
import { NavigationProvider } from './contexts/NavigationContext'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './lib/react-query'
import { router } from './router'

export default function App() {
    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <NavigationProvider>
                <QueryClientProvider client={queryClient}>
                    <RouterProvider router={router} />
                </QueryClientProvider>
            </NavigationProvider>
        </ThemeProvider>
    );
}