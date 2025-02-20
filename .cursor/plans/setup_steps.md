# Setting Up Local Development Environment

## Prerequisites
1.1. [ ] Install Python 3.8 or higher
   - Python is the programming language we'll use for the backend server
   - Download it from python.org - choose the version that matches your operating system
   - This is needed to run our backend code and handle database operations

1.2. [ ] Install Node.js 16 or higher
   - Node.js lets us run JavaScript code outside a web browser
   - Download it from nodejs.org - pick the "LTS" (Long Term Support) version
   - We need this to build and run our frontend user interface

1.3. [ ] Ensure pip is installed with Python
   - pip is Python's package manager - it helps us install Python libraries
   - Usually comes with Python installation
   - Open terminal/command prompt and type "pip --version" to verify

1.4. [ ] Ensure npm is installed with Node.js
   - npm is Node's package manager - it helps us install JavaScript libraries
   - Comes automatically with Node.js
   - Open terminal/command prompt and type "npm --version" to verify

## Backend Setup

### Step 1: Initial Setup
1.1. [ ] Navigate to backend-flask directory
   - Open your terminal/command prompt
   - Use "cd" command to move to the backend-flask folder
   - This is where our backend server code lives

1.2. [ ] Create a virtual environment
   - A virtual environment is like a clean room for your Python project
   - It keeps project dependencies separate from other Python projects
   - Run: "python -m venv venv" to create it

1.3. [ ] Activate the virtual environment
   - This tells your computer to use the Python version in your virtual environment
   - On Windows, run: "venv\Scripts\activate"
   - On Mac/Linux, run: "source venv/bin/activate"

1.4. [ ] Install required Python packages from requirements.txt
   - This installs all the libraries our backend needs
   - Run: "pip install -r requirements.txt"
   - You'll see a list of packages being installed

### Step 2: Database Setup
2.1. [ ] Navigate to backend-flask directory
   - Make sure you're in the right folder
   - The database setup scripts are located here

2.2. [ ] Run database initialization command
   - This creates your database and sets up its structure
   - Run: "flask db upgrade"
   - This will create tables and relationships in your database

2.3. [ ] Verify database creation
   - Check that a new SQLite database file was created
   - Look for a file ending in ".db" in your directory
   - This is where all your data will be stored

### Step 3: Start Backend Server
3.1. [ ] Ensure you're in backend-flask directory
   - Double-check your location with "pwd" (Mac/Linux) or "cd" (Windows)
   - You should see backend-flask as your current directory

3.2. [ ] Start the Flask development server
   - This launches your backend server
   - Run: "flask run"
   - You'll see messages about the server starting up

3.3. [ ] Verify server is running at localhost:5000
   - Open your web browser
   - Go to http://localhost:5000
   - You should see a welcome message

## Frontend Setup

### Step 1: Initial Setup
1.1. [ ] Open a new terminal
   - Keep your backend terminal running
   - Open a separate terminal window/tab
   - This is where we'll run frontend commands

1.2. [ ] Navigate to frontend-react directory
   - Use "cd" to move to the frontend-react folder
   - This contains our user interface code

1.3. [ ] Install Node dependencies
   - This gets all the required JavaScript libraries
   - Run: "npm install"
   - This might take a few minutes

### Step 2: Start Frontend Server
2.1. [ ] Start the development server
   - This launches your frontend application
   - Run: "npm start"
   - Wait for the compilation to complete

2.2. [ ] Verify application is running at localhost:8080
   - Open your web browser
   - Visit http://localhost:8080
   - You should see the application's interface

## Verification Steps

### Backend Verification
1.1. [ ] Open web browser
   - Use any modern web browser (Chrome, Firefox, Safari, etc.)

1.2. [ ] Navigate to localhost:5000
   - Type http://localhost:5000 in your browser's address bar
   - This connects to your backend server

1.3. [ ] Confirm "Flask is working!" message
   - You should see a success message
   - This means your backend is running correctly

### Frontend Verification
2.1. [ ] Open web browser
   - Use the same or a new browser window

2.2. [ ] Navigate to localhost:8080
   - Type http://localhost:8080 in your browser's address bar
   - This connects to your frontend application

2.3. [ ] Confirm dashboard appears
   - You should see your application's interface
   - All styling and components should load properly

### API Verification
3.1. [ ] Test words endpoint
   - Visit http://localhost:5000/api/words
   - Should see a list of words in JSON format
   - This tests if your backend can serve data

3.2. [ ] Test groups endpoint
   - Visit http://localhost:5000/api/groups
   - Should see a list of groups in JSON format
   - This verifies group functionality

3.3. [ ] Test study-activities endpoint
   - Visit http://localhost:5000/api/study-activities
   - Should see activity data in JSON format
   - This checks if activity tracking works

## Common Issues

### Database Issues
1.1. [ ] Delete existing database file
   - Find and remove the .db file in your backend directory
   - This gives you a fresh start if your database is corrupted

1.2. [ ] Reinitialize database
   - Run database setup commands again
   - This creates a new, clean database

1.3. [ ] Verify new database creation
   - Check for the new .db file
   - Ensure it has the correct permissions

### Port Conflicts
2.1. [ ] Check for processes using port 5000
   - Another program might be using the required port
   - On Mac/Linux, use: "lsof -i :5000"
   - On Windows, use: "netstat -ano | findstr :5000"

2.2. [ ] Stop conflicting process
   - Find the process ID from previous command
   - Stop it using Task Manager or terminal commands
   - This frees up the port for your application

2.3. [ ] Restart server
   - Start your backend server again
   - Verify it starts without port conflicts

### Frontend Build Issues
3.1. [ ] Clear node modules
   - Delete the node_modules folder
   - This removes potentially corrupted dependencies

3.2. [ ] Clean npm cache
   - Run: "npm cache clean --force"
   - This ensures a clean slate for installations

3.3. [ ] Reinstall dependencies
   - Run: "npm install"
   - This gets fresh copies of all dependencies

3.4. [ ] Rebuild application
   - Run: "npm run build"
   - This creates a fresh build of your application

## Development Workflow
1.1. [ ] Keep both servers running
   - Backend server on port 5000
   - Frontend server on port 8080
   - Both need to run simultaneously

1.2. [ ] Backend changes auto-reload
   - Flask will automatically detect most changes
   - Some changes might require manual restart

1.3. [ ] Frontend changes hot-reload
   - React will automatically update the browser
   - No manual refresh needed for most changes

1.4. [ ] Monitor terminal for errors
   - Watch both terminal windows
   - Red text usually indicates problems
   - Error messages help diagnose issues

1.5. [ ] Check browser console for frontend issues
   - Right-click in browser, select "Inspect"
   - Go to "Console" tab
   - Look for errors or warnings in red/yellow

Would you like me to elaborate on any of these steps? 