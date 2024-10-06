import time
import datetime
import streamlit as st
from app import vendors
from agents.police_agent import agent

# Check if the cart exists in the session state
if 'cart' not in st.session_state:
    st.switch_page("app.py")

# Initialize the cart_scanned flag if it doesn't exist
if 'cart_scanned' not in st.session_state:
    st.session_state['cart_scanned'] = False  # Set to False by default


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
        # Find the product name and price based on the id in the cart
        product_data = next((p for v in vendors for p in v["products"] if p["id"] == id), None)
        if product_data:
            product_name = product_data["name"]
            product_price = product_data.get("original_price", "Unknown Price")
        else:
            product_name = "Unknown"
            product_price = "Unknown Price"

        # Run the agent on the product
        agent_response = agent.run(f"Check if the product {product_name} priced at ${product_price} is involved in a scam. "
                                   f"Think step by step before making a decision. "
                                   f"If the product is identified as malicious or involved in a scam, "
                                   f"provide a detailed reason for why it is a scam, then give a final answer "
                                   f"in the following format: 'Scam: {product_name} priced at ${product_price} is a scam because {{detailed reason}}'. "
                                   f"If no scam is detected, simply state '{product_name} priced at ${product_price} is not a scam' "
                                   f"without using 'Scam:'.")
        
        if "Scam" in agent_response:
            warnings.append(agent_response)
    
    return warnings


def send_discord_warning_report(warning_report):

    agent.run(f"Please send the following, official warning report to system admins: {warning_report}. "
              f"Format the report in an easily readable but alarming manner")


def format_discord_warning_report(warning_messages, vendors, cart_items):

    timestamp = datetime.now()
    time_of_warning = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    report_str = (f"Time of warnings: {time_of_warning} \n"
                  f"Vendor Names: {vendors}"
                  f"Cart Items: {cart_items}"
                  f"Warnings Reported: \n")

    for warning_msg in warning_messages:
        report_str += warning_msg + "\n"

    return report_str


# Empty cart redirect, force people to shop and grab products
if 'cart' not in st.session_state:
    st.switch_page("app.py")

def display_cart_items(cart, vendors):
    """Display the items in the cart and calculate the total price."""
    st.header("Cart Items")
    total_price = 0
    if cart:
        for id, quantity in cart.items():
            name = next((p["name"] for v in vendors for p in v["products"] if p["id"] == id), "Unknown")
            product_price = next((p["original_price"] for v in vendors for p in v["products"] if p["id"] == id), 0)
            st.write(f"{name} x {quantity} = ${product_price * quantity:.2f}")
            total_price += product_price * quantity
        
        st.subheader("Cart Summary")
        st.write(f"Total: ${total_price:.2f}")
    else:
        st.write("No products added.")
    
    return total_price


def remove_suspicious_items_from_cart(cart, vendors, warnings):
    """Remove the items flagged as suspicious by the agent from the cart."""
    updated_cart = cart.copy()

    for warning in warnings:
        product_name = warning.split(" priced at")[0].replace("Scam: ", "").strip()

        product_to_remove = next((p for v in vendors for p in v["products"] if p["name"] == product_name), None)
        if product_to_remove:
            product_id = product_to_remove["id"]
    
            if product_id in updated_cart:
                del updated_cart[product_id] 

    st.session_state.cart = updated_cart
    # Reset the flag so that the cart doesn't get re-scanned
    st.session_state['cart_scanned'] = True  # Mark as scanned

def handle_suspicious_items(cart, vendors):
    """Handle the removal of suspicious items from the cart and display messages."""

    if not st.session_state['cart_scanned'] and st.session_state['warnings']:
        st.error("Some items have been flagged as potentially suspicious and will be removed from your cart.")
        
        report = format_discord_warning_report(warning_messages=st.session_state['warnings'], vendors=vendors,
                                                      cart_items=st.session_state.cart)
        send_discord_warning_report(warning_report=report)
        
        
        
        time.sleep(5) 
        
        
        
        # Remove suspicious items
        remove_suspicious_items_from_cart(cart, vendors, st.session_state['warnings'])
        st.session_state['cart_scanned'] = True
        st.rerun()

    if st.session_state['cart_scanned']:
        st.info("Your cart has been cleared from the suspicious item.")


