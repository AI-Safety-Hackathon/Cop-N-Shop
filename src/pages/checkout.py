import streamlit as st

# Empty cart redirect, force people to shop and grab products
if 'cart' not in st.session_state:
    st.switch_page("app.py")

# Load page
st.title("Cop N' Shop Marketplace")

col1, col2 = st.columns(2)
with col1:
    back_btn = st.button("Back to Products")
with col2: 
    checkout_btn = st.button("Checkout", type="primary")

# Button Logic
if back_btn:
    st.switch_page("app.py")
if checkout_btn:
    #do something
    st.success(f"Hit Checkout")


st.header("Cart Items")
if st.session_state.cart:
    for item in st.session_state.cart:
        st.write(f"{item['product_name']} - ${item['original_price']:.2f}")
    st.subheader("Cart Summary")
    total_price = sum(item['original_price'] for item in st.session_state.cart)
    st.write(f"Total: ${total_price:.2f}")
else:
    st.write("No products added.")
