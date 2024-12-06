from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from models import *

app = FastAPI()


# Endpoint to create a customer
@app.post("/customers/")
def create_customer_endpoint(customer: Customer):
    customer_id = create_customer(customer)
    return {"id": customer_id, "name": customer.name, "phone": customer.phone}


# Endpoint to retrieve a customer by ID
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"id": row["id"], "name": row["name"], "phone": row["phone"]}


# Endpoint to update a customer by ID
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET name = ?, phone = ? WHERE id = ?",
        (customer.name, customer.phone, customer_id)
    )
    conn.commit()
    conn.close()

    # Check if the customer exists
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"id": customer_id, "name": customer.name, "phone": customer.phone}


# Endpoint to delete a customer by ID
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()

    # Check if the customer exists
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"message": "Customer deleted successfully"}


# Endpoint to create an item
@app.post("/items/")
def create_item_endpoint(item: Item):
    item_id = create_item(item)
    return {"id": item_id, "name": item.name, "price": item.price}


# Endpoint to retrieve an item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"id": row["id"], "name": row["name"], "price": row["price"]}


# Endpoint to update an item by ID
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET name = ?, price = ? WHERE id = ?",
        (item.name, item.price, item_id)
    )
    conn.commit()
    conn.close()

    # Check if the item exists
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"id": item_id, "name": item.name, "price": item.price}


# Endpoint to delete an item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    # Check if the item exists
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted successfully"}


# Endpoint to create an order
@app.post("/orders/")
def create_order_endpoint(order: Order):
    create_order(order)
    return {"message": "Order created successfully"}


# Endpoint to retrieve an order by ID
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve order details
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order_row = cursor.fetchone()

    if order_row is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Retrieve customer details for the order
    cursor.execute("SELECT name, phone FROM customers WHERE id = ?", (order_row["customer_id"],))
    customer_row = cursor.fetchone()

    if customer_row is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Retrieve items for the order
    cursor.execute("""
        SELECT items.name, order_items.item_id
        FROM order_items
        JOIN items ON items.id = order_items.item_id
        WHERE order_items.order_id = ?
    """, (order_id,))
    items = cursor.fetchall()

    conn.close()

    return {
        "id": order_row["id"],
        "timestamp": order_row["timestamp"],
        "customer": {
            
            "name": customer_row["name"],
            "phone": customer_row["phone"]
        },
        "items": [{"item_id": item[1], "name": item[0]} for item in items],
        "notes": order_row["notes"]
    }


# Endpoint to update an order by ID
@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET timestamp = ?, customer_id = ?, notes = ? WHERE id = ?",
        (order.timestamp, order.customer_id, order.notes, order_id)
    )
    conn.commit()

    # Check if the order exists
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update order items
    cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
    conn.commit()
    for item_id in order.items:
        cursor.execute(
            "INSERT INTO order_items (order_id, item_id) VALUES (?, ?)",
            (order_id, item_id)
        )
    conn.commit()
    conn.close()

    return {"message": "Order updated successfully"}


# Endpoint to delete an order by ID
@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()

    # Check if the order exists
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    # Delete order items
    cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
    conn.commit()
    conn.close()

    return {"message": "Order deleted successfully"}
