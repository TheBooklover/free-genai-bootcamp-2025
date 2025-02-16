import React from 'react';
import { Card, CardContent } from './ui/card';

interface Props {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      return this.props.fallback || (
        <Card>
          <CardContent>
            <div className="text-red-500">
              Something went wrong in this component.
              {this.state.error && (
                <div className="mt-2 text-sm">
                  Error: {this.state.error.message}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      );
    }

    return this.props.children;
  }
} 