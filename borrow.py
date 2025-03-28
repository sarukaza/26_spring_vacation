import tkinter as tk
from tkinter import ttk
import library_db
from tkinter import messagebox
from tkinter import simpledialog

class borrow_page(tk.Frame):
    def __init__(self, master, account, cart_items):
        super().__init__(master)
        self.master = master
        self.account = account
        self.cart_items = cart_items
        # self.cart_items = library_db.get_cart_items(account[0])
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

        self.delete_button = tk.Button(button_frame, text="削除する")
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
                # データベースに選択された本を「借りた」状態として登録
                for book_id in selected_item_ids:
                    library_db.register_borrowed_book(self.account[0], book_id)

                messagebox.showinfo("借りる成功", "選択された本を借りました。")

                # 借りた本をTreeviewから削除
                for item in selected_items:
                    self.treeview.delete(item)

            except ValueError as e:
                messagebox.showerror("購入失敗", str(e))
        else:
            messagebox.showwarning("選択なし", "借りる本を選択してください。")

    # def purchase(self):
    #     selected_items = self.treeview.selection()
    #     if selected_items:
    #         selected_item_ids = [self.treeview.item(item, option='values')[0] for item in selected_items]
    #         points_to_use = 0
            
    #         if messagebox.askyesno("ポイント利用", "利用可能なポイントを使用しますか？"):
    #             current_points = shopping_db.get_user_points(self.account[0])
    #             if current_points > 0:
    #                 points_to_use = simpledialog.askinteger("ポイント利用", f"利用するポイント数を入力してください (現在のポイント: {current_points}):", minvalue=1, maxvalue=current_points)
    #             else:
    #                 messagebox.showwarning("ポイント利用失敗", "利用可能なポイントがありません。")

    #         try:
    #             total_amount = purchase_selected_items(self.account[0], selected_item_ids, points_to_use)
    #             points_earned = total_amount // 10000
    #             shopping_db.add_points(self.account[0], points_earned)
    #             messagebox.showinfo("購入成功", f"合計金額は{total_amount}円です。{points_earned}ポイントが付与されました。")
    #             for item in selected_items:
    #                 self.treeview.delete(item)
    #             self.update_cart()
    #         except ValueError as e:
    #             messagebox.showerror("購入失敗", str(e))
    #     else:
    #         messagebox.showwarning("購入失敗", "購入するアイテムが選択されていません。")

    # def delete(self):
    #     selected_items = self.treeview.selection()
    #     if selected_items:
    #         for selected_item in selected_items:
    #             item_id = self.treeview.item(selected_item, option='values')[0]
    #             delete_cart_item(self.account[0], item_id)
    #             self.treeview.delete(selected_item)
    #         messagebox.showinfo("削除成功", "選択されたアイテムがカートから削除されました。")
    #     else:
    #         messagebox.showwarning("削除失敗", "削除するアイテムが選択されていません。")

    # def purchase_history(self):
    #     from purchase_history import Purchase_history
    #     self.destroy()
    #     Purchase_history(self.master, self.account)
        
    # def checkout(self):
    #     user_id = self.account[0]

    #     selected_items = self.treeview.selection()
    #     selected_item_ids = [self.treeview.item(item, 'values')[0] for item in selected_items]

    #     if not selected_item_ids:
    #         messagebox.showerror("エラー", "購入するアイテムが選択されていません。")
    #         return

    #     try:
    #         total_amount = shopping_db.purchase_selected_items(user_id, selected_item_ids)
    #         messagebox.showinfo("購入成功", f"合計金額 {total_amount} 円で購入しました。")
    #         self.update_cart()
    #     except Exception as e:
    #         messagebox.showerror("エラー", f"購入中にエラーが発生しました: {e}")

    # def update_cart(self):
    #     for item in self.treeview.get_children():
    #         self.treeview.delete(item)

    #     rows = shopping_db.get_cart_items(self.account[0])
    #     for row in rows:
    #         self.treeview.insert('', index='end', values=row)

if __name__ == '__main__':
    root = tk.Tk()
    app = borrow_page(master=root)
    app.mainloop()