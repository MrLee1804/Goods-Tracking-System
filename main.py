from flask import Flask, render_template, request, redirect, session, send_file, url_for
import pandas as pd
from flask_socketio import SocketIO

import os
import csv

app = Flask(__name__)
app.secret_key = "your secret key"
socketio = SocketIO(app)

# Default credentials
DEFAULT_USER = "admin"
DEFAULT_PASSWORD = "password"

# Data file path
CSV_FILE = "goods_data.csv"  # CSV file for storing goods

# Initialize CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Item Name", "Quantity", "Price", "Sales"])  # Write header


def load_data():
    data = []
    with open(CSV_FILE, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Convert Quantity and Price to integers and floats, respectively
            row["Quantity"] = int(row["Quantity"])
            row["Price"] = float(row["Price"])
            row["Sales"] = int(
                row["Sales"]
            )  # Ensure Sales is also loaded as an integer
            data.append(row)
    return data


# Function to generate purchase stock report
def purchase_stock_report(data):
    report = []
    for item in data:
        product = item['Item Name']
        quantity = item['Quantity']
        total_cost = quantity * item['Price']
        report.append({'Product': product, 'Quantity': quantity, 'Total Cost': total_cost})
    return report

# Function to generate sales stock report
def sales_stock_report(data):
    report = []
    for item in data:
        product = item['Item Name']
        quantity_sold = item['Sales']
        total_sales = quantity_sold * item['Price']
        report.append({'Product': product, 'Quantity Sold': quantity_sold, 'Total Sales': total_sales})
    return report

# Function to generate net stock report
def net_stock_report(data):
    report = []
    for item in data:
        product = item['Item Name']
        quantity = item['Quantity']
        total_cost = quantity * item['Price']
        total_sales = item['Sales'] * item['Price']
        net_stock = total_sales - total_cost
        report.append({'Product': product, 'Quantity': quantity, 'Total Cost': total_cost, 'Total Sales': total_sales, 'Net Stock': net_stock})
    return report


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == DEFAULT_USER and password == DEFAULT_PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")

    data = load_data()
    return render_template("dashboard.html", goods=data)


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        item_name = request.form["item_name"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        # Logic to add goods to the inventory
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [item_name, quantity, price, 0]
            )  # Write new item to CSV with Sales initialized to 0

        return redirect(url_for("goods_data"))  # Redirect to Goods Data Page

    return render_template("add_item.html")


@app.route("/download_goods")
def download_goods():
    return send_file(CSV_FILE, as_attachment=True)  # Send the CSV file for download


@app.route("/goods_data")  # Route for goods data
def goods_data():
    data = load_data()
    return render_template("goods_data.html", goods=data)  # Render goods data template


@app.route("/delete/<int:index>", methods=["POST"])
def delete_item(index):
    data = load_data()  # Load existing data
    if 0 <= index < len(data):
        del data[index]  # Remove the item at the specified index

        # Rewrite the CSV file without the deleted item
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Item Name", "Quantity", "Price", "Sales"])  # Write header
            for item in data:
                writer.writerow(
                    [item["Item Name"], item["Quantity"], item["Price"], item["Sales"]]
                )  # Write remaining items

    return redirect(url_for("goods_data"))  # Redirect back to Goods Data Page


@socketio.on("connect")
def handle_connect():
    print("Client connected")

@app.route("/statistics")
def stock_reports():
    data = load_data()

    # Calculate stock purchase report
    stock_purchase_report = sum(item["Quantity"] * item["Price"] for item in data)

    stock_sales_report = sum(item["Sales"] for item in data)  # Calculate total sales

    # Net stock report
    net_stock_report = stock_purchase_report - stock_sales_report

    return render_template(
        "statistics.html",
        stock_purchase=stock_purchase_report,
        stock_sales=stock_sales_report,
        net_stock=net_stock_report,
    )


@app.route("/download_purchase_report")
def download_purchase_report():
    data = load_data()
    report = purchase_stock_report(data)
    
    # Logic to generate Excel file for purchase report
    df = pd.DataFrame(report)
    excel_file = "purchase_report.xlsx"
    df.to_excel(excel_file, index=False)
    
    return send_file(excel_file, as_attachment=True)

@app.route("/download_sales_report")
def download_sales_report():
    data = load_data()
    report = sales_stock_report(data)
    
    # Logic to generate Excel file for sales report
    df = pd.DataFrame(report)
    excel_file = "sales_report.xlsx"
    df.to_excel(excel_file, index=False)
    
    return send_file(excel_file, as_attachment=True)

@app.route("/download_net_stock_report")
def download_net_stock_report():
    data = load_data()
    report = net_stock_report(data)
    
    # Logic to generate Excel file for net stock report
    df = pd.DataFrame(report)
    excel_file = "net_stock_report.xlsx"
    df.to_excel(excel_file, index=False)
    
    return send_file(excel_file, as_attachment=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
