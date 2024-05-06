import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create MySQL database engine
DB_USER = 'root'
DB_PASSWORD = 'soham2003'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'restaurant_management'

engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True, pool_pre_ping=True)
Base = declarative_base()


class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer = Column(String, nullable=False)
    table_no = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_time = Column(String(20), nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_menu_item(item_data):
    session = Session()
    item = MenuItem(**item_data)
    session.add(item)
    session.commit()
    session.close()


def add_order(order_data):
    session = Session()
    order = Order(**order_data)
    session.add(order)
    session.commit()
    session.close()


def get_all_menu_items():
    session = Session()
    items = session.query(MenuItem).all()
    session.close()
    return items


def get_all_orders():
    session = Session()
    orders = session.query(Order).all()
    session.close()
    return orders


class RestaurantManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack()
        self.create_home_page()

    def create_home_page(self):
        self.clear_frame()

        ttk.Label(self.main_frame, text="Restaurant Management System", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Button(self.main_frame, text="1. Place Order", command=self.place_order_gui).pack(pady=5)
        ttk.Button(self.main_frame, text="2. View Menu", command=self.view_menu).pack(pady=5)
        ttk.Button(self.main_frame, text="3. View Orders", command=self.view_orders).pack(pady=5)
        ttk.Button(self.main_frame, text="4. Exit", command=self.root.quit).pack(pady=5)

    def place_order_gui(self):
        self.clear_frame()
        self.create_order_form()


    def view_menu(self):
        self.clear_frame()

        menu_items = get_all_menu_items()

        self.menu_records_frame = ttk.LabelFrame(self.main_frame, text="Menu")
        self.menu_records_frame.pack(padx=20, pady=10)

        columns = ["ID", "Name", "Category", "Price"]
        tree = ttk.Treeview(self.menu_records_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)

        for item in menu_items:
            tree.insert("", "end", values=(
                item.id,
                item.name,
                item.category,
                item.price
            ))

        tree.pack(pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.create_home_page).pack(pady=5)

    def create_order_form(self):
        self.clear_frame()

        menu_items = get_all_menu_items()

        self.menu_records_frame = ttk.LabelFrame(self.main_frame, text="Menu")
        self.menu_records_frame.pack(padx=20, pady=10)

        columns = ["ID", "Name", "Category", "Price"]
        tree = ttk.Treeview(self.menu_records_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)

        for item in menu_items:
            tree.insert("", "end", values=(
                item.id,
                item.name,
                item.category,
                item.price
            ))

        tree.pack(pady=10)
        #Above code is for to view menu in place order

        self.order_form_frame = ttk.LabelFrame(self.main_frame, text="Place Order")
        self.order_form_frame.pack(padx=20, pady=10)


        self.order_labels = ["Customer Name:", "Table No.:", "Item ID:", "Quantity:"]
        self.order_entries = []

        for label_text in self.order_labels:
            label = ttk.Label(self.order_form_frame, text=label_text)
            label.pack(pady=5)
            entry = ttk.Entry(self.order_form_frame, width=50)
            entry.pack(pady=5)
            self.order_entries.append(entry)

        ttk.Button(self.order_form_frame, text="Place Order", command=self.place_order).pack(pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.create_home_page).pack(pady=5)

    def place_order(self):
        customer = self.order_entries[0].get().strip()
        table_no = self.order_entries[1].get().strip()
        item_id = self.order_entries[2].get().strip()
        quantity = self.order_entries[3].get().strip()
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            table_no = int(table_no)
            item_id = int(item_id)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Table No., Item ID, and Quantity must be valid integers.")
            return

        # Manually generate order ID
        order_id = self.generate_order_id()

        order_data = {
            "id": order_id,
            "customer": customer,
            "table_no": table_no,
            "item_id": item_id,
            "quantity": quantity,
            "order_time": order_time
        }

        add_order(order_data)
        messagebox.showinfo("Success", "Order placed successfully.")
        self.create_home_page()

    def generate_order_id(self):
        # Retrieve the maximum order ID from the database and add 1
        session = Session()
        max_order_id = session.query(func.max(Order.id)).scalar()
        session.close()
        return (max_order_id or 0) + 1


    def view_orders(self):
        self.clear_frame()

        orders = get_all_orders()

        if not orders:
            messagebox.showinfo("No Orders", "There are no orders available.")
            self.create_home_page()
            return

        # Dictionary to store total bill for each table number
        table_bills = {}

        for order in orders:
            table_no = order.table_no
            session = Session()  # Create a session
            item = session.query(MenuItem).filter(MenuItem.id == order.item_id).first()
            session.close()  # Close the session
            total_price = item.price * order.quantity

            if table_no not in table_bills:
                # Initialize bill for this table if not already present
                table_bills[table_no] = {
                    'customer': order.customer,
                    'total_price': total_price
                }
            else:
                # Update total bill for this table
                table_bills[table_no]['total_price'] += total_price

        # Display all orders
        orders_frame = ttk.LabelFrame(self.main_frame, text="All Orders")
        orders_frame.pack(padx=20, pady=10)

        # Display each order in a separate label
        for order in orders:
            session = Session()  # Create a session
            item = session.query(MenuItem).filter(MenuItem.id == order.item_id).first()
            session.close()  # Close the session
            order_label = ttk.Label(orders_frame,
                                    text=f"Table {order.table_no}: {order.customer} - Item: {item.name}, Quantity: {order.quantity}")
            order_label.pack(pady=5)

        # Create a button to navigate to the bill summary
        bill_button = ttk.Button(self.main_frame, text="Show Bill Summary",
                                 command=lambda: self.scroll_to_bill_summary(table_bills))
        bill_button.pack(pady=10)

        # Back button
        ttk.Button(self.main_frame, text="Back", command=self.create_home_page).pack(pady=5)

    def scroll_to_bill_summary(self, table_bills):
        # Clear the frame and create bill summary section
        self.clear_frame()
        bill_frame = ttk.LabelFrame(self.main_frame, text="Bill Summary")
        bill_frame.pack(padx=20, pady=10)

        # Display the bill for each table in a separate label
        for table_no, bill_info in table_bills.items():
            bill_label = ttk.Label(bill_frame,
                                   text=f"Table {table_no} (Customer: {bill_info['customer']}): ${bill_info['total_price']:.2f}")
            bill_label.pack(pady=5)

        # Back button
        ttk.Button(self.main_frame, text="Back to Orders", command=self.create_home_page).pack(pady=5)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = RestaurantManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
