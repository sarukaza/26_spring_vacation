import tkinter as tk
import pygame
from tkinter import messagebox
from library_db import login
from main import Application
from pygame import mixer
from app import main_page

class Login_page(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        master.geometry('400x400')
        master.title('ログイン画面')

        self.create_widgets()


    def create_widgets(self):
        self.center_frame = tk.Frame(self)
        self.center_frame.pack(expand=True)

        self.label = tk.Label(self.center_frame, text="ログインページ")
        self.label.pack(pady=20)

        self.label_pw = tk.Label(self.center_frame, text='パスワード')
        self.entry_pw = tk.Entry(self.center_frame, width=30, show='*')
        self.label_pw.pack(pady=10)
        self.entry_pw.pack(pady=10)

        self.label_nm = tk.Label(self.center_frame, text='名前')
        self.entry_nm = tk.Entry(self.center_frame, width=30)
        self.label_nm.pack(pady=10)
        self.entry_nm.pack(pady=10)

        self.button_frame = tk.Frame(self.center_frame)
        self.button_frame.pack(pady=20)

        self.button_back = tk.Button(self.button_frame, text="戻る", command=self.back)
        self.button_back.pack(side="left", padx=10)

        self.button = tk.Button(self.button_frame, text="ログイン", command=self.login)
        self.button.pack(side="left", padx=10)

    def back(self):
        from main import Application
        self.destroy()
        Application(self.master)

    def login(self):
        if self.entry_pw.get() == '' or self.entry_nm.get() == '':
            messagebox.showerror('エラー', 'パスワードと名前は必須です')
        else:
            pw = self.entry_pw.get()
            name = self.entry_nm.get()
            if len(pw) < 6:
                messagebox.showerror('エラー', 'パスワードは6文字以上である必要があります')
                return
            account = login(pw, name)
            if account is not None:
                messagebox.showinfo('ログイン', 'ログイン成功です')
                self.destroy()
                main_page(self.master, account)
            else:   
                messagebox.showerror("エラー", "ログイン失敗です")

if __name__ == '__main__':
    root = tk.Tk()
    app = Login_page(master=root)
    app.mainloop()