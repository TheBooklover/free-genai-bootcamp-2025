# Québécois French Migration Implementation Plan

## Overview
This plan outlines the necessary changes to transition from Japanese to Québécois French language learning.

## Prerequisites
- [x] Database backup completed
- [x] Migration script created
- [x] Test data prepared
- [x] Frontend components identified for updates

## Step-by-Step Implementation

1. Database Schema Migration
   - [ ] 1.1. Execute backup of existing data
   - [ ] 1.2. Drop existing Japanese-specific tables
   - [ ] 1.3. Create new Québécois-focused tables
   - [ ] 1.4. Add appropriate indexes
   - [ ] 1.5. Create updated triggers
   **Risk**: Application-wide crashes if database operations fail
   **Impact**: Critical - Core data structure

2. Update Route Parameters
   - [ ] 2.1. Modify sort_by defaults from 'kanji' to 'quebecois'
   - [ ] 2.2. Update valid_columns arrays
   - [ ] 2.3. Update filter parameters
   - [ ] 2.4. Validate new column names
   **Risk**: Group sorting and filtering functionality breaks
   **Impact**: High - User navigation affected

3. Update Data Import Functions
   - [ ] 3.1. Modify SQL insert statements
   - [ ] 3.2. Update JSON parsing logic
   - [ ] 3.3. Add new field validations
   - [ ] 3.4. Update seed data structure
   **Risk**: Data seeding fails, no initial data available
   **Impact**: High - Empty application state

4. Frontend Component Updates
   - [ ] 4.1. Update WordsTable columns
   - [ ] 4.2. Modify sort key types
   - [ ] 4.3. Update column headers
   - [ ] 4.4. Add new field displays
   **Risk**: UI rendering errors, missing data
   **Impact**: High - User experience degraded

5. Study Session Functionality
   - [ ] 5.1. Update word data structure
   - [ ] 5.2. Modify response formats
   - [ ] 5.3. Update progress tracking
   - [ ] 5.4. Adjust review logic
   **Risk**: Progress tracking breaks
   **Impact**: Critical - Core functionality

6. SQL Setup Files
   - [ ] 6.1. Remove Japanese-specific schemas
   - [ ] 6.2. Update table creation scripts
   - [ ] 6.3. Modify foreign key relationships
   - [ ] 6.4. Update indexes
   **Risk**: Incorrect database structure in new deployments
   **Impact**: Critical - System integrity

7. Word Review System
   - [ ] 7.1. Update foreign key constraints
   - [ ] 7.2. Modify review tracking logic
   - [ ] 7.3. Update progress calculations
   - [ ] 7.4. Adjust mastery criteria
   **Risk**: Progress monitoring fails
   **Impact**: High - Learning tracking affected

8. Frontend Word Display
   - [ ] 8.1. Add Québécois-specific fields
   - [ ] 8.2. Update detail views
   - [ ] 8.3. Add pronunciation display
   - [ ] 8.4. Include usage notes
   **Risk**: Incorrect/missing word information
   **Impact**: Medium - Content display affected

9. Dashboard Statistics
   - [ ] 9.1. Update calculation queries
   - [ ] 9.2. Add Québécois-specific metrics
   - [ ] 9.3. Modify progress tracking
   - [ ] 9.4. Update statistical displays
   **Risk**: Incorrect statistics shown
   **Impact**: Medium - Reporting affected

10. Test Suite Updates
    - [ ] 10.1. Modify test data
    - [ ] 10.2. Update expected responses
    - [ ] 10.3. Add new field validations
    - [ ] 10.4. Create Québécois-specific tests
    **Risk**: False positive test results
    **Impact**: High - Quality assurance compromised

## Validation Checklist
- [ ] Database schema correctly reflects Québécois structure
- [ ] Routes handle new field structure
- [ ] Frontend displays all new fields correctly
- [ ] Study session tracking works with new structure
- [ ] Statistics calculate correctly
- [ ] All tests pass with new structure

## Testing Steps
1. Run migration with test data
2. Verify frontend displays
3. Test study session functionality
4. Validate statistics calculations
5. Run complete test suite

## Files Modified/Created
- `backend-flask/migrations/03_update_words_for_quebecois.sql`
- `backend-flask/routes/*.py`
- `frontend-react/src/components/WordsTable.tsx`
- `frontend-react/src/pages/WordShow.tsx`
- `backend-flask/tests/*`

## Implementation Summary
1. Database Structure
   1.1. New Québécois-specific fields
   1.2. Updated relationships
   1.3. Proper indexing

2. Frontend Updates
   2.1. Modified displays
   2.2. Updated sorting
   2.3. New field handling

3. Backend Logic
   3.1. Updated routes
   3.2. Modified queries
   3.3. New validation rules

4. Testing Coverage
   4.1. Updated test cases
   4.2. New field validation
   4.3. Complete coverage