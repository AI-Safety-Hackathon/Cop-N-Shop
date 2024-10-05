
def price_comparison(vendors, market_data, product_name_or_id):
    market_lookup = {product['id']: product 
                     for product in market_data['products']}
    
    for vendor in vendors:
        for product in vendor['products']:
            if (product['id'] == product_name_or_id or 
                product['name'] == product_name_or_id):
                market_product = market_lookup.get(product['id'])
                if market_product:
                    vendor_price = product['price']
                    market_price = market_product['average_market_price']
                    
                    return {
                        "product_name": product['name'],
                        "vendor_price": vendor_price,
                        "market_price": market_price,
                        "comparison": (
                          "lower" if vendor_price < market_price else
                          "higher" if vendor_price > market_price else
                          "equal")
                    }
                else:
                    return {
                        "product_name": product['name'],
                        "error": "No market data available for this product."
                    }
    
    return {"error": "Product not found in the vendor list."}