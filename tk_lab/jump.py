import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("多界面跳转示例")
        self.show_main_frame()

    def show_main_frame(self):
        # 隐藏其他界面
        self.hide_all_frames()

        # 创建主界面
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        label = tk.Label(self.main_frame, text="这是主界面", font=("Arial", 24))
        label.pack(pady=20)

        button = tk.Button(self.main_frame, text="切换到第二界面", command=self.show_second_frame)
        button.pack(pady=10)

    def show_second_frame(self):
        # 隐藏其他界面
        self.hide_all_frames()

        # 创建第二界面
        self.second_frame = tk.Frame(self.root)
        self.second_frame.pack(fill="both", expand=True)

        label = tk.Label(self.second_frame, text="这是第二界面", font=("Arial", 24))
        label.pack(pady=20)

        button = tk.Button(self.second_frame, text="返回主界面", command=self.show_main_frame)
        button.pack(pady=10)

    def hide_all_frames(self):
        # 隐藏所有界面
        for widget in self.root.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = App(root)
    root.mainloop()