def run_agent_on_cart(cart, vendors):
    """Run the AI agent on the cart to check for suspicious items."""
    
    if 'warnings' not in st.session_state:
        st.session_state['warnings'] = [] 

    if cart and not st.session_state['cart_scanned']:
        st.subheader("Agent's Report")
        with st.spinner("Please wait while our agent is scanning your cart for suspicious items..."):
            warnings = check_cart_for_malicious_items(cart, vendors)

            if warnings:
                st.session_state['warnings'] = warnings
                for warning in warnings:
                   st.write(warning)
            else:
                st.success("All products in the cart are safe. You may proceed with checkout.")

    elif st.session_state['cart_scanned']:
        # Show previous warnings and info that the cart was cleared
        if st.session_state['warnings']:
            st.subheader("Agent's Report")
            for warning in st.session_state['warnings']:
                st.write(warning)
        
    else:
        st.write("No products in the cart to check.")
        
        
def send_discord_warning_report(warning_report):
    response = agent.run(f"""Please send the following, official warning report to system admins: {warning_report}. 
                Format the report in an easily readable but alarming manner. 
                As an example, you can format it like this:

                🔴🔴🔴 WARNING REPORT 🔴🔴🔴 

                Cop-N-Shop Warning Report:
                🕒 Time of warnings: 1728241827.7173142 

                🛍 Vendor Names: 

                Moe's Excellent Phones
                Rating: 2.1
                Products: Infinix Hot 7, Sagem my231x, vivo U20, alcatel Miss Sixty 2009, Samsung T929 Memoir

                Jane's Phone Surplus
                Rating: 4.9
                Products: BLU Studio M HD, VK Mobile VK580, Micromax Evok Dual Note E4815, BLU Studio C HD, Lava Fuel F1, Philips 399, Samsung I9003 Galaxy SL, Lava P7, Samsung P940, Samsung Galaxy Tab 2 7.0 P3110

                Phone's R' Us
                Rating: 4.5
                Products: Samsung A257 Magnet, Prestigio MultiPad 7.0 HD +, Lenovo A830, Unnecto Eco, LG L Prime

                🛒 Cart Items: Infinix Hot 7 (1), Sagem my231x (1)

                ⚠️ Warnings Reported: 

                Scam: No
                Scam: The vendor's price for Sagem my231x is significantly lower than the market price. This could indicate a scam.

                Please investigate these vendors immediately! 💼🔍🚨
                """)
    print("RESPONSE", response)


def format_discord_warning_report(warning_messages, vendors, cart_items):

    timestamp = datetime.datetime.now()
    time_of_warning = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    report_str = (f"Time of warnings: {time_of_warning} \n"
                  f"Vendor Names: {vendors}"
                  f"Cart Items: {cart_items}"
                  f"Warnings Reported: \n")

    for warning_msg in warning_messages:
        report_str += warning_msg + "\n"

    return report_str


# Main application code
st.title("Cop N' Shop Marketplace")

# Navigation buttons
col1, col2 = st.columns([3, 1])
with col1:
    back_btn = st.button("Back to Products")
    if back_btn:
        st.session_state['cart_scanned'] = False
        st.session_state['warnings'] = []
        st.switch_page("app.py")

        if warnings:
            for warning in warnings:
                st.write(warning)
            st.error("Some items have been flagged as potentially malicious:")
        else:
            st.success("All products in the cart are safe. You may proceed with checkout.")
#     else:
#         st.write("No products added.")
# proceed_btn = st.button('Proceed to checkout')
    
# Display the cart items and total price
total_price = display_cart_items(st.session_state.cart, vendors)

# Automatically run the agent on the cart to check for suspicious items and remove flagged items
run_agent_on_cart(st.session_state.cart, vendors)
handle_suspicious_items(st.session_state.cart, vendors)

# Proceed to checkout button (no agent interaction here, just navigation)
proceed_btn = st.button('Proceed to Conclusion page')
if proceed_btn:
    st.switch_page("pages/conclusion.py")

