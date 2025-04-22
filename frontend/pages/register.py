import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Register - Food Delivery System",
    page_icon="🍽️",
    layout="centered"
)

# Backend API URL
BACKEND_URL = "http://localhost:8080/api"

def register(user_data):
    try:
        response = requests.post(
            f"{BACKEND_URL}/users/register",
            json=user_data
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Failed to connect to server"}

def main():
    st.title("🍽️ Create Account")
    
    # Create two columns for the registration form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Register")
        
        # Registration form
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                if not username or not email or not password or not confirm_password:
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    # Attempt registration
                    user_data = {
                        "username": username,
                        "email": email,
                        "password": password
                    }
                    response = register(user_data)
                    if "error" not in response:
                        st.success("Registration successful! Please login.")
                        st.session_state["registered"] = True
                        st.rerun()
                    else:
                        st.error(response.get("error", "Registration failed"))
        
        # Login link
        st.markdown("---")
        st.markdown("Already have an account? [Login here](/)")

if __name__ == "__main__":
    main() 