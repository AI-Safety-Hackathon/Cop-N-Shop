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

# Initialize cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(product):
    st.session_state.cart.append(product)
    st.success(f"Added {product['product_name']} to cart!")

# Header
st.title("Cop N' Shop Marketplace")
st.sidebar.header("Cart")
st.sidebar.write("Products in Cart: ", len(st.session_state.cart))

# Display cart items
if st.session_state.cart:
    st.sidebar.subheader("Cart Items")
    for item in st.session_state.cart:
        st.sidebar.write(f"{item['product_name']} - ${item['original_price']:.2f}")

# Main section to display vendors and products
if st.button("Checkout"): 
    st.switch_page("pages/checkout.py")

for vendor in vendors:
    st.subheader(vendor["name"])
    for product in vendor["products"]:
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.image(product.get("image", "./images/placeholder.jpeg"), use_column_width=True)  # Placeholder if no image is provided
        with col2:
            st.write(f"**{product['product_name']}**")
            st.write(f"Price: ${product['original_price']:.2f}")
            st.write(f"Brand: {product['product_brand']}")
            st.write(f"OS: {product['product_os']}")
            st.write(product['product_description'])
        with col3:
            if st.button("Add to Cart", key=product["product_id"]):
                add_to_cart(product)

# Optionally, you can display the cart contents directly in the sidebar
if st.session_state.cart:
    st.sidebar.subheader("Cart Summary")
    total_price = sum(item['original_price'] for item in st.session_state.cart)
    st.sidebar.write(f"Total: ${total_price:.2f}")
