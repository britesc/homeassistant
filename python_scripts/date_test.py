from datetime import timedelta

def add_fifty_days(date_str):
    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Add 50 days
    new_date = date_obj + timedelta(days=50)
    thisdict =	{
        "drug": "Opium",
        "date": new_date
    }
    
    hass.states.set(entity_id, 'state', thisdict)
    # Convert back to string
    return new_date.strftime("%Y-%m-%d")


# Example usage
logger.info("Date Test 1 {} at {}".format("Fred 1",time.time()))
date_input = "2025-03-31"

new_date = add_fifty_days(date_input)
logger.info("Date Test 1 {} at {}".format("Fred 2",new_date))
print("New date:", new_date)






