import { ReactNode } from "react";

interface LayoutProps {
  children?: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto py-6">
        {children}
      </main>
    </div>
  );
} 