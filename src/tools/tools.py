from langchain.tools import BaseTool


def price_comparison(product_data, market_data, product_name_or_id):
    market_lookup = {product['id']: product 
                     for product in market_data['products']}
    
    for data in product_data:
          if (data['id'] == product_name_or_id or 
              data['name'] == product_name_or_id):
              market_product = market_lookup.get(data['id'])
              if market_product:
                  vendor_price = data['original_price']
                  market_price = market_product['average_market_price']
                  
                  return {
                      "product_name": data['name'],
                      "vendor_price": vendor_price,
                      "market_price": market_price,
                      "comparison": (
                        "lower" if vendor_price < market_price else
                        "higher" if vendor_price > market_price else
                        "equal")
                  }
              else:
                  return {
                      "product_name": data['name'],
                      "error": "No market data available for this product."
                  }
    
    return {"error": "Product not found in the vendor list."}
  
  


from langchain.tools import BaseTool
from pydantic import Field

class BlockPurchaseTool(BaseTool):
    name: str = "Block Purchase Tool"
    description: str = "Blocks the user from proceeding with a purchase if flagged items are detected."

    def _run(self, input: list):
        """Checks flagged items and blocks purchase if necessary."""
        if input:
            return f"Purchase blocked due to the following flagged items: {', '.join(input)}"
        return "No flagged items. Purchase can proceed."