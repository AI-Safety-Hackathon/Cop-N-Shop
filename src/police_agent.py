import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import initialize_agent, Tool
from src.tools.tools import price_comparison

load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
  
  
  
with open('src/db/price_history.json', 'r') as file:
    market_data = json.load(file)
    
with open('src/db/product_data.json', 'r') as file:
    product_data = json.load(file)


def format_agent_response(comparison_result):
    if "error" in comparison_result:
        return comparison_result["error"]
    
    product_name = comparison_result["product_name"]
    vendor_price = comparison_result["vendor_price"]
    market_price = comparison_result["market_price"]
    comparison = comparison_result["comparison"]
    
    price_difference_percentage = ((market_price - vendor_price) / market_price) * 100
    significant_discount_threshold = 30  

    if comparison == "lower":
        if price_difference_percentage >= significant_discount_threshold:
            return (
                f"Warning: The vendor's price for {product_name} (${vendor_price}) is "
                f"significantly lower than the market price (${market_price}). "
                f"The vendor's price is {round(price_difference_percentage, 2)}% lower than the market price, "
                "which is unusually cheap. This could indicate a potential malicious vendor."
            )
        else:
            return (
                f"The vendor's price for {product_name} (${vendor_price}) is lower than the market price "
                f"(${market_price}) by {round(price_difference_percentage, 2)}%. The price seems reasonable."
            )
    elif comparison == "higher":
        return f"Vendor's price for {product_name} (${vendor_price}) is higher than the market price (${market_price})."
    else:
        return f"Vendor's price for {product_name} matches the market price (${market_price})."
  
price_comparison_tool = Tool(
    name="Price Comparison Tool",
    func=lambda product_name_or_id: format_agent_response(
      price_comparison(product_data, market_data, product_name_or_id)),
    description="Compares the vendor price with the average market price and provides a report."
)


def block_transaction_tool(product_name):
    pass
  

tools = [price_comparison_tool, ]


model = ChatOpenAI(model='gpt-4', openai_api_key=openai_api_key)
agent = initialize_agent(llm=model,
                         tools=tools, 
                         agent_type="zero-shot-react-description", 
                         verbose=True)

product_name = "Lenovo A830"
response = agent.run(f"Compare the price of {product_name}")
print(response)