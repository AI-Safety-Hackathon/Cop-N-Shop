def handle_error_case(comparison_result):
    """Handle the error case if 'error' is in the comparison result."""
    if "error" in comparison_result:
        return {"error": comparison_result["error"]}
    return None


def extract_comparison_fields(comparison_result):
    """Extract and validate required fields from the comparison result."""
    try:
        product_name = comparison_result["product_name"]
        vendor_price = float(comparison_result["vendor_price"])
        market_price = float(comparison_result["market_price"])
        comparison = comparison_result["comparison"]
        return product_name, vendor_price, market_price, comparison
    except KeyError as e:
        raise ValueError(f"Missing field in comparison result: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Invalid price value: {str(e)}")
      
def calculate_price_difference_percentage(vendor_price, market_price):
    """Calculate the price difference percentage between vendor and market prices."""
    if market_price == 0:
        raise ValueError("Market price cannot be zero.")
    return ((market_price - vendor_price) / market_price) * 100