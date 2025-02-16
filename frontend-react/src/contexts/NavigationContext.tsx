import { createContext, useContext, useState, ReactNode } from 'react';
import { Group } from '../services/api';

interface NavigationContextType {
  currentGroup: Group | null;
  setCurrentGroup: (group: Group | null) => void;
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

export function NavigationProvider({ children }: { children: ReactNode }) {
  const [currentGroup, setCurrentGroup] = useState<Group | null>(null);

  return (
    <NavigationContext.Provider value={{ currentGroup, setCurrentGroup }}>
      {children}
    </NavigationContext.Provider>
  );
}

export function useNavigation() {
  const context = useContext(NavigationContext);
  if (context === undefined) {
    throw new Error('useNavigation must be used within a NavigationProvider');
  }
  return context;
} 