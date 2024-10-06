# app.py

import streamlit as st
import json
import os

st.set_page_config(page_title="Cop N' Shop", page_icon="🚓", layout="wide", initial_sidebar_state='collapsed')

# Load vendors and products from JSON files
def load_data():
    # Load vendor data
    with open(os.path.join('db', 'vendor_data.json')) as f:
        vendor_data = json.load(f)

    # Load product data
    with open(os.path.join('db', 'product_data.json')) as f:
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
            'rating':vendor['vendor_rating'],
            'nature':vendor['vendor_nature'],
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
    id = product["id"]
    if id in st.session_state.cart:
        st.session_state.cart[id] += 1  # Increment quantity
    else:
        st.session_state.cart[id] = 1  # Add new product
    st.session_state.total += product["original_price"]  # Update total
    st.success(f"Added {product['name']} to cart!")

# Header
st.title("Cop N' Shop Marketplace")

# Create two columns: one for products and one for the cart
col1, col2 = st.columns([3, 1])

with col1:
    # Main section to display vendors and products
    for vendor in vendors:
        st.subheader(vendor["name"])
        if st.button(f"Talk with {vendor['name']}"):
            if 'vendor' not in st.session_state: 
                st.session_state.vendor = ""
            st.session_state.vendor = vendor
            st.switch_page("pages/vendor_chat.py")
        st.write(f"Rating: {vendor['rating']} ⭐")
        for product in vendor["products"][:3]:
            col3, col4, col5 = st.columns([2, 3, 1])
            with col3:
                st.image(product.get("image", os.path.join('images', 'placeholder.jpeg')), width=100, use_column_width=False)  # Reduced image size
            with col4:
                # st.write(f"**{product['name']}**")
                st.markdown(f"<h3 style='font-size: 24px;'>{product['name']}</h3>", unsafe_allow_html=True) 
                st.write(f"Price: ${product['original_price']:.2f}")
                st.write(f"Brand: {product['brand']}")
                st.write(f"OS: {product['os']}")
                st.write(product['description'])
            with col5:
                if st.button("Add to Cart", key=product["id"]):
                    add_to_cart(product)

with col2:
    # Cart column
    st.subheader("Your Cart")
    
    if st.button("Proceed to Checkout"): 
        st.switch_page("pages/checkout.py")
    
    with st.expander(f"View Cart - ({len(st.session_state.cart.items())}) - $**{st.session_state.total:.2f}**", expanded=False):
        if st.session_state.cart:
            for id, quantity in st.session_state.cart.items():
                # Find product details from the vendors data
                name = next((p["name"] for v in vendors for p in v["products"] if p["id"] == id), "Unknown")
                product_price = next((p["original_price"] for v in vendors for p in v["products"] if p["id"] == id), 0)
                st.write(f"{name} x {quantity} = ${product_price * quantity:.2f}")
            st.write(f"**Total: ${st.session_state.total:.2f}**")
        else:
            st.write("Your cart is empty.")
