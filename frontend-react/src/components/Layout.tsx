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