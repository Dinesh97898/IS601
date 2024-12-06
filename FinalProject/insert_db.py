import json
from models import *


def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def populate_customers(customers_data):
    """Populate customers from customers.json."""
    customer_ids = {}
    for phone, name in customers_data.items():
        customer = Customer(name=name, phone=phone)
        customer_id = create_customer(customer)
        customer_ids[phone] = customer_id
    return customer_ids


def populate_items(orders_data):
    """Populate items from example_orders.json."""
    item_ids = {}
    for order_data in orders_data:
        for item in order_data['items']:
            if item['name'] not in item_ids:
                item_create = Item(name=item['name'], price=item['price'])
                item_id = create_item(item_create)
                item_ids[item['name']] = item_id
    return item_ids


def populate_orders(orders_data, customer_ids, item_ids):
    """Populate orders and order_items from example_orders.json."""
    for order_data in orders_data:
        # Get customer ID based on phone number
        customer_id = customer_ids.get(order_data['phone'])
        if not customer_id:
            print(f"Warning: Customer with phone {order_data['phone']} not found.")
            continue
        
        # Create order
        order_create = Order(
            timestamp=order_data['timestamp'],
            customer_id=customer_id,
            notes=order_data.get('notes', ""),
            items=[item_ids[item['name']] for item in order_data['items']]
        )
        create_order(order_create)


def main():
    # Load data from JSON files
    customers_data = load_json('customers.json')
    orders_data = load_json('example_orders.json')

    # Populate customers into the database
    print("Populating customers...")
    customer_ids = populate_customers(customers_data)

    # Populate items into the database
    print("Populating items...")
    item_ids = populate_items(orders_data)

    # Populate orders into the database
    print("Populating orders...")
    populate_orders(orders_data, customer_ids, item_ids)

    print("Database population complete.")


if __name__ == '__main__':
    main()
