import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master, account=None):
        super().__init__(master, width=400, height=400)
        self.pack(fill="both", expand=True)
        master.geometry('400x400')
        master.title('図書館')

        self.create_widgets()

    def create_widgets(self):
        central_frame = tk.Frame(self)
        central_frame.pack(expand=True)

        self.label = tk.Label(central_frame, text="図書館へようこそ")
        self.label.pack(pady=20)

        button_frame = tk.Frame(central_frame)
        button_frame.pack(pady=20)

        self.login_button = tk.Button(button_frame, text="ログイン", command=self.login_page, bg="white", activebackground="white")
        self.login_button.pack(side="left", padx=50)

        self.register_button = tk.Button(button_frame, text="登録", command=self.register_page, bg="white", activebackground="white")
        self.register_button.pack(side="right", padx=50)

    def login_page(self):
        from login_user import Login_page
        self.destroy()
        Login_page(self.master)

    def register_page(self):
        from register_user import Register_page
        self.destroy()
        Register_page(self.master)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()