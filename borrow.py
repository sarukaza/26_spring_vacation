import tkinter as tk
import pygame
import library_db
from shopping_db import get_cart_items, purchase_selected_items, delete_cart_item
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from pygame import mixer

class borrow_page(tk.Frame):
    def __init__(self, master, account=None, cart_items=[]):
        super().__init__(master)
        self.account = account
        self.cart_items = get_cart_items(account[0])
        self.pack(expand=True, fill='both')
        master.geometry('400x400')
        master.title('ショッピング・サルダテ・カートページ')

        pygame.mixer.init()
        self.play_bgm()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="カートの中身")
        self.label.pack(padx=20)

        self.treeview = ttk.Treeview(self, show='headings', height=10)
        self.treeview.pack(pady=20)
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

        for item in self.cart_items:
            self.treeview.insert('', index='end', values=item)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.back_button = tk.Button(button_frame, text="戻る", command=self.back)
        self.back_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(button_frame, text="削除する", command=self.delete)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.purchase_button = tk.Button(button_frame, text="購入する", command=self.purchase)
        self.purchase_button.grid(row=0, column=2, padx=5)

        self.button = tk.Button(button_frame, text="購入履歴", command=self.purchase_history)
        self.button.grid(row=0, column=3, padx=5)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

    def back(self):
        self.se_music()
        from main import Application
        self.destroy()
        Application(self.master, self.account, self.cart_items)

    def purchase(self):
        self.se_music()
        selected_items = self.treeview.selection()
        if selected_items:
            selected_item_ids = [self.treeview.item(item, option='values')[0] for item in selected_items]
            points_to_use = 0
            
            if messagebox.askyesno("ポイント利用", "利用可能なポイントを使用しますか？"):
                current_points = shopping_db.get_user_points(self.account[0])
                if current_points > 0:
                    points_to_use = simpledialog.askinteger("ポイント利用", f"利用するポイント数を入力してください (現在のポイント: {current_points}):", minvalue=1, maxvalue=current_points)
                else:
                    messagebox.showwarning("ポイント利用失敗", "利用可能なポイントがありません。")

            try:
                total_amount = purchase_selected_items(self.account[0], selected_item_ids, points_to_use)
                points_earned = total_amount // 10000
                shopping_db.add_points(self.account[0], points_earned)
                messagebox.showinfo("購入成功", f"合計金額は{total_amount}円です。{points_earned}ポイントが付与されました。")
                for item in selected_items:
                    self.treeview.delete(item)
                self.update_cart()
            except ValueError as e:
                messagebox.showerror("購入失敗", str(e))
        else:
            messagebox.showwarning("購入失敗", "購入するアイテムが選択されていません。")

    def delete(self):
        self.se_music()
        selected_items = self.treeview.selection()
        if selected_items:
            for selected_item in selected_items:
                item_id = self.treeview.item(selected_item, option='values')[0]
                delete_cart_item(self.account[0], item_id)
                self.treeview.delete(selected_item)
            messagebox.showinfo("削除成功", "選択されたアイテムがカートから削除されました。")
        else:
            messagebox.showwarning("削除失敗", "削除するアイテムが選択されていません。")

    def se_music(self):
        click_sound = mixer.Sound("C:/Users/kazato/Downloads/マウスクリック音-効果音.mp3")
        click_sound.play()

    def play_bgm(self):
        pygame.mixer.music.load("C:/Users/kazato/Downloads/昼下がり気分.mp3")
        pygame.mixer.music.play(-1)

    def purchase_history(self):
        self.se_music()
        from purchase_history import Purchase_history
        self.destroy()
        Purchase_history(self.master, self.account)
        
    def checkout(self):
        self.se_music()
        user_id = self.account[0]

        selected_items = self.treeview.selection()
        selected_item_ids = [self.treeview.item(item, 'values')[0] for item in selected_items]

        if not selected_item_ids:
            messagebox.showerror("エラー", "購入するアイテムが選択されていません。")
            return

        try:
            total_amount = shopping_db.purchase_selected_items(user_id, selected_item_ids)
            messagebox.showinfo("購入成功", f"合計金額 {total_amount} 円で購入しました。")
            self.update_cart()
        except Exception as e:
            messagebox.showerror("エラー", f"購入中にエラーが発生しました: {e}")

    def update_cart(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        rows = shopping_db.get_cart_items(self.account[0])
        for row in rows:
            self.treeview.insert('', index='end', values=row)

if __name__ == '__main__':
    root = tk.Tk()
    app = borrow_page(master=root)
    app.mainloop()