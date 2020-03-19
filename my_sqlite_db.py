import sqlite3


def make_drink(drink, addition=None):
    c.execute("UPDATE drinks SET amount = amount - 1 WHERE drink = ?", drink)
    if addition:
        c.execute("UPDATE additions SET amount = amount - 1 WHERE addition = ?", addition)
    conn.close()


def create_order(drink, addition=None):
    c.execute("INSERT INTO orders VALUES (?, ?)", [drink, addition])
    conn.commit()
    conn.close()


def check_history():
    c.execute("SELECT rowid, * FROM orders")
    order_history = []
    for order in c.fetchall():
        order_info = f"In order {order[0]} you ordered {order[1]}"
        if order[2]:
            order_info += f" with {order[2]}"
        order_info += "!"
        print(order_info)
        order_history.append(order_info)
    conn.commit()
    conn.close()
    return order_history


# create_order()
# conn.commit()
# c.execute("SELECT rowid, * FROM orders")
# print(c.fetchall())
# conn.commit()

try:
    conn = sqlite3.connect('coffee_machine.db')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE orders (
    drink text,
    addition text
    )
    """)
    c.execute("""
        CREATE TABLE drinks (
        drink text,
        amount integer 
        )
        """)
    c.execute("""
            CREATE TABLE additions (
            addition text,
            amount integer 
            )
            """)
except sqlite3.OperationalError:
    pass
# finally:
#     conn.close()
