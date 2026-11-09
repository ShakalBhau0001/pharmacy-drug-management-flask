from core.database import get_connection


def place_order(uid, pid, quantity):
    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT p.price, i.sid
            FROM product p JOIN inventory i ON p.pid = i.pid
            WHERE p.pid = ?
        """,
            (pid,),
        ).fetchone()
        if row is None:
            return False, "Product not found"

        # stock is reduced only if enough quantity is available
        cur = conn.execute(
            "UPDATE inventory SET quantity = quantity - ? WHERE pid = ? AND sid = ? AND quantity >= ?",
            (quantity, pid, row["sid"], quantity),
        )
        if cur.rowcount == 0:
            conn.rollback()
            return False, "Not enough stock available"

        conn.execute(
            "INSERT INTO orders (pid, sid, uid, quantity, price) VALUES (?, ?, ?, ?, ?)",
            (pid, row["sid"], uid, quantity, quantity * row["price"]),
        )
        conn.commit()
        return True, "Order placed"
    except Exception as e:  # noqa: BLE001
        conn.rollback()
        return False, "Database error: " + str(e)
    finally:
        conn.close()


def get_customer_orders(uid):
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT oid, pid, price, quantity, sid, orderdatetime FROM orders WHERE uid = ? ORDER BY oid DESC",
            (uid,),
        ).fetchall()
    finally:
        conn.close()


def get_seller_orders(sid):
    conn = get_connection()
    try:
        return conn.execute(
            "SELECT oid, pid, price, quantity, uid, orderdatetime FROM orders WHERE sid = ? ORDER BY oid DESC",
            (sid,),
        ).fetchall()
    finally:
        conn.close()
