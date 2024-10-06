import streamlit as st
from app import vendors
from agents.police_agent import agent

def check_cart_for_malicious_items(cart, vendors):
    """Check each product in the cart using the AI agent and return any warnings."""
    warnings = []
    for id, quantity in cart.items():
        product_name = next((p["name"] for v in vendors
                             for p in v["products"] if p["id"] == id), "Unknown")
        
        agent_response = agent.run(f"Check for scams for {product_name} and think step by step before taking action."
                                   f"If a scam is detected, give a final answer in this format: Scam: 'your answer'")
        print(agent_response)

        if any(phrase in agent_response for phrase in ["Scam"]):
            warnings.append(agent_response)
    
    return warnings


# Empty cart redirect, force people to shop and grab products
if 'cart' not in st.session_state:
    st.switch_page("app.py")

# Load page
st.title("Cop N' Shop Marketplace")

col1, col2 = st.columns([3, 1])
with col1:
    back_btn = st.button("Back to Products")
with col2: 
    checkout_btn = st.button("Proceed to Billing", type="primary")

# # Button Logic
# if back_btn:
#     st.switch_page("app.py")
# if checkout_btn:
#     #do something
#     st.switch_page("pages/conclusion.py")



st.header("Cart Items")
if st.session_state.cart:
    for id, quantity in st.session_state.cart.items():
        name = next((p["name"] for v in vendors for p in v["products"] if p["id"] == id), "Unknown")
        product_price = next((p["original_price"] for v in vendors for p in v["products"] if p["id"] == id), 0)
        st.write(f"{name} x {quantity} = ${product_price * quantity:.2f}")
    st.subheader("Cart Summary")
    total_price = st.session_state.total
    st.write(f"Total: ${total_price:.2f}")
    
    if checkout_btn:
        st.subheader("Agent's Report")
        warnings = check_cart_for_malicious_items(st.session_state.cart, vendors)

        if warnings:
            for warning in warnings:
                st.write(warning)
            st.error("Some items have been flagged as potentially malicious:")
        else:
            st.success("All products in the cart are safe. You may proceed with checkout.")
else:
    st.write("No products added.")
proceed_btn = st.button('Proceed to checkout')
    

if back_btn:
    st.switch_page("app.py")
if proceed_btn:
    #do something
    st.switch_page("pages/conclusion.py")
# Checkout Page Logic
