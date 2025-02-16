import * as React from "react"
import { createContext, useContext, useState } from 'react';
import { Group } from '../services/api';

interface NavigationContextType {
  currentGroup: Group | null;
  setCurrentGroup: (group: Group | null) => void;
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

interface NavigationProviderProps {
  children: React.ReactNode;
}

export function NavigationProvider({ children }: NavigationProviderProps) {
  const [currentGroup, setCurrentGroup] = useState<Group | null>(null);

  const value = {
    currentGroup,
    setCurrentGroup,
  };

  return (
    <div className="navigation-provider">
      <NavigationContext.Provider value={value}>
        {children}
      </NavigationContext.Provider>
    </div>
  );
}

export function useNavigation() {
  const context = useContext(NavigationContext);
  if (context === undefined) {
    throw new Error('useNavigation must be used within a NavigationProvider');
  }
  return context;
} 