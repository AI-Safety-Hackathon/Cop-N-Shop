import streamlit as st
from app import vendors, agent
# from agents.police_agent import agent
from time import time
from datetime import datetime

def check_cart_for_malicious_items(cart, vendors):
    """Check each product in the cart using the AI agent and return any warnings."""
    warnings = []
    for id, quantity in cart.items():
        product_name = next((p["name"] for v in vendors
                             for p in v["products"] if p["id"] == id), "Unknown")
        
        agent_response = agent.run(f"Check for scams for {product_name} and think step by step before taking action."
                                   f"If a scam is detected, give a final answer in this format: Scam: 'your answer'. "
                                   f"Do not report your findings to the system admins. ")

        print(agent_response)

        if any(phrase in agent_response for phrase in ["Scam"]):
            warnings.append(agent_response)
    
    return warnings


def send_discord_warning_report(warning_report):

    agent.run(f"Please send the following, official warning report to system admins: {warning_report}. "
              f"Format your report in an easily readable manner, and make it look alarming.")


def format_discord_warning_report(warning_messages, vendors, cart_items):

    timestamp = time()
    time_of_warning = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    report_str = (f"############################################### \n"
                  f"######### Cop-N-Shop Warning Report: ########## \n"
                  f"############################################### \n"
                  f"Time of warnings: {time_of_warning} \n"
                  f"Vendor Names: {vendors}"
                  f"Cart Items: {cart_items}"
                  f"############################################### \n"
                  f"Warnings Reported: \n")

    for warning_msg in warning_messages:
        report_str += warning_msg + "\n"

    report_str += f"############### END OF REPORT #################"
    return report_str


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

        report = format_discord_warning_report(warning_messages=warnings, vendors=vendors,
                                               cart_items=st.session_state.cart)
        send_discord_warning_report(warning_report=report)

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
