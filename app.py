# app.py

import streamlit as st
from products_data import vendors

st.set_page_config(page_title="Cop N' Shop", page_icon="🚓", layout="wide")

# Initialize cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(product):
    st.session_state.cart.append(product)
    st.success(f"Added {product['name']} to cart!")

# Set page configuration
# st.set_page_config(page_title="Marketplace", layout="wide")

# Header
st.title("Marketplace")
st.sidebar.header("Cart")
st.sidebar.write("Products in Cart: ", len(st.session_state.cart))

# Display cart items
if st.session_state.cart:
    st.sidebar.subheader("Cart Items")
    for item in st.session_state.cart:
        st.sidebar.write(f"{item['name']} - ${item['price']:.2f}")

# Main section to display vendors and products
for vendor in vendors:
    st.subheader(vendor["name"])
    for product in vendor["products"]:
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.image(product["image"], use_column_width=True)
        with col2:
            st.write(f"**{product['name']}**")
            st.write(f"Price: ${product['price']:.2f}")
        with col3:
            if st.button("Add to Cart", key=product["id"]):
                add_to_cart(product)

# Optionally, you can display the cart contents directly in the sidebar
if st.session_state.cart:
    st.sidebar.subheader("Cart Summary")
    total_price = sum(item['price'] for item in st.session_state.cart)
    st.sidebar.write(f"Total: ${total_price:.2f}")
