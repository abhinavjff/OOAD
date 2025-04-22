# Food Delivery System

This is a Streamlit-based food delivery system with both frontend and backend components.

## Prerequisites

1. Python 3.8 or higher installed on your system
2. pip (Python package installer)

## Setup Instructions

1. First, create a virtual environment (recommended):
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required packages:
   ```bash
   pip install streamlit requests python-dotenv
   ```

3. Make sure you have the backend server running:
   - Navigate to the backend directory
   - Install backend dependencies (if any)
   - Start the backend server (it should be running on port 8504)

4. Run the frontend application:
   ```bash
   # Navigate to the frontend directory
   cd frontend

   # Run the Streamlit app
   streamlit run app.py
   ```

5. The application will open in your default web browser at `http://localhost:8501`

## Important Notes

- Make sure the backend server is running on port 8504 before starting the frontend
- The application requires both frontend and backend to be running simultaneously
- You can register as either a CUSTOMER or ADMIN user
- The backend server must be accessible at `http://localhost:8504/api`

## Troubleshooting

If you encounter any issues:
1. Ensure both frontend and backend servers are running
2. Check if all required packages are installed
3. Verify that the backend server is running on port 8504
4. Make sure you have proper internet connectivity

## Support

If you encounter any issues, please contact the development team for support. 