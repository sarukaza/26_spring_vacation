import tkinter as tk
import shopping_db
import pygame
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from pygame import mixer

class Application(tk.Frame):
    def __init__(self, master, account=None, cart_items=[]):
        super().__init__(master)
        self.master = master
        self.account = account
        self.cart_items = cart_items
        self.pack(expand=True, fill='both')
        master.geometry('400x400')
        master.title('ショッピング・サルダテ・商品一覧')

        pygame.mixer.init()
        self.play_bgm()

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

        self.search_button = tk.Button(self, text="検索", command=self.search)
        self.search_button.pack(pady=10)

        self.treeview = ttk.Treeview(self, show='headings', height=10)
        self.treeview.pack()
        header = ('ID', 'product_name', 'price', 'stock', 'description', 'quantity')
        self.treeview.configure(columns=header)

        self.treeview.heading('ID', text='ID')
        self.treeview.heading('product_name', text='商品名')
        self.treeview.heading('price', text='価格') 
        self.treeview.heading('stock', text='在庫')
        self.treeview.heading('description', text='商品説明')
        self.treeview.heading('quantity', text='個数')

        self.treeview.column('ID', width=30, anchor=tk.CENTER)
        self.treeview.column('product_name', width=300, anchor=tk.CENTER)
        self.treeview.column('price', width=80, anchor=tk.CENTER)
        self.treeview.column('stock', width=50, anchor=tk.CENTER)
        self.treeview.column('description', width=500, anchor=tk.CENTER)
        self.treeview.column('quantity', width=50, anchor=tk.CENTER)

        rows = shopping_db.insert_treeview()

        for row in rows:
            self.treeview.insert('', index='end', values=row)

        self.button = tk.Button(self, text="カートへ", command=self.cart)
        self.button.pack(pady=10)

    def logout(self):
        self.se_music()
        from login_user import Login_page
        self.destroy()
        Login_page(self.master)

    def search(self):
        self.se_music()
        query = self.search_entry.get()
        for item in self.treeview.get_children():
            self.treeview.delete(item)  

        rows = shopping_db.search_products(query)
        for row in rows:
            self.treeview.insert('', index='end', values=row)

    def cart(self):
        self.se_music()
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("エラー", "アイテムが選択されていません。")
            return

        user_id = self.account[0]
        selected_items_data = []
        for item in selected_item:
            item_data = self.treeview.item(item, 'values')
            product_id = item_data[0]

            quantity = simpledialog.askinteger("個数", f"{item_data[1]} の個数を入力してください:", minvalue=1)
            if quantity is None:
                continue

            shopping_db.add_to_cart(user_id, product_id, quantity)
            selected_items_data.append((*item_data[:-1], quantity))

        messagebox.showinfo("情報", "カートに商品が追加されました。")

        from cart import Cart_page
        self.destroy()
        Cart_page(self.master, self.account, selected_items_data)

    def se_music(self):
        click_sound = mixer.Sound("C:/Users/kazato/Downloads/マウスクリック音-効果音.mp3")
        click_sound.play()

    def play_bgm(self):
        pygame.mixer.music.load("C:/Users/kazato/Downloads/昼下がり気分.mp3")
        pygame.mixer.music.play(-1)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()