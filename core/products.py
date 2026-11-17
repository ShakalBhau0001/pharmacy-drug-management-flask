from core.database import get_connection


def add_product(sid, pid, pname, manufacturer, mfg, exp, price, quantity):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT pid FROM product WHERE pid = ? OR pname = ?", (pid, pname)
        ).fetchone()
        if row:
            return False, "Product already exists, add a different product"

        conn.execute(
            "INSERT INTO product (pid, pname, manufacturer, mfg, exp, price) VALUES (?, ?, ?, ?, ?, ?)",
            (pid, pname, manufacturer, mfg, exp, price),
        )
        conn.execute(
            "INSERT INTO inventory (pid, sid, quantity) VALUES (?, ?, ?)",
            (pid, sid, quantity),
        )
        conn.commit()
        return True, "Product added"
    except Exception as e:
        conn.rollback()
        return False, "Database error: " + str(e)
    finally:
        conn.close()


def get_all_products():
    conn = get_connection()
    try:
        return conn.execute("""
            SELECT p.pid, p.pname, p.manufacturer, p.mfg, p.exp, p.price, i.quantity
            FROM product p JOIN inventory i ON p.pid = i.pid
            ORDER BY p.pname
        """).fetchall()
    finally:
        conn.close()


def get_seller_products(sid):
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT p.pid, p.pname, p.manufacturer, p.mfg, p.exp, p.price, i.quantity
            FROM product p JOIN inventory i ON p.pid = i.pid
            WHERE i.sid = ?
            ORDER BY p.pname
        """,
            (sid,),
        ).fetchall()
    finally:
        conn.close()


def restock_product(sid, pid, quantity):
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE inventory SET quantity = quantity + ? WHERE sid = ? AND pid = ?",
            (quantity, sid, pid),
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, "Product not found in your inventory"
        return True, "Stock updated"
    except Exception as e:  # noqa: BLE001
        conn.rollback()
        return False, "Database error: " + str(e)
    finally:
        conn.close()
