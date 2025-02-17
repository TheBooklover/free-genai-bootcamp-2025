# Linter Errors Analysis

## High Severity (Must Fix)

### Router Configuration (High Severity, Low Complexity)
- [x] Remove React Router in favor of TanStack Router
  - Why: Having two router implementations causes conflicts and potential runtime errors
  - Impact: Application routing could break unexpectedly
  - Files: App.tsx, router.tsx, package.json

### Missing Module Declarations (High Severity, Medium Complexity)
- [ ] Add missing module declarations:
  - [ ] '../hooks/useGroupWords'
  - [ ] './ui/pagination'
  - [ ] './ui/table'
  - Why: TypeScript can't find these modules, leading to compilation errors
  - Impact: Application won't build until fixed
  - Files: GroupWordsList.tsx

## Medium Severity (Should Fix)

### Icon Import Issues (Medium Severity, Low Complexity)
- [ ] Fix Lucide React icon imports:
  - [ ] ArrowDownIcon → ArrowDown
  - [ ] ArrowUpIcon → ArrowUp
  - [ ] ArrowsUpDownIcon → ArrowsUpDown
  - [ ] ChevronLeftIcon → ChevronLeft
  - [ ] ChevronRightIcon → ChevronRight
  - Why: Icon names have changed in newer versions
  - Impact: Icons won't render correctly
  - Files: GroupWordsList.tsx, pagination.tsx

### Button Component Type Issues (Medium Severity, Medium Complexity)
- [ ] Fix Button component return type:
  ```typescript
  'Button' cannot be used as a JSX component.
  Its return type 'ReactNode' is not a valid JSX element.
  ```
  - Why: Type safety for component rendering
  - Impact: TypeScript compilation errors
  - Files: GroupWordsList.tsx, pagination.tsx

## Low Severity (Nice to Fix)

### Test Setup Issues (Low Severity, Low Complexity)
- [ ] Add missing test setup types:
  - [ ] beforeEach
  - [ ] afterEach
  - Why: Test setup functions aren't properly typed
  - Impact: Only affects test environment
  - Files: setup.ts

### Component Props Issues (Low Severity, Medium Complexity)
- [ ] Fix ErrorBoundary children prop:
  ```typescript
  Property 'children' is missing in type '{}' but required in type 'Props'
  ```
  - Why: Props validation for ErrorBoundary
  - Impact: TypeScript compilation warning
  - Files: GroupDetails.tsx

### Test Rendering Issues (Low Severity, High Complexity)
- [ ] Fix test rendering type errors:
  ```typescript
  No overload matches this call.
  Argument of type 'Element' is not assignable to parameter of type 'ReactNode'
  ```
  - Why: Type mismatch in test rendering
  - Impact: Only affects test environment
  - Files: GroupWordsList.test.tsx

## Impact Scale
- High: Prevents application from running/building
- Medium: Causes runtime errors or significant TypeScript warnings
- Low: Developer experience or best practice issues

## Complexity Scale
- High: Requires significant refactoring or deep understanding
- Medium: Requires moderate changes across multiple files
- Low: Simple find-and-replace or single-file fixes 