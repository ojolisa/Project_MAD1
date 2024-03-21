import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
import sqlite3
matplotlib.use("Agg")


def plot1():
    conn = sqlite3.connect('grocery.db')
    cur = conn.cursor()
    cur.execute("SELECT id,quantity FROM product")
    products = cur.fetchall()
    conn.close()

    x, y = [], []
    for i in products:
        x.append(str(i[0]))
        y.append(i[1])
    plt.bar(x, y)
    plt.xlabel('Product ID')
    plt.ylabel('Quantity')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return image_base64
