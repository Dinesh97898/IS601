import json

def read_json(file_path):
    #read json
    return json.load(open(file_path,'r'))

def get_customers_json(json_data_objs, output_file):
    customer_data = {}
    for data_obj in json_data_objs:
        customer_data[data_obj['phone']] = data_obj['name']
    
    # Write  customers.json
    with open(output_file, 'w') as f:
        json.dump(customer_data, f, indent=4)

def get_items_json(json_data_obj, output_file):
    """Processes item data from JSON and writes to item.json."""
    item_data = {}
    for data_obj in json_data_obj:
        for order in data_obj['items']:
            if order['name'] in item_data.keys():
                item_data[order['name']]['orders'] += 1
            else:
                item_data[order['name']] = {
                    'price': order['price'],
                    'orders': 1
                }
    
    # write to json
    with open(output_file, 'w') as f:
        json.dump(item_data, f)

# Read json file
json_data = read_json("midterm_project/example_orders.json")

# customers.json
get_customers_json(json_data, "midterm_project/customers.json")

# items.json
get_items_json(json_data, "midterm_project/items.json")


