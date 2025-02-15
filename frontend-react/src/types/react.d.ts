/// <reference types="react" />
/// <reference types="react-router-dom" />
/// <reference types="lucide-react" />

declare module 'react' {
  export = React;
  export const useState: <T>(initialState: T | (() => T)) => [T, (newState: T | ((prevState: T) => T)) => void];
  export const useEffect: (effect: () => void | (() => void), deps?: readonly any[]) => void;
}

declare module 'react-router-dom' {
  export interface LinkProps {
    to: string;
    className?: string;
    children?: React.ReactNode;
  }
  export const Link: React.FC<LinkProps>;
  export const useParams: <T extends Record<string, string>>() => T;
}

declare module 'lucide-react' {
  export const ChevronUp: React.FC<{ className?: string }>;
  export const ChevronDown: React.FC<{ className?: string }>;
} 