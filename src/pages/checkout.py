import streamlit as st
from app import vendors

# Empty cart redirect, force people to shop and grab products
if 'cart' not in st.session_state:
    st.switch_page("app.py")

# Load page
st.title("Cop N' Shop Marketplace")

col1, col2 = st.columns(2)
with col1:
    back_btn = st.button("Back to Products")
with col2: 
    checkout_btn = st.button("Proceed to Billing", type="primary")

# Button Logic
if back_btn:
    st.switch_page("app.py")
if checkout_btn:
    #do something
    st.switch_page("pages/conclusion.py")



st.header("Cart Items")
if st.session_state.cart:
    for id, quantity in st.session_state.cart.items():
        name = next((p["name"] for v in vendors for p in v["products"] if p["id"] == id), "Unknown")
        product_price = next((p["original_price"] for v in vendors for p in v["products"] if p["id"] == id), 0)
        st.write(f"{name} x {quantity} = ${product_price * quantity:.2f}")
    st.subheader("Cart Summary")
    total_price = st.session_state.total
    st.write(f"Total: ${total_price:.2f}")
else:
    st.write("No products added.")
