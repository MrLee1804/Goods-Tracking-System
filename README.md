# Goods Tracking System

## Description
The Goods Tracking System is a web application that allows users to manage inventory, track sales, and generate reports. It provides a user-friendly interface for adding, deleting, and viewing goods, as well as downloading reports in Excel format.

## Installation Instructions
To install the necessary dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage
To run the application, execute the following command:

```
python main.py
```

After starting the application, navigate to `http://127.0.0.1:5000` in your web browser to access the Goods Tracking System.

## Routes
- **/**: Home page of the application.
- **/login**: Login page for user authentication.
- **/logout**: Logs the user out and redirects to the home page.
- **/dashboard**: Displays the dashboard with inventory data.
- **/add_item**: Page to add new items to the inventory.
- **/goods_data**: Displays the list of goods in the inventory.
- **/delete/<int:index>**: Deletes an item from the inventory based on its index.
- **/sell_item**: Endpoint to sell an item and update inventory.
- **/statistics**: Displays stock reports and statistics.
- **/download_goods**: Downloads the goods data as a CSV file.
- **/download_purchase_report**: Downloads the purchase report as an Excel file.
- **/download_sales_report**: Downloads the sales report as an Excel file.
- **/download_net_stock_report**: Downloads the net stock report as an Excel file.

## Steps to Use
1. Start the application by running `python main.py`.
2. Navigate to `http://127.0.0.1:5000` in your web browser.
3. Log in using the default credentials (admin/password).
4. Use the dashboard to view inventory data.
5. Add new items using the "Add Item" page.
6. View and manage goods data.
7. Generate and download reports as needed.

## License
This project is licensed under the MIT License.
