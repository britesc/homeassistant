from datetime import datetime, timedelta

def add_fifty_days(date_str):
    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Add 50 days
    new_date = date_obj + timedelta(days=50)
    
    # Convert back to string
    return new_date.strftime("%Y-%m-%d")

# Example usage
date_input = "2025-03-31"
new_date = add_fifty_days(date_input)
print("New date:", new_date)

