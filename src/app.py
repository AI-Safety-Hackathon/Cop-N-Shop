# # app.py

# import streamlit as st
# import json
# import os

# st.set_page_config(page_title="Cop N' Shop", page_icon="🚓", layout="wide")

# # Load vendors and products from JSON files
# def load_data():
#     # Load vendor data
#     with open(os.path.join('db', 'vendor_data.json')) as f:
#         vendor_data = json.load(f)

#     # Load product data
#     with open(os.path.join('db', 'updated_product_data.json')) as f:
#         product_data = json.load(f)

#     # Combine vendor data with products
#     vendors = []
#     for vendor in vendor_data['vendors']:
#         vendor_id = int(vendor['vendor_id'])
#         # Filter products by vendor_id
#         products = [product for product in product_data if product['vendor_id'] == vendor_id]
#         vendors.append({
#             'id': vendor_id,
#             'name': vendor['vendor_name'],
#             'products': products
#         })
    
#     return vendors

# # Load data
# vendors = load_data()

# # Initialize cart
# if 'cart' not in st.session_state:
#     st.session_state.cart = []

# def add_to_cart(product):
#     st.session_state.cart.append(product)
#     st.success(f"Added {product['product_name']} to cart!")
#     # Call function to update the sidebar cart immediately
#     update_cart_summary()

# def update_cart_summary():
#     # Clear previous sidebar content
#     st.sidebar.empty()  # <-- Added to clear previous content
    
#     st.sidebar.header("Cart")  # <-- Moved this line here to re-add the header after clearing
    
#     # Display current cart items
#     st.sidebar.write("Products in Cart: ", len(st.session_state.cart))
#     if st.session_state.cart:
#         st.sidebar.subheader("Cart Items")
#         for item in st.session_state.cart:
#             st.sidebar.write(f"{item['product_name']} - ${item['original_price']:.2f}")
        
#         # Display total price in the sidebar
#         total_price = sum(item['original_price'] for item in st.session_state.cart)
#         st.sidebar.subheader("Cart Summary")
#         st.sidebar.write(f"Total: ${total_price:.2f}")

# # Header
# st.title("Cop N' Shop Marketplace")
# st.sidebar.header("Cart")
# update_cart_summary()  # Update sidebar initially

# # Main section to display vendors and products
# for vendor in vendors:
#     st.subheader(vendor["name"])
#     for product in vendor["products"]:
#         col1, col2, col3 = st.columns([2, 3, 1])
#         with col1:
#             st.image(product.get("image", "./images/placeholder.jpeg"), width=100, use_column_width=False)  # Reduced image size
#         with col2:
#             st.write(f"**{product['product_name']}**")
#             st.write(f"Price: ${product['original_price']:.2f}")
#             st.write(f"Brand: {product['product_brand']}")
#             st.write(f"OS: {product['product_os']}")
#             st.write(product['product_description'])
#         with col3:
#             if st.button("Add to Cart", key=product["product_id"]):
#                 add_to_cart(product)

# # Update the cart summary again at the end
# update_cart_summary()

# app.py

import streamlit as st
import json
import os

st.set_page_config(page_title="Cop N' Shop", page_icon="🚓", layout="wide")

# Load vendors and products from JSON files
def load_data():
    # Load vendor data
    with open(os.path.join('db', 'vendor_data.json')) as f:
        vendor_data = json.load(f)

    # Load product data
    with open(os.path.join('db', 'updated_product_data.json')) as f:
        product_data = json.load(f)

    # Combine vendor data with products
    vendors = []
    for vendor in vendor_data['vendors']:
        vendor_id = int(vendor['vendor_id'])
        # Filter products by vendor_id
        products = [product for product in product_data if product['vendor_id'] == vendor_id]
        vendors.append({
            'id': vendor_id,
            'name': vendor['vendor_name'],
            'products': products
        })
    
    return vendors

# Load data
vendors = load_data()

# Initialize session state for cart and total
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'total' not in st.session_state:
    st.session_state.total = 0

def add_to_cart(product):
    """Add the selected product to the cart."""
    product_id = product["product_id"]
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += 1  # Increment quantity
    else:
        st.session_state.cart[product_id] = 1  # Add new product
    st.session_state.total += product["original_price"]  # Update total
    st.success(f"Added {product['product_name']} to cart!")

# Header
st.title("Cop N' Shop Marketplace")

# Create two columns: one for products and one for the cart
col1, col2 = st.columns([3, 1])

with col1:
    # Main section to display vendors and products
    for vendor in vendors:
        st.subheader(vendor["name"])
        for product in vendor["products"]:
            col3, col4, col5 = st.columns([2, 3, 1])
            with col3:
                st.image(product.get("image", "./images/placeholder.jpeg"), width=100, use_column_width=False)  # Reduced image size
            with col4:
                st.write(f"**{product['product_name']}**")
                st.write(f"Price: ${product['original_price']:.2f}")
                st.write(f"Brand: {product['product_brand']}")
                st.write(f"OS: {product['product_os']}")
                st.write(product['product_description'])
            with col5:
                if st.button("Add to Cart", key=product["product_id"]):
                    add_to_cart(product)

with col2:
    # Cart column
    st.subheader("Your Cart")
    
    with st.expander("View Cart", expanded=False):
        if st.session_state.cart:
            for product_id, quantity in st.session_state.cart.items():
                # Find product details from the vendors data
                product_name = next((p["product_name"] for v in vendors for p in v["products"] if p["product_id"] == product_id), "Unknown")
                product_price = next((p["original_price"] for v in vendors for p in v["products"] if p["product_id"] == product_id), 0)
                st.write(f"{product_name} x {quantity} = ${product_price * quantity:.2f}")
            st.write(f"**Total: ${st.session_state.total:.2f}**")
        else:
            st.write("Your cart is empty.")

