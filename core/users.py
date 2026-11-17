from werkzeug.security import check_password_hash, generate_password_hash

from core.database import get_connection


def register_customer(uid, password, fname, lname, email, address, phno):
    conn = get_connection()
    try:
        row = conn.execute("SELECT uid FROM customer WHERE uid = ?", (uid,)).fetchone()
        if row:
            return False, "User already exists"

        conn.execute(
            "INSERT INTO customer (uid, pass_hash, fname, lname, email, address, phno) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (uid, generate_password_hash(password), fname, lname, email, address, phno),
        )
        conn.commit()
        return True, "Registered successfully, please login"
    except Exception as e:
        return False, "Database error: " + str(e)
    finally:
        conn.close()


def register_seller(sid, password, sname, address, phno):
    conn = get_connection()
    try:
        row = conn.execute("SELECT sid FROM seller WHERE sid = ?", (sid,)).fetchone()
        if row:
            return False, "Seller ID already exists"

        conn.execute(
            "INSERT INTO seller (sid, pass_hash, sname, address, phno) VALUES (?, ?, ?, ?, ?)",
            (sid, generate_password_hash(password), sname, address, phno),
        )
        conn.commit()
        return True, "Registered successfully, please login"
    except Exception as e:  # noqa: BLE001
        return False, "Database error: " + str(e)
    finally:
        conn.close()


def login_user(user_id, password, role):
    if role == "customer":
        query = "SELECT pass_hash FROM customer WHERE uid = ?"
    elif role == "seller":
        query = "SELECT pass_hash FROM seller WHERE sid = ?"
    else:
        return False, "Select a valid account type"

    conn = get_connection()
    try:
        row = conn.execute(query, (user_id,)).fetchone()
        if row is None:
            return False, "User does not exist"
        if not check_password_hash(row["pass_hash"], password):
            return False, "Invalid password"
        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, "Database error: " + str(e)
    finally:
        conn.close()


def get_profile(user_id, role):
    if role == "customer":
        query = (
            "SELECT uid, fname, lname, email, address, phno FROM customer WHERE uid = ?"
        )
    else:
        query = "SELECT sid, sname, address, phno FROM seller WHERE sid = ?"

    conn = get_connection()
    try:
        return conn.execute(query, (user_id,)).fetchone()
    finally:
        conn.close()
