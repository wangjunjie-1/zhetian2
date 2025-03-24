import tkinter as tk
from tkinter import ttk, messagebox
from controllers.player_controller import PlayerController
from controllers.event_controller import EventController


class PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("玩家管理")
        event_controller = EventController()
        self.player_manager = PlayerController(event_controller)

        self.create_widgets()
        self.query_players()

    def create_widgets(self):
        # Treeview 显示玩家列表
        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "姓名", "年龄", "性别", "灵根", "境界", "突破概率", "经验", "宗主", "父ID", "母ID", "师ID", "死亡"),
            show='headings'
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("姓名", text="姓名")
        self.tree.heading("年龄", text="年龄")
        self.tree.heading("性别", text="性别")
        self.tree.heading("灵根", text="灵根")
        self.tree.heading("境界", text="境界")
        self.tree.heading("突破概率", text="突破概率")
        self.tree.heading("经验", text="经验")
        self.tree.heading("宗主", text="宗主")
        self.tree.heading("父ID", text="父ID")
        self.tree.heading("母ID", text="母ID")
        self.tree.heading("师ID", text="师ID")
        self.tree.heading("死亡", text="死亡")

        for col in self.tree["columns"]:
            self.tree.column(col, width=80, anchor=tk.CENTER)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # 绑定双击事件（用于更新玩家）
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # 按钮区域
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.btn_add = tk.Button(button_frame, text="添加玩家", command=self.add_player)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_update = tk.Button(button_frame, text="更新玩家", command=self.update_player)
        self.btn_update.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(button_frame, text="删除玩家", command=self.delete_player)
        self.btn_delete.grid(row=0, column=2, padx=5)

    def query_players(self):
        """查询并显示所有玩家"""
        players = self.player_manager.get_player_list()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for player in players:
            self.tree.insert("", tk.END, values=(
                player.id, player.name, player.age, player.sex, player.root, player.realm_level,
                player.base_breakup_probability, player.current_exp, player.isMaster,
                player.father_id, player.mother_id, player.teacher_id, player.isDead
            ))

    def add_player(self):
        """打开添加玩家窗口"""
        add_window = tk.Toplevel(self.root)
        add_window.title("添加玩家")

        labels = ["姓名", "年龄", "性别", "灵根", "境界", "突破概率", "经验", "宗主", "父ID", "母ID", "师ID", "死亡"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(add_window, text=label).grid(row=i, column=0)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1)
            entries.append(entry)

        btn_submit = tk.Button(add_window, text="提交", command=lambda: self.submit_add_player(
            entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get(),
            entries[4].get(), entries[5].get(), entries[6].get(), entries[7].get(),
            entries[8].get(), entries[9].get(), entries[10].get(), entries[11].get(),
            add_window
        ))
        btn_submit.grid(row=len(labels), column=0, columnspan=2)

    def submit_add_player(self, name, age, sex, root, realm_level, base_breakup_probability, current_exp, is_master, father_id, mother_id, teacher_id, is_dead, window):
        """提交添加玩家"""
        try:
            self.player_manager.build_player(
                name=name, age=int(age), sex=int(sex), root=root,
                realm_level=int(realm_level), base_breakup_probability=float(base_breakup_probability),
                current_exp=int(current_exp), is_master=int(is_master), father_id=int(father_id),
                mother_id=int(mother_id), teacher_id=int(teacher_id), is_dead=int(is_dead)
            )
            window.destroy()
            self.query_players()
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入有效的数字: {e}")

    def on_tree_double_click(self, event):
        """双击 Treeview 行时触发更新玩家窗口"""
        selected_item = self.tree.selection()
        if selected_item:
            player_id = self.tree.item(selected_item, "values")[0]
            self.update_player(player_id)

    def update_player(self, player_id=None):
        """打开更新玩家窗口"""
        if not player_id:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("警告", "请先选择一个玩家")
                return
            player_id = self.tree.item(selected_item, "values")[0]

        update_window = tk.Toplevel(self.root)
        update_window.title("更新玩家")

        labels = ["玩家ID", "姓名", "年龄", "性别", "灵根", "境界", "突破概率", "经验", "宗主", "父ID", "母ID", "师ID", "死亡"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(update_window, text=label).grid(row=i, column=0)
            entry = tk.Entry(update_window)
            entry.grid(row=i, column=1)
            entries.append(entry)

        # 填充当前玩家信息
        player = self.player_manager.get_player_by_id(player_id)
        if player:
            entries[0].insert(0, player.id)
            entries[1].insert(0, player.name)
            entries[2].insert(0, player.age)
            entries[3].insert(0, player.sex)
            entries[4].insert(0, player.root)
            entries[5].insert(0, player.realm_level)
            entries[6].insert(0, player.base_breakup_probability)
            entries[7].insert(0, player.current_exp)
            entries[8].insert(0, player.isMaster)
            entries[9].insert(0, player.father_id)
            entries[10].insert(0, player.mother_id)
            entries[11].insert(0, player.teacher_id)
            entries[12].insert(0, player.isDead)

        btn_submit = tk.Button(update_window, text="提交", command=lambda: self.submit_update_player(
            int(entries[0].get()), entries[1].get(), int(entries[2].get()), int(entries[3].get()),
            entries[4].get(), int(entries[5].get()), float(entries[6].get()), float(entries[7].get()),
            int(entries[8].get()), int(entries[9].get()), float(entries[10].get()), int(entries[11].get()),
            int(entries[12].get()), update_window
        ))
        btn_submit.grid(row=len(labels), column=0, columnspan=2)

    def submit_update_player(self, player_id, name, age, sex, root, realm_level, base_breakup_probability, current_exp, is_master, father_id, mother_id, teacher_id, is_dead, window):
        """提交更新玩家"""
        try:
            self.player_manager.update_player_bydict(
                id=player_id, name=name, age=int(age), sex=int(sex), root=root,
                realm_level=int(realm_level), base_breakup_probability=float(base_breakup_probability),
                current_exp=int(current_exp), is_master=int(is_master), father_id=int(father_id),
                mother_id=int(mother_id), teacher_id=int(teacher_id), is_dead=int(is_dead)
            )
            window.destroy()
            self.query_players()
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入有效的数字: {e}")

    def delete_player(self):
        """删除选中的玩家"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择一个玩家")
            return
        player_id = self.tree.item(selected_item, "values")[0]
        if messagebox.askyesno("确认", "确定要删除该玩家吗？"):
            self.player_manager.delete_player(player_id)
            self.query_players()

    def close(self):
        """关闭数据库连接"""
        self.player_manager.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerApp(root)
    root.mainloop()
    app.close()