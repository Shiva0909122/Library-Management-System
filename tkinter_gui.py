import sqlite3
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import tkinter.ttk as ttk

# Tkinter GUI Setup
root = tk.Tk()
root.title('Library Management System')
root.geometry('1010x530')
root.resizable(0, 0)

# Database Connection
db_path = os.path.join(os.path.dirname(__file__), 'library.db')
connector = sqlite3.connect(db_path)
cursor = connector.cursor()

# Create Table if not exists
connector.execute(
'CREATE TABLE IF NOT EXISTS Library (BK_NAME TEXT, BK_ID TEXT PRIMARY KEY NOT NULL, AUTHOR_NAME TEXT, BK_STATUS TEXT, CARD_ID TEXT)'
)

# Functions
def issuer_card():
    Cid = simpledialog.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')
    if not Cid:
        messagebox.showerror('Issuer ID cannot be zero!', 'Can\'t keep Issuer ID empty, it must have a value')
    else:
        return Cid

def display_records():
    global connector, cursor, tree
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM Library')
    data = curr.fetchall()

    for records in data:
        tree.insert('', tk.END, values=records)

def clear_fields():
    global bk_status, bk_id, bk_name, author_name, card_id
    bk_status.set('Available')
    for i in ['bk_id', 'bk_name', 'author_name', 'card_id']:
        exec(f"{i}.set('')")
    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass

def add_record():
    global connector
    if bk_status.get() == 'Issued':
        card_id.set(issuer_card())
    else:
        card_id.set('N/A')

    surety = messagebox.askyesno('Are you sure?', 'Are you sure this is the data you want to enter?')

    if surety:
        try:
            connector.execute(
                'INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?)',
                (bk_name.get(), bk_id.get(), author_name.get(), bk_status.get(), card_id.get())
            )
            connector.commit()
            clear_fields()
            display_records()
            messagebox.showinfo('Record added', 'The new record was successfully added to your database')
        except sqlite3.IntegrityError:
            messagebox.showerror('Book ID already in use!',
                                 'The Book ID you are trying to enter is already in the database, please check for discrepancies')

# Tkinter Widgets (GUI)
bk_status = tk.StringVar()
bk_name = tk.StringVar()
bk_id = tk.StringVar()
author_name = tk.StringVar()
card_id = tk.StringVar()

left_frame = tk.Frame(root, bg='LightSkyBlue')
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

tk.Label(left_frame, text='Book Name', bg='LightSkyBlue', font=('Georgia', 13)).place(x=98, y=25)
tk.Entry(left_frame, width=25, font=('Times New Roman', 12), textvariable=bk_name).place(x=45, y=55)

tk.Label(left_frame, text='Book ID', bg='LightSkyBlue', font=('Georgia', 13)).place(x=110, y=105)
bk_id_entry = tk.Entry(left_frame, width=25, font=('Times New Roman', 12), textvariable=bk_id)
bk_id_entry.place(x=45, y=135)

tk.Label(left_frame, text='Author Name', bg='LightSkyBlue', font=('Georgia', 13)).place(x=90, y=185)
tk.Entry(left_frame, width=25, font=('Times New Roman', 12), textvariable=author_name).place(x=45, y=215)

tk.Label(left_frame, text='Status of the Book', bg='LightSkyBlue', font=('Georgia', 13)).place(x=75, y=265)
dd = tk.OptionMenu(left_frame, bk_status, *['Available', 'Issued'])
dd.configure(font=('Times New Roman', 12), width=12)
dd.place(x=75, y=300)

submit = tk.Button(left_frame, text='Add new record', font=('Gill Sans MT', 13), bg='SteelBlue', width=20, command=add_record)
submit.place(x=50, y=375)

clear = tk.Button(left_frame, text='Clear fields', font=('Gill Sans MT', 13), bg='SteelBlue', width=20, command=clear_fields)
clear.place(x=50, y=435)

# Table to display records
tree = ttk.Treeview(root, selectmode=tk.BROWSE, columns=('Book Name', 'Book ID', 'Author', 'Status', 'Issuer Card ID'))
tree.heading('Book Name', text='Book Name', anchor=tk.CENTER)
tree.heading('Book ID', text='Book ID', anchor=tk.CENTER)
tree.heading('Author', text='Author', anchor=tk.CENTER)
tree.heading('Status', text='Status of the Book', anchor=tk.CENTER)
tree.heading('Issuer Card ID', text='Card ID of the Issuer', anchor=tk.CENTER)

tree.column('#0', width=0, stretch=tk.NO)
tree.column('#1', width=225, stretch=tk.NO)
tree.column('#2', width=70, stretch=tk.NO)
tree.column('#3', width=150, stretch=tk.NO)
tree.column('#4', width=105, stretch=tk.NO)

tree.place(x=300, y=30, relheight=0.9, relwidth=0.7)

# Initialize display
display_records()

root.mainloop()
