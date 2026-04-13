# Quick Start Guide

This guide will help you get YiCe up and running on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher**
- **Node.js 18 or higher**
- **npm** or **yarn**
- **Git** (optional, for cloning the repository)

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd YiCe
```

## Step 2: Set Up the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   # Using uv (recommended)
   uv pip install -r pyproject.toml
   
   # Or using pip
   pip install -r pyproject.toml
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend will be available at `http://localhost:8000`

## Step 3: Set Up the Frontend

1. Navigate to the frontend directory (in a new terminal window):
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## Step 4: Verify Installation

1. Open your browser and go to `http://localhost:5173`
2. You should see the YiCe application interface

## Next Steps

- Check out the [Architecture Guide](architecture.md) to learn more about the project structure
- Explore the codebase to understand how everything works
- Start developing new features!

## Troubleshooting

If you encounter any issues:

1. Make sure all prerequisites are installed correctly
2. Check that both backend and frontend servers are running
3. Verify your environment variables are set correctly
4. Check the server logs for error messages
