import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Data storage
library = []
borrowed = {}

# Add Book
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    fee = float(fee_entry.get())
    qty = int(qty_entry.get())

    library.append({
        'title': title,
        'author': author,
        'isbn': isbn,
        'fee': fee,
        'qty': qty
    })

    messagebox.showinfo("Success", "Book Added Successfully")

# Search Book
def search_book():
    keyword = search_entry.get().lower()
    results = []

    for book in library:
        if keyword in book['title'].lower() or keyword in book['author'].lower():
            results.append(f"{book['title']} by {book['author']} (Available: {book['qty']})")

    result_box.delete(0, tk.END)
    for r in results:
        result_box.insert(tk.END, r)

# Borrow Book
def borrow_book():
    title = borrow_entry.get().lower()

    for book in library:
        if book['title'].lower() == title:
            if book['qty'] > 0:
                book['qty'] -= 1
                borrowed[title] = datetime.now()
                messagebox.showinfo("Success", "Book Borrowed")
                return
            else:
                messagebox.showwarning("Error", "No copies available")
                return

    messagebox.showerror("Error", "Book not found")

# Return Book
def return_book():
    title = return_entry.get().lower()

    if title in borrowed:
        borrow_date = borrowed[title]
        return_date = datetime.now()
        days = (return_date - borrow_date).days

        fee = 0
        for book in library:
            if book['title'].lower() == title:
                book['qty'] += 1
                if days > 14:
                    fee = (days - 14) * book['fee']
                break

        del borrowed[title]
        messagebox.showinfo("Return", f"Book Returned. Late Fee: {fee}")
    else:
        messagebox.showerror("Error", "No record of borrowing")

# Inventory Report
def show_inventory():
    report_box.delete(0, tk.END)
    for book in library:
        report_box.insert(tk.END, f"{book['title']} | {book['author']} | Qty: {book['qty']} | Fee/day: {book['fee']}")

# GUI Setup
root = tk.Tk()
root.title("Library Management System")
root.geometry("700x600")

# Add Book Section
tk.Label(root, text="Add Book").pack()

title_entry = tk.Entry(root)
title_entry.pack()
title_entry.insert(0, "Title")

author_entry = tk.Entry(root)
author_entry.pack()
author_entry.insert(0, "Author")

isbn_entry = tk.Entry(root)
isbn_entry.pack()
isbn_entry.insert(0, "ISBN")

fee_entry = tk.Entry(root)
fee_entry.pack()
fee_entry.insert(0, "Late Fee per Day")

qty_entry = tk.Entry(root)
qty_entry.pack()
qty_entry.insert(0, "Quantity")

tk.Button(root, text="Add Book", command=add_book).pack()

# Search Section
tk.Label(root, text="Search Book").pack()
search_entry = tk.Entry(root)
search_entry.pack()

tk.Button(root, text="Search", command=search_book).pack()

result_box = tk.Listbox(root)
result_box.pack(fill=tk.BOTH, expand=True)

# Borrow Section
tk.Label(root, text="Borrow Book (Enter Title)").pack()
borrow_entry = tk.Entry(root)
borrow_entry.pack()

tk.Button(root, text="Borrow", command=borrow_book).pack()

# Return Section
tk.Label(root, text="Return Book (Enter Title)").pack()
return_entry = tk.Entry(root)
return_entry.pack()

tk.Button(root, text="Return", command=return_book).pack()

# Inventory Section
tk.Button(root, text="Show Inventory", command=show_inventory).pack()

report_box = tk.Listbox(root)
report_box.pack(fill=tk.BOTH, expand=True)

root.mainloop()
