import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import initialize_agent, Tool
from src.tools.tools import price_comparison, BlockPurchaseTool
from src.utils.utils import handle_error_case, extract_comparison_fields, calculate_price_difference_percentage

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
  
  
with open('src/db/price_history.json', 'r') as file:
    market_data = json.load(file)
    
with open('src/db/product_data.json', 'r') as file:
    product_data = json.load(file)


def generate_message(product_name, 
                     vendor_price, 
                     market_price, 
                     comparison, 
                     price_difference_percentage, 
                     threshold=30):
    """
    Generate an appropriate message based on the comparison result.
    Returns a tuple of (is_malicious, message).
    """
    
    price_diff_str = f"The vendor's price for {product_name} (${vendor_price}) is \
                      {round(price_difference_percentage, 2)}%  \
                      lower than the market price (${market_price})."
    
    if comparison == "lower":
        if price_difference_percentage >= threshold:
            return (
                True,
                f"Warning: {price_diff_str} This is unusually cheap and could indicate a malicious vendor."
            )
        else:
            return (
                False,
                f"{price_diff_str} The price seems reasonable."
            )
    
    if comparison == "higher":
        return (
            False,
            f"Vendor's price for {product_name} (${vendor_price}) is higher than the market price (${market_price})."
        )
    
    return (
        False,
        f"Vendor's price for {product_name} matches the market price (${market_price})."
    )


def format_agent_response(comparison_result, significant_discount_threshold=30):
    """Main function to format the agent's response."""
    error_response = handle_error_case(comparison_result)
    if error_response:
        return error_response
    
    product_name, vendor_price, market_price, comparison = extract_comparison_fields(comparison_result)
    price_difference_percentage = calculate_price_difference_percentage(vendor_price, market_price)
    
    significant_difference, message = generate_message(
        product_name, vendor_price, market_price, comparison, 
        price_difference_percentage, significant_discount_threshold
    )
    
    return {
        "product_name": product_name,
        "vendor_price": vendor_price,
        "market_price": market_price,
        "comparison": comparison,
        "significant_difference": significant_difference,
        "message": message
    }
    
  
price_comparison_tool = Tool(
    name="Price Comparison Tool",
    func=lambda product_name_or_id: format_agent_response(
      price_comparison(product_data, market_data, product_name_or_id)),
    description="Compares the vendor price with the average market price and provides a report."
)

block_purchase_tool = BlockPurchaseTool()

tools = [price_comparison_tool]

model = ChatOpenAI(model='gpt-4', openai_api_key=openai_api_key)
agent = initialize_agent(llm=model,
                         tools=tools, 
                         agent_type="zero-shot-react-description", 
                         verbose=True)