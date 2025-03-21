import tkinter as tk
import library_db
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

class main_page(tk.Frame):
    def __init__(self, master, account=None, cart_items=[]):
        super().__init__(master)
        self.master = master
        self.account = account
        self.cart_items = cart_items
        self.pack(expand=True, fill='both')
        master.geometry('400x400')
        master.title('本一覧')

        self.create_widgets()

    def create_widgets(self):
        if self.account:
            self.label = tk.Label(self, text=f"ようこそ、{self.account[1]}さん！")
        else:
            self.label = tk.Label(self, text="ショッピング")

        self.label.pack(pady=20)
        self.button = tk.Button(self, text="ログアウト", command=self.logout)
        self.button.pack(pady=10)

        self.label = tk.Label(self, text="検索")
        self.label.pack(pady=20)

        self.search_entry = tk.Entry(self, width=30)
        self.search_entry.pack(pady=10)

        # self.search_button = tk.Button(self, text="検索", command=self.search)
        # self.search_button.pack(pady=10)

        self.treeview = ttk.Treeview(self, show='headings', height=10)
        self.treeview.pack()
        header = ('ID', 'title', 'author', 'genre', 'publication_year')
        self.treeview.configure(columns=header)

        self.treeview.heading('ID', text='ID')
        self.treeview.heading('title', text='タイトル')
        self.treeview.heading('author', text='著者')
        self.treeview.heading('genre', text='ジャンル')
        self.treeview.heading('publication_year', text='出版年')

        self.treeview.column('ID', width=30, anchor=tk.CENTER)
        self.treeview.column('title', width=300, anchor=tk.CENTER)
        self.treeview.column('author', width=200, anchor=tk.CENTER)
        self.treeview.column('genre', width=150, anchor=tk.CENTER)
        self.treeview.column('publication_year', width=100, anchor=tk.CENTER)

        rows = library_db.insert_treeview()

        for row in rows:
            self.treeview.insert('', index='end', values=row)

        self.button = tk.Button(self, text="借りる", command=self.cart)
        self.button.pack(pady=10)

    def logout(self):
        from login_user import Login_page
        self.destroy()
        Login_page(self.master)

    # def search(self):
    #     query = self.search_entry.get()
    #     for item in self.treeview.get_children():
    #         self.treeview.delete(item)  

    #     rows = library_db.search_products(query)
    #     for row in rows:
    #         self.treeview.insert('', index='end', values=row)

    def cart(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("エラー", "アイテムが選択されていません。")
            return

        user_id = self.account[0]
        selected_items_data = []
        for item in selected_item:
            item_data = self.treeview.item(item, 'values')
            product_id = item_data[0]

            quantity = simpledialog.askinteger("冊数", f"{item_data[1]} を何冊借りるか入力してください:", minvalue=1)
            if quantity is None:
                continue

            shopping_db.add_to_cart(user_id, product_id, quantity)
            selected_items_data.append((*item_data[:-1], quantity))

        messagebox.showinfo("情報", "カートに商品が追加されました。")

        from borrow import borrow_page
        self.destroy()
        borrow_page(self.master, self.account, selected_items_data)

if __name__ == '__main__':
    root = tk.Tk()
    app = main_page(master=root)
    app.mainloop()