import streamlit as st

# Set page configuration
st.set_page_config(page_title="Conclusion - Cop N' Shop", page_icon="🚓", layout="centered")

# Header
st.title("Conclusion")

# Introduction to the marketplace simulation
st.write("""
In this project, we simulated a dynamic marketplace environment aimed at demonstrating 
the interactions between customers, vendors, and a rogue AI agent posing as a vendor. 
""")

# Marketplace Use Case
st.subheader("Marketplace Use Case")
st.write("""
The marketplace serves as a platform where vendors offer various products to customers. 
The app allows users to browse products from different vendors, add items to their cart, 
and proceed to checkout, mimicking a typical online shopping experience. 
""")

# Role of the Police Agent
st.subheader("The Role of the Police Agent")
st.write("""
To maintain order and security within the marketplace, a police agent has been integrated 
into the application. 
""")

st.markdown("""
<h3 style='font-size: 20px;'>Marketplace Police Agent Features:</h3>

- **Vendor Chatbot Parsing:** Analyzes responses from vendor chatbots to identify suspicious practices.<br>
- **Administrator Notifications:** Alerts administrators via Discord when suspicious actions are detected.<br>
- **User Alerts:** Notifies users when a vendor offers items at significantly discounted prices.<br>
- **Price Manipulation:** Monitors vendors' attempts to scam users.<br>
""", unsafe_allow_html=True)

# Conclusion
st.subheader("Conclusion")
st.write("""
**Cop N' Shop** is not just a simulation of a marketplace; it represents the broader implications 
of integrating artificial intelligence into everyday business operations. As AI continues to evolve, 
the need for vigilant monitoring and regulation becomes paramount.
""")


# Closing statement
st.write("""
Thank you for exploring **Cop N' Shop**! We invite you to continue navigating the challenges 
and opportunities presented by AI in our daily lives.
""")
