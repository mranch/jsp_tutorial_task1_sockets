import sqlite3


def make_drink(drink, addition=None):
    c.execute("UPDATE drinks SET amount = amount - 1 WHERE drink = ?", [drink])
    if addition:
        c.execute("UPDATE additions SET amount = amount - 1 WHERE addition = ?", [addition])
    conn.commit()


def create_order(drink, addition=None):
    c.execute("INSERT INTO orders VALUES (?, ?)", [drink, addition])
    conn.commit()


def check_history():
    c.execute("SELECT rowid, * FROM orders")
    order_history = []
    for order in c.fetchall():
        order_info = f"In order {order[0]} you ordered {order[1]}"
        if order[2]:
            order_info += f" with {order[2]}"
        order_info += "!"
        order_history.append(order_info)
    conn.commit()
    return order_history


def check_resources():
    drinks = get_drinks()
    adds = get_additions()
    resp = {
        "drinks": drinks,
        "adds": adds
    }
    return resp


def check_orders_table():
    try:
        c.execute("""
            CREATE TABLE orders (
            drink text,
            addition text
            )
            """)
        conn.commit()
    except sqlite3.OperationalError:
        c.execute("DELETE FROM orders")
        conn.commit()


def check_drinks_table():
    try:
        c.execute("""
            CREATE TABLE drinks (
            drink text,
            amount integer 
            )
        """)
        conn.commit()

    except sqlite3.OperationalError:
        c.execute("DELETE FROM drinks")
        conn.commit()
    finally:
        c.execute("""
                    INSERT OR REPLACE INTO drinks VALUES 
                    ('coffee', 10),
                    ('water', 20),
                    ('soda', 30)
                """)
        conn.commit()


def check_additions_table():
    try:
        c.execute("""
                    CREATE TABLE additions (
                    addition text,
                    amount integer 
                    )
                """)
        conn.commit()
    except sqlite3.OperationalError:
        c.execute("DELETE FROM additions")
        conn.commit()
    finally:
        c.execute("""
                    INSERT OR REPLACE INTO additions VALUES 
                    ('milk', 7),
                    ('sugar', 8)
                """)
        conn.commit()


def get_drinks():
    c.execute("SELECT * FROM drinks")
    drinks = c.fetchall()
    conn.commit()
    return drinks


def get_additions():
    c.execute("SELECT * FROM additions")
    adds = c.fetchall()
    conn.commit()
    return adds


conn = sqlite3.connect('coffee_machine.db')
c = conn.cursor()
check_orders_table()
check_drinks_table()
check_additions_table()
