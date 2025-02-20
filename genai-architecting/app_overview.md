# Language Learning Application: Québécois French

## Core Purpose
This is an AI-powered language learning platform specifically designed to teach Québécois French, focusing on the unique regional expressions, pronunciations, and cultural nuances that distinguish it from standard French.

## Key Components

### 1. Word Management System
#### Word Database
- Stores vocabulary with multiple fields:
  - Québécois French expression
  - Standard French equivalent 
  - English translation
  - Pronunciation guides
  - Usage notes
  - Performance statistics (correct/wrong counts)

#### Word Groups
- Organized collections of related words
- Pre-populated lesson sets (e.g., "Core Verbs", "Core Adjectives")
- Progress tracking per group
- Word count and mastery statistics

### 2. Study System
#### Study Activities
- Different types of learning exercises
- Interactive practice sessions  
- Real-time feedback on pronunciation and usage
- Progress tracking per activity

#### Study Sessions
- Track individual learning sessions
- Record performance metrics
- Store review items and corrections
- Calculate success rates
- Maintain user learning streaks

### 3. Progress Tracking
#### Word Reviews
- Records correct/incorrect attempts
- Tracks mastery levels
- Calculates success rates
- Identifies challenging words

#### Dashboard Analytics
- Total vocabulary progress
- Words studied vs. total available
- Mastered words count
- Current learning streak
- Active groups in last 30 days
- Overall success rate
- Total study sessions

### 4. User Interface Features
#### Theme Support
- Light/Dark/System theme options
- Persistent user preferences

#### Navigation
- Group browsing
- Word lists with sorting/filtering
- Study activity selection
- Session history
- Progress dashboard

## Feature Interactions

### Study Flow
1. **Activity Selection**
   - User selects a word group
   - Chooses a study activity
   - System creates new study session

2. **Learning Process**
   - Words presented based on activity type
   - User provides responses
   - System records performance
   - Real-time feedback provided

3. **Progress Updates**
   - Session results recorded
   - Word review statistics updated
   - Group progress calculated
   - Dashboard statistics refreshed

### Data Flow
1. **Word Management**
   ```
   Words ←→ Word Groups ←→ Study Sessions ←→ Word Reviews
   ```

2. **Progress Tracking**
   ```
   Study Sessions → Word Reviews → Progress Statistics → Dashboard
   ```

3. **Learning Analytics**
   ```
   Word Reviews → Success Rates → Mastery Levels → Adaptive Learning
   ```

## Technical Implementation

### Backend (Flask)
- RESTful API architecture
- SQLite database
- Cross-origin resource sharing (CORS)
- Rate limiting for API endpoints
- Error handling and logging
- Database migrations system

### Frontend (React)
- TypeScript implementation
- Component-based architecture
- Context-based state management
- Responsive design
- Theme support
- Real-time updates

### API Endpoints
1. **Words API**
   - GET /words (paginated list)
   - GET /words/{id} (details)

2. **Groups API**
   - GET /groups (paginated list)
   - GET /groups/{id} (details)
   - GET /groups/{id}/words (group words)
   - GET /groups/{id}/words/raw (bulk data)

3. **Study Sessions API**
   - GET /study-sessions (history)
   - POST /study-sessions (create)
   - GET /study-sessions/{id} (details)
   - POST /study-sessions/reset (clear history)

4. **Dashboard API**
   - GET /dashboard/recent-session
   - GET /dashboard/stats

### Security Features
- Rate limiting on API endpoints
- Input validation and sanitization
- Error handling and logging
- CORS configuration
- Database connection management

## Performance Considerations
- Pagination for large data sets
- Efficient JOIN operations
- Proper indexing
- Memory usage optimization
- Caching strategies
- Rate limiting for API stability

## Future Enhancements

### 1. AI Integration
- Speech recognition for pronunciation
- Adaptive learning paths
- Personalized feedback
- Context-aware corrections

### 2. Content Expansion
- Additional word groups
- More study activities
- Cultural context integration
- Advanced usage examples

### 3. User Features
- Custom word lists
- Progress sharing
- Achievement system
- Social learning features

This application provides a comprehensive platform for learning Québécois French, with strong emphasis on tracking progress and providing meaningful feedback to learners. The modular design allows for easy expansion and enhancement of features while maintaining performance and user experience. 