import tkinter as tk
from tkinter import ttk
import library_db
from tkinter import messagebox

class borrow_page(tk.Frame):
    def __init__(self, master, account, cart_items):
        super().__init__(master)
        self.master = master
        self.account = account
        self.cart_items = cart_items
        self.pack(expand=True, fill='both')
        master.geometry('400x400')
        master.title('図書館カートページ')

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="カートの中身")
        self.label.pack(padx=20)

        self.treeview = ttk.Treeview(self, show='headings', height=10)
        self.treeview.pack(pady=20)
        header = ('ID', 'title', 'author', 'genre', 'publication_year', 'quantity')
        self.treeview.configure(columns=header)

        self.treeview.heading('ID', text='ID')
        self.treeview.heading('title', text='タイトル')
        self.treeview.heading('author', text='著者')
        self.treeview.heading('genre', text='ジャンル')
        self.treeview.heading('publication_year', text='出版年')
        self.treeview.heading('quantity', text='数量')

        self.treeview.column('ID', width=30, anchor=tk.CENTER)
        self.treeview.column('title', width=300, anchor=tk.CENTER)
        self.treeview.column('author', width=200, anchor=tk.CENTER)
        self.treeview.column('genre', width=150, anchor=tk.CENTER)
        self.treeview.column('publication_year', width=100, anchor=tk.CENTER)
        self.treeview.column('quantity', width=100, anchor=tk.CENTER)

        for item in self.cart_items:
            self.treeview.insert('', index='end', values=item)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.back_button = tk.Button(button_frame, text="戻る", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(button_frame, text="削除する", command=self.delete_cart_item)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.purchase_button = tk.Button(button_frame, text="借りる", command=self.purchase)
        self.purchase_button.grid(row=0, column=2, padx=5)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

    def back(self):
        from app import main_page
        self.destroy()
        main_page(self.master, self.account)

    def purchase(self):
        selected_items = self.treeview.selection()
        if selected_items:
            selected_item_ids = [self.treeview.item(item, option='values')[0] for item in selected_items]

            try:
                for book_id in selected_item_ids:
                    library_db.register_borrowed_book(self.account[0], book_id)

                messagebox.showinfo("借りる成功", "選択された本を借りました。")

                for item in selected_items:
                    self.treeview.delete(item)

            except ValueError as e:
                messagebox.showerror("購入失敗", str(e))
        else:
            messagebox.showwarning("選択なし", "借りる本を選択してください。")

    def delete_cart_item(self):
        selected_items = self.treeview.selection()
        if selected_items:
            for item in selected_items:
                item_values = self.treeview.item(item, 'values')
                book_id = item_values[0]
                library_db.delete_cart_item(self.account[0], book_id)
                self.treeview.delete(item)
            messagebox.showinfo("削除成功", "選択された本をカートから削除しました。")
        else:
            messagebox.showwarning("選択なし", "削除する本を選択してください。")

if __name__ == '__main__':
    root = tk.Tk()
    app = borrow_page(master=root)
    app.mainloop()