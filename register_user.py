import tkinter as tk
import library_db
from tkinter import messagebox
from main import Application

class Register_page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill='both')
        master.geometry('400x400')
        master.title('登録画面')

        self.create_widgets()

    def create_widgets(self):

        self.center_frame = tk.Frame(self)
        self.center_frame.pack(expand=True)

        self.label = tk.Label(self.center_frame, text="登録フォーム")
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

        self.button = tk.Button(self.button_frame, text="登録", command=self.register)
        self.button.pack(side="left", padx=10)

    def back(self):
        self.destroy()
        Application(self.master)

    def register(self):
        if self.entry_pw.get() == '' or self.entry_nm.get() == '':
            messagebox.showerror('エラー', 'パスワードと名前は必須です')
        else:
            pw = self.entry_pw.get()
            name = self.entry_nm.get()
            if len(pw) < 6:
                messagebox.showerror('エラー', 'パスワードは6文字以上である必要があります')
                return
            try:
                library_db.insert_user(name, pw)   
                messagebox.showinfo('登録完了', '登録が完了しました')
            except ValueError as e:
                messagebox.showerror('エラー', str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = Register_page(master=root)
    app.mainloop()