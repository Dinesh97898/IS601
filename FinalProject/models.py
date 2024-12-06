import sqlite3
from pydantic import BaseModel
from typing import List, Optional


# Database connection
def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


# Pydantic Models
class Customer(BaseModel):
    name: str
    phone: str


class Item(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    timestamp: int
    customer_id: int
    notes: Optional[str] = ""
    items: List[int]  # List of item IDs


# CRUD Operations
def create_customer(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO customers (name, phone) VALUES (?, ?)",
        (customer.name, customer.phone)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid


def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, price) VALUES (?, ?)",
        (item.name, item.price)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid


def create_order(order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (timestamp, customer_id, notes) VALUES (?, ?, ?)",
        (order.timestamp, order.customer_id, order.notes)
    )
    order_id = cursor.lastrowid
    # Insert order items into order_items table
    for item_id in order.items:
        cursor.execute(
            "INSERT INTO order_items (order_id, item_id) VALUES (?, ?)",
            (order_id, item_id)
        )
    conn.commit()
    conn.close()


def get_item_by_id(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    return row
