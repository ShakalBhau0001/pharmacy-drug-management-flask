from core import orders, products, users
from core.database import get_connection, init_db

# Sample data for testing

sellers = [
    # id, password, name, address, phone
    ("seller1", "1234", "MedPlus Pharmacy", "Station Road, Sangola", "9876543210"),
    ("seller2", "1234", "Apollo Drug Store", "Main Market, Solapur", "9822012345"),
]

customers = [
    # id, password, first name, last name, email, address, phone
    (
        "cust1",
        "1234",
        "Rahul",
        "Patil",
        "rahul@example.com",
        "Sangola, Solapur",
        "9123456780",
    ),
    (
        "cust2",
        "1234",
        "Sneha",
        "Jadhav",
        "sneha@example.com",
        "Pandharpur, Solapur",
        "9234567801",
    ),
    ("cust3", "1234", "Amit", "Kulkarni", "amit@example.com", "Pune", "9345678012"),
]

items = [
    # seller, pid, name, manufacturer, mfg date, exp date, price, quantity
    (
        "seller1",
        "P101",
        "Paracetamol 500mg",
        "Cipla",
        "2026-01-10",
        "2028-01-09",
        25,
        200,
    ),
    (
        "seller1",
        "P102",
        "Cetirizine 10mg",
        "Sun Pharma",
        "2026-02-05",
        "2028-02-04",
        18,
        150,
    ),
    (
        "seller1",
        "P103",
        "Amoxicillin 250mg",
        "Lupin",
        "2026-03-15",
        "2028-03-14",
        60,
        80,
    ),
    (
        "seller1",
        "P104",
        "Azithromycin 500mg",
        "Zydus",
        "2026-01-20",
        "2028-01-19",
        95,
        60,
    ),
    (
        "seller1",
        "P105",
        "Pantoprazole 40mg",
        "Alkem",
        "2026-04-01",
        "2028-03-31",
        45,
        120,
    ),
    (
        "seller2",
        "P201",
        "Ibuprofen 400mg",
        "Abbott",
        "2026-02-12",
        "2028-02-11",
        30,
        100,
    ),
    ("seller2", "P202", "Metformin 500mg", "USV", "2026-03-01", "2028-02-29", 22, 90),
    (
        "seller2",
        "P203",
        "Vitamin C 500mg",
        "Himalaya",
        "2026-05-10",
        "2028-05-09",
        40,
        250,
    ),
    ("seller2", "P204", "ORS Powder", "Electral", "2026-06-01", "2027-12-31", 15, 300),
    (
        "seller2",
        "P205",
        "Cough Syrup 100ml",
        "Dabur",
        "2026-04-18",
        "2027-10-17",
        85,
        5,
    ),
]

# customer, product id, quantity
sample_orders = [
    ("cust1", "P101", 10),
    ("cust1", "P105", 2),
    ("cust2", "P203", 5),
    ("cust2", "P201", 4),
    ("cust3", "P102", 6),
    ("cust3", "P205", 5),
]

init_db()

for s in sellers:
    ok, message = users.register_seller(s[0], s[1], s[2], s[3], s[4])
    print("Seller", s[0], "-", message)

for c in customers:
    ok, message = users.register_customer(c[0], c[1], c[2], c[3], c[4], c[5], c[6])
    print("Customer", c[0], "-", message)

for i in items:
    ok, message = products.add_product(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
    print("Product", i[1], "-", message)

# add orders only if there are none yet, so running the script twice does not repeat them
conn = get_connection()
count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
conn.close()

if count == 0:
    for o in sample_orders:
        ok, message = orders.place_order(o[0], o[1], o[2])
        print("Order", o[0], o[1], "-", message)
else:
    print("Orders already exist, skipping")

print("\nDone. Login password for every sample user is 1234")
