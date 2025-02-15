import { ThemeProvider } from "@/components/theme-provider"
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { NavigationProvider } from '@/context/NavigationContext'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './lib/react-query'
import WordShow from './pages/WordShow'
import { Layout } from '@/components/Layout'

export default function App() {
    return (
        <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
            <NavigationProvider>
                <QueryClientProvider client={queryClient}>
                    <BrowserRouter>
                        <Layout>
                            <Routes>
                                <Route path="/words/:wordId" element={<WordShow />} />
                            </Routes>
                        </Layout>
                    </BrowserRouter>
                </QueryClientProvider>
            </NavigationProvider>
        </ThemeProvider>
    );
}