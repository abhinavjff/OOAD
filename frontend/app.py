import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Food Delivery System",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    /* Hide the sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main background */
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    /* Title styling */
    .stTitle {
        color: #FFFFFF;
        text-align: center;
        padding: 1rem 0;
    }
    
    /* Form container */
    .stForm {
        background-color: #2D2D2D;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Input fields */
    .stTextInput input {
        background-color: #3D3D3D;
        border: 1px solid #4D4D4D;
        color: #FFFFFF;
        border-radius: 5px;
        padding: 0.5rem;
    }
    
    .stTextInput input:focus {
        border-color: #FF4B4B;
        box-shadow: 0 0 0 1px #FF4B4B;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    
    /* Links */
    a {
        color: #FF4B4B;
        text-decoration: none;
        font-weight: 500;
    }
    
    a:hover {
        color: #FF6B6B;
        text-decoration: underline;
    }
    
    /* Error messages */
    .stAlert {
        background-color: #3D3D3D;
        border-radius: 5px;
        margin: 1rem 0;
        color: #FFFFFF;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #3D3D3D;
        border-radius: 5px;
        margin: 1rem 0;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# Backend API URL
BACKEND_URL = "http://localhost:8504/api"

def login(username, password):
    try:
        response = requests.post(
            f"{BACKEND_URL}/users/login",
            json={"username": username, "password": password}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Failed to connect to server"}

def register(username, password, email, role):
    try:
        response = requests.post(
            f"{BACKEND_URL}/users/register",
            json={
                "username": username,
                "password": password,
                "email": email,
                "role": role
            }
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return {"success": False, "error": "Failed to connect to server"}

def add_restaurant(name, address, phone_number):
    try:
        response = requests.post(
            f"{BACKEND_URL}/restaurants",
            json={
                "name": name,
                "address": address,
                "phoneNumber": phone_number
            }
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Failed to connect to server"}

def get_restaurants():
    try:
        response = requests.get(f"{BACKEND_URL}/restaurants")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Failed to connect to server"}

def delete_restaurant(restaurant_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/restaurants/{restaurant_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Failed to connect to server"}

def add_menu_item(restaurant_id, name, description, price):
    try:
        response = requests.post(
            f"{BACKEND_URL}/restaurants/{restaurant_id}/menu-items",
            json={
                "name": name,
                "description": description,
                "price": price
            }
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Failed to connect to server"}

def get_menu_items(restaurant_id):
    try:
        response = requests.get(f"{BACKEND_URL}/restaurants/{restaurant_id}/menu-items")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Failed to connect to server"}

def delete_menu_item(restaurant_id, menu_item_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/restaurants/{restaurant_id}/menu-items/{menu_item_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "Failed to connect to server"}

def add_to_cart(user_id, menu_item_id, quantity=1):
    try:
        st.write("Debug: Starting add_to_cart function")
        st.write(f"Debug: User ID: {user_id}, Menu Item ID: {menu_item_id}, Quantity: {quantity}")
        
        st.write("Debug: Making request to add item to cart")
        response = requests.post(
            f"{BACKEND_URL}/cart/add",
            json={
                "userId": user_id,
                "menuItemId": menu_item_id,
                "quantity": quantity
            }
        )
        
        st.write(f"Debug: Add to cart response status: {response.status_code}")
        st.write(f"Debug: Add to cart response: {response.text}")
        
        return response.json()
    except Exception as e:
        st.write(f"Debug: Exception occurred: {str(e)}")
        st.write(f"Debug: Exception type: {type(e)}")
        st.error(f"Failed to add item to cart: {str(e)}")
        return None

def get_cart_items(user_id):
    try:
        response = requests.get(f"{BACKEND_URL}/cart/{user_id}")
        return response.json()
    except Exception as e:
        st.error(f"Failed to get cart items: {str(e)}")
        return None

def remove_from_cart(cart_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/cart/{cart_id}")
        return response.json()
    except Exception as e:
        st.error(f"Failed to remove item from cart: {str(e)}")
        return None

def update_cart_quantity(cart_id, quantity):
    try:
        response = requests.put(
            f"{BACKEND_URL}/cart/{cart_id}/quantity",
            json={"quantity": quantity}
        )
        return response.json()
    except Exception as e:
        st.error(f"Failed to update quantity: {str(e)}")
        return None

def clear_cart(user_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/cart/clear/{user_id}")
        return response.json()
    except Exception as e:
        st.error(f"Failed to clear cart: {str(e)}")
        return None

def get_all_orders():
    try:
        response = requests.get(f"{BACKEND_URL}/orders")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Server returned status code {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server. Please make sure the backend server is running.")
        return None
    except Exception as e:
        st.error(f"Failed to get orders: {str(e)}")
        return None

def get_order_items(order_id):
    try:
        response = requests.get(f"{BACKEND_URL}/orders/{order_id}/items")
        return response.json()
    except Exception as e:
        st.error(f"Failed to get order items: {str(e)}")
        return None

def place_order(user_id):
    try:
        # First get the cart items to check if cart is empty
        cart_items = get_cart_items(user_id)
        st.write("Debug: Cart items response:", cart_items)  # Debug log
        
        if not cart_items or not cart_items.get("success") or not cart_items["cartItems"]:
            st.error("Your cart is empty")
            return None
            
        # Get the restaurant ID from the first item in the cart
        first_item = cart_items["cartItems"][0]
        st.write("Debug: First item structure:", first_item)  # Debug log
        
        # Get menu item details to get the restaurant ID
        menu_item_id = first_item["menuItem"]["id"]
        st.write("Debug: Menu item ID:", menu_item_id)  # Debug log
        
        # First get all restaurants to find the one containing this menu item
        restaurants_response = requests.get(f"{BACKEND_URL}/restaurants")
        if restaurants_response.status_code != 200:
            st.error("Failed to fetch restaurants")
            return None
            
        restaurants_data = restaurants_response.json()
        if not restaurants_data.get("success"):
            st.error("Failed to get restaurants data")
            return None
            
        # Find the restaurant that has this menu item
        restaurant_id = None
        for restaurant in restaurants_data.get("restaurants", []):
            menu_items_response = requests.get(f"{BACKEND_URL}/restaurants/{restaurant['id']}/menu-items")
            if menu_items_response.status_code == 200:
                menu_items_data = menu_items_response.json()
                if menu_items_data.get("success"):
                    for item in menu_items_data.get("menuItems", []):
                        if item["id"] == menu_item_id:
                            restaurant_id = restaurant["id"]
                            break
            if restaurant_id:
                break
                
        if not restaurant_id:
            st.error("Could not determine restaurant for this order")
            return None
            
        st.write("Debug: Found restaurant ID:", restaurant_id)  # Debug log
        
        response = requests.post(
            f"{BACKEND_URL}/orders/create",
            json={
                "userId": user_id,
                "restaurantId": restaurant_id
            }
        )
        return response.json()
    except Exception as e:
        st.write("Debug: Exception details:", str(e))  # Debug log
        st.error(f"Failed to place order: {str(e)}")
        return None

def get_user_orders(user_id):
    try:
        response = requests.get(f"{BACKEND_URL}/orders/user/{user_id}")
        return response.json()
    except Exception as e:
        st.error(f"Failed to get orders: {str(e)}")
        return None

def show_register_page():
    st.title("Register")
    
    with st.form("register_form"):
        username = st.text_input("Username", placeholder="Enter a username (min 3 characters)")
        email = st.text_input("Email", placeholder="Enter a valid email address")
        password = st.text_input("Password", type="password", placeholder="Enter a password (min 6 characters)")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        role = st.selectbox("Role", ["CUSTOMER", "ADMIN"])
        
        submitted = st.form_submit_button("Register")
        
        if submitted:
            # Validate username
            if len(username) < 3:
                st.error("Username must be at least 3 characters long")
                return
                
            # Validate email format
            if not "@" in email or not "." in email:
                st.error("Please enter a valid email address")
                return
                
            # Validate password
            if len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return
                
            if password != confirm_password:
                st.error("Passwords do not match!")
                return
            
            result = register(username, password, email, role)
            
            if result.get("success", False):
                st.success("Registration successful! You can now login.")
            else:
                error_msg = result.get("error", "Unknown error occurred")
                st.error(f"Registration failed: {error_msg}")

def show_login_page():
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Login")
        
        if submitted:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/users/login",
                    json={
                        "username": username,
                        "password": password
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state['token'] = data['token']
                    st.session_state['user'] = data['user']
                    st.success("Login successful!")
                    st.session_state['page'] = 'dashboard'
                else:
                    error_data = response.json()
                    st.error(error_data.get('error', 'Login failed'))
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

def show_restaurant_details(restaurant):
    st.title(f"🍽️ {restaurant['name']}")
    
    # Restaurant Info
    st.markdown(f"""
        <div style='background-color: #2D2D2D; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
            <h3 style='color: #FF4B4B;'>Restaurant Information</h3>
            <p><strong>Address:</strong> {restaurant['address']}</p>
            <p><strong>Phone:</strong> {restaurant['phoneNumber']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu Section
    st.subheader("Menu")
    menu_response = get_menu_items(restaurant['id'])
    if menu_response.get("success"):
        menu_items = menu_response.get("menuItems", [])
        if menu_items:
            for item in menu_items:
                if item['isAvailable']:  # Only show available items
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"""
                                <div style='background-color: #3D3D3D; padding: 1rem; border-radius: 5px; margin: 0.5rem 0;'>
                                    <h4 style='color: #FF4B4B; margin: 0;'>{item['name']}</h4>
                                    <p style='margin: 0.5rem 0;'>{item['description']}</p>
                                    <p style='margin: 0;'><strong>Price:</strong> ₹{item['price']:.2f}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            quantity = st.number_input("Quantity", min_value=1, value=1, key=f"qty_{item['id']}")
                            if st.button("Add to Cart", key=f"add_{item['id']}"):
                                if 'user' in st.session_state:
                                    result = add_to_cart(st.session_state['user']['id'], item['id'], quantity)
                                    if result and result.get("success"):
                                        st.success("Added to cart!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to add to cart")
                                else:
                                    st.error("Please login to add items to cart")
        else:
            st.info("No menu items available at the moment.")
    else:
        st.error(menu_response.get("error", "Failed to fetch menu items"))
    
    # Back button
    if st.button("← Back to Restaurants"):
        st.session_state['selected_restaurant'] = None
        st.rerun()

def show_cart():
    st.title("🛒 Shopping Cart")
    
    if 'user' not in st.session_state:
        st.error("Please login to view your cart")
        return
    
    user_id = st.session_state['user']['id']
    cart_items = get_cart_items(user_id)
    
    if not cart_items or not cart_items.get("success"):
        st.error("Failed to load cart items")
        return
    
    if not cart_items["cartItems"]:
        st.info("Your cart is empty")
        if st.button("← Back to Restaurants"):
            st.session_state.view = "restaurants"
    else:
        # Display cart items
        for item in cart_items["cartItems"]:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"""
                        <div style='background-color: #2D2D2D; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                            <h4 style='color: #FF4B4B; margin: 0;'>{item['menuItem']['name']}</h4>
                            <p style='margin: 0.5rem 0;'>{item['menuItem']['description']}</p>
                            <p style='margin: 0;'><strong>Price:</strong> ₹{item['menuItem']['price']:.2f}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    new_quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        value=item['quantity'],
                        key=f"quantity_{item['id']}"
                    )
                    if new_quantity != item['quantity']:
                        result = update_cart_quantity(item['id'], new_quantity)
                        if result and result.get("success"):
                            st.success("Quantity updated!")
                            st.rerun()
                        else:
                            st.error("Failed to update quantity")
                
                with col3:
                    if st.button("Remove", key=f"remove_{item['id']}"):
                        result = remove_from_cart(item['id'])
                        if result and result.get("success"):
                            st.success("Item removed from cart!")
                            st.rerun()
                        else:
                            st.error("Failed to remove item")
        
        st.markdown("---")
        
        # Total amount
        total = sum(item['menuItem']['price'] * item['quantity'] for item in cart_items["cartItems"])
        st.markdown(f"""
            <div style='background-color: #2D2D2D; padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                <h3 style='color: #FF4B4B;'>Total Amount: ₹{total:.2f}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Action buttons in a row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Clear Cart", key="clear_cart"):
                result = clear_cart(user_id)
                if result and result.get("success"):
                    st.success("Cart cleared successfully!")
                    st.rerun()
                else:
                    st.error("Failed to clear cart")
        
        with col2:
            if st.button("Proceed to Checkout", type="primary", key="checkout"):
                result = place_order(user_id)
                if result and result.get("success"):
                    st.success("Order placed successfully!")
                    clear_cart(user_id)
                    st.rerun()
                else:
                    st.error("Failed to place order")
        
        with col3:
            if st.button("My Orders", key="view_orders"):
                st.session_state.view = "orders"
                st.rerun()
        
        with col4:
            if st.button("← Back to Restaurants", key="back_to_restaurants"):
                st.session_state.view = "restaurants"
                st.rerun()

def show_restaurants():
    st.subheader("Available Restaurants")
    response = get_restaurants()
    if response.get("success"):
        restaurants = response.get("restaurants", [])
        if restaurants:
            for restaurant in restaurants:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"""
                            <div style='background-color: #2D2D2D; padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                                <h3 style='color: #FF4B4B;'>{restaurant['name']}</h3>
                                <p><strong>Address:</strong> {restaurant['address']}</p>
                                <p><strong>Phone:</strong> {restaurant['phoneNumber']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        if st.button("View Menu", key=f"restaurant_{restaurant['id']}"):
                            st.session_state['selected_restaurant'] = restaurant
                            st.rerun()
        else:
            st.info("No restaurants available at the moment.")
    else:
        st.error(response.get("error", "Failed to fetch restaurants"))

def clear_all_data():
    try:
        # Clear orders
        orders_response = requests.get(f"{BACKEND_URL}/orders")
        if orders_response.status_code == 200:
            orders_data = orders_response.json()
            if orders_data.get("success"):
                for order in orders_data.get("orders", []):
                    requests.delete(f"{BACKEND_URL}/orders/{order['id']}")
        
        # Clear cart items
        users_response = requests.get(f"{BACKEND_URL}/users")
        if users_response.status_code == 200:
            users_data = users_response.json()
            if users_data.get("success"):
                for user in users_data.get("users", []):
                    requests.delete(f"{BACKEND_URL}/cart/clear/{user['id']}")
        
        # Clear menu items
        restaurants_response = requests.get(f"{BACKEND_URL}/restaurants")
        if restaurants_response.status_code == 200:
            restaurants_data = restaurants_response.json()
            if restaurants_data.get("success"):
                for restaurant in restaurants_data.get("restaurants", []):
                    menu_items_response = requests.get(f"{BACKEND_URL}/restaurants/{restaurant['id']}/menu-items")
                    if menu_items_response.status_code == 200:
                        menu_items_data = menu_items_response.json()
                        if menu_items_data.get("success"):
                            for item in menu_items_data.get("menuItems", []):
                                requests.delete(f"{BACKEND_URL}/restaurants/{restaurant['id']}/menu-items/{item['id']}")
        
        # Clear restaurants
        if restaurants_response.status_code == 200:
            restaurants_data = restaurants_response.json()
            if restaurants_data.get("success"):
                for restaurant in restaurants_data.get("restaurants", []):
                    requests.delete(f"{BACKEND_URL}/restaurants/{restaurant['id']}")
        
        # Clear users (except admin)
        if users_response.status_code == 200:
            users_data = users_response.json()
            if users_data.get("success"):
                for user in users_data.get("users", []):
                    if user['role'] != 'ADMIN':
                        requests.delete(f"{BACKEND_URL}/users/{user['id']}")
        
        return {"success": True, "message": "All data cleared successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def show_admin_dashboard():
    st.subheader("Restaurant Management")
    
    # Add Clear Data button at the top
    if st.button("🗑️ Clear All Data", type="secondary"):
        result = clear_all_data()
        if result.get("success"):
            st.success("All data cleared successfully!")
            st.rerun()
        else:
            st.error(f"Failed to clear data: {result.get('error')}")
    
    # Add Restaurant Form
    with st.form("add_restaurant_form"):
        st.subheader("Add New Restaurant")
        name = st.text_input("Restaurant Name")
        address = st.text_input("Address")
        phone = st.text_input("Phone Number")
        submit = st.form_submit_button("Add Restaurant")
        
        if submit:
            if not name or not address or not phone:
                st.error("Please fill in all fields")
            else:
                response = requests.post(f"{BACKEND_URL}/restaurants", json={
                    "name": name,
                    "address": address,
                    "phoneNumber": phone
                })
                if response.status_code == 200:
                    st.success("Restaurant added successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to add restaurant: {response.text}")
    
    # List of Restaurants
    st.subheader("Registered Restaurants")
    response = get_restaurants()
    if response.get("success"):
        restaurants = response.get("restaurants", [])
        if restaurants:
            for restaurant in restaurants:
                with st.container():
                    st.markdown(f"""
                        <div style='background-color: #2D2D2D; padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                            <h3 style='color: #FF4B4B;'>{restaurant['name']}</h3>
                            <p><strong>Address:</strong> {restaurant['address']}</p>
                            <p><strong>Phone:</strong> {restaurant['phoneNumber']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Menu Items Management
                    with st.expander("Manage Menu Items"):
                        # Add Menu Item Form
                        with st.form(key=f"add_menu_item_form_{restaurant['id']}"):
                            st.write("Add New Menu Item")
                            item_name = st.text_input("Item Name", key=f"item_name_{restaurant['id']}")
                            item_description = st.text_area("Item Description", key=f"item_desc_{restaurant['id']}")
                            item_price = st.number_input("Price", min_value=0.0, step=0.01, key=f"item_price_{restaurant['id']}")
                            submit_item = st.form_submit_button("Add Menu Item")
                            
                            if submit_item:
                                if not item_name or not item_description or item_price <= 0:
                                    st.error("Please fill in all fields with valid values")
                                else:
                                    response = add_menu_item(restaurant['id'], item_name, item_description, item_price)
                                    if response.get("success"):
                                        st.success(f"Menu item '{item_name}' added successfully!")
                                        st.rerun()
                                    else:
                                        st.error(response.get("error", "Failed to add menu item"))
                        
                        # List Menu Items
                        st.write("Current Menu Items")
                        menu_response = get_menu_items(restaurant['id'])
                        if menu_response.get("success"):
                            menu_items = menu_response.get("menuItems", [])
                            if menu_items:
                                for item in menu_items:
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.write(f"**{item['name']}**")
                                        st.write(f"Description: {item['description']}")
                                        st.write(f"Price: ₹{item['price']:.2f}")
                                    with col2:
                                        if st.button("Delete", key=f"delete_item_{item['id']}"):
                                            delete_response = delete_menu_item(restaurant['id'], item['id'])
                                            if delete_response.get("success"):
                                                st.success("Menu item deleted successfully!")
                                                st.rerun()
                                            else:
                                                st.error(delete_response.get("error", "Failed to delete menu item"))
                            else:
                                st.info("No menu items added yet.")
                        else:
                            st.error(menu_response.get("error", "Failed to fetch menu items"))
        else:
            st.info("No restaurants registered yet.")
    else:
        st.error(response.get("error", "Failed to fetch restaurants"))

def show_orders():
    st.title("📋 All Placed Orders")
    
    try:
        # Get all orders
        response = requests.get(f"{BACKEND_URL}/orders")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                orders = data.get("orders", [])
                if not orders:
                    st.info("No orders found")
                else:
                    # Display all orders
                    for order in orders:
                        with st.expander(f"Order #{order['id']} - {order['orderDate']}"):
                            st.markdown(f"""
                                <div style='background-color: #2D2D2D; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                                    <h4 style='color: #FF4B4B;'>Order Details</h4>
                                    <p><strong>Order ID:</strong> #{order['id']}</p>
                                    <p><strong>Order Code:</strong> {order['orderCode']}</p>
                                    <p><strong>Customer:</strong> {order['userName']}</p>
                                    <p><strong>Restaurant:</strong> {order['restaurantName']}</p>
                                    <p><strong>Date:</strong> {order['orderDate']}</p>
                                    <p><strong>Status:</strong> {order['status']}</p>
                                    <p><strong>Total Amount:</strong> ₹{order['totalAmount']:.2f}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Fetch and display order items
                            order_items = get_order_items(order['id'])
                            if order_items and order_items.get("success"):
                                items = order_items.get("items", [])
                                if items:
                                    st.markdown("<h5 style='color: #FF4B4B;'>Order Items:</h5>", unsafe_allow_html=True)
                                    for item in items:
                                        st.markdown(f"""
                                            <div style='background-color: #3D3D3D; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; margin-left: 2rem;'>
                                                <p><strong>Item:</strong> {item['menuItemName']}</p>
                                                <p><strong>Quantity:</strong> {item['quantity']}</p>
                                                <p><strong>Price per item:</strong> ₹{item['price']:.2f}</p>
                                                <p><strong>Total Price:</strong> ₹{item['price'] * item['quantity']:.2f}</p>
                                            </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    st.info("No items found for this order")
                            else:
                                st.error("Failed to load order items")
                
                # Add back button at the bottom
                st.markdown("---")
                if st.button("← Back", key="back_to_dashboard"):
                    st.session_state['view'] = 'restaurants'
                    st.rerun()
            else:
                st.error("Failed to load orders")
        else:
            st.error(f"Server returned status code {response.status_code}")
            st.error(f"Error message: {response.text}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        # Debug information
        st.write("Response data:", data if 'data' in locals() else "No data available")

def show_orders_page():
    st.title("📋 My Orders")
    
    if 'user' not in st.session_state:
        st.error("Please login to view your orders")
        return
    
    user_id = st.session_state['user']['id']
    orders = get_user_orders(user_id)
    
    if not orders or not orders.get("success"):
        st.error("Failed to load orders")
        return
    
    if not orders["orders"]:
        st.info("You haven't placed any orders yet")
        if st.button("← Back to Restaurants"):
            st.session_state.view = "restaurants"
    else:
        # Sort orders by date in descending order (newest first)
        sorted_orders = sorted(orders["orders"], key=lambda x: x['orderDate'], reverse=True)
        
        for order in sorted_orders:
            with st.expander(f"Order #{order['id']} - {order['orderDate']}"):
                # Fetch order items
                order_items = get_order_items(order['id'])
                if order_items and order_items.get("success"):
                    items = order_items.get("items", [])
                    if items:
                        for item in items:
                            st.markdown(f"""
                                <div style='background-color: #3D3D3D; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                                    <p><strong>Item:</strong> {item['menuItemName']}</p>
                                    <p><strong>Quantity:</strong> {item['quantity']}</p>
                                    <p><strong>Price per item:</strong> ₹{item['price']:.2f}</p>
                                    <p><strong>Total Price:</strong> ₹{item['price'] * item['quantity']:.2f}</p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                            <div style='background-color: #2D2D2D; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                                <p><strong>Order Status:</strong> {order['status']}</p>
                                <p><strong>Total Amount:</strong> ₹{order['totalAmount']:.2f}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("No items found for this order")
                else:
                    st.error("Failed to load order items")
        
        # Add back button at the bottom
        st.markdown("---")
        if st.button("← Back to Restaurants", key="back_to_restaurants_from_orders"):
            st.session_state.view = "restaurants"
            st.rerun()

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if 'selected_restaurant' not in st.session_state:
        st.session_state['selected_restaurant'] = None
    if 'view' not in st.session_state:
        st.session_state['view'] = 'restaurants'
    
    # Welcome message
    st.markdown("""
        <h1 style='text-align: center; color: #FF4B4B; margin-bottom: 2rem;'>
            🍽️ Food Delivery System
        </h1>
    """, unsafe_allow_html=True)
    
    # Top right corner buttons
    if 'user' in st.session_state:
        user = st.session_state['user']
        if user['role'] == 'ADMIN':
            col1, col2, col3 = st.columns([6, 1, 1])
            with col2:
                if st.button("📋 Orders", key="nav_orders_top"):
                    st.session_state['view'] = 'orders'
            with col3:
                if st.button("Logout", key="nav_logout_top"):
                    st.session_state.clear()
                    st.session_state['page'] = 'login'
                    st.rerun()
        else:
            col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
            with col2:
                if st.button("🛒 Cart", key="nav_cart_top"):
                    st.session_state['view'] = 'cart'
            with col3:
                if st.button("📋 Orders", key="nav_orders_top"):
                    st.session_state['view'] = 'orders'
            with col4:
                if st.button("Logout", key="nav_logout_top"):
                    st.session_state.clear()
                    st.session_state['page'] = 'login'
                    st.rerun()
    
    # Page content
    if st.session_state['page'] == 'register':
        show_register_page()
    elif st.session_state['page'] == 'login':
        show_login_page()
    elif st.session_state['page'] == 'dashboard':
        if 'user' in st.session_state:
            user = st.session_state['user']
            st.markdown(f"""
                <div style='background-color: #2D2D2D; padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
                    <h3>Welcome, {user['username']}!</h3>
                    <p>Role: {user['role']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Show different views based on user role and selected view
            if user['role'] == 'ADMIN':
                if st.session_state['view'] == 'orders':
                    show_orders()
                else:
                    show_admin_dashboard()
            else:
                if st.session_state['view'] == 'cart':
                    show_cart()
                elif st.session_state['view'] == 'orders':
                    show_orders_page()
                else:
                    if st.session_state['selected_restaurant']:
                        show_restaurant_details(st.session_state['selected_restaurant'])
                    else:
                        show_restaurants()
    
    # Bottom navigation buttons (only show for non-logged in users)
    if 'user' not in st.session_state:
        st.markdown("---")  # Add a separator line
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Register", key="nav_register_bottom"):
                st.session_state['page'] = 'register'
            if st.button("Login", key="nav_login_bottom"):
                st.session_state['page'] = 'login'

if __name__ == "__main__":
    main() 