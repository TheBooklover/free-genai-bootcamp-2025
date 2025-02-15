declare module 'react/jsx-runtime' {
  export namespace JSX {
    interface Element {}
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
  export function jsx(type: any, props: any): JSX.Element;
  export function jsxs(type: any, props: any): JSX.Element;
} 