# ui/tk_ui.py
import tkinter as tk
from .base_view import BaseView
import logging
class MainView(BaseView):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        # self.frame.title("修仙门派游戏")
        # self.frame.geometry("1200x400")

        self.eventcontroller.subscribe('cultivate',lambda:self.update_player_info)
        self.eventcontroller.subscribe('breakup',lambda:self.update_player_info)
         # 创建主界面
        self.create_main_menu()
        
        
    def create_main_menu(self):
        """创建主菜单界面"""
        self.clear_window()

        # 配置列的权重
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(6, weight=1)

        # 标题
        tk.Label(self.frame, text="===== 修仙门派游戏 =====", font=("Arial", 16)).grid(row=1, column=1, columnspan=5, pady=10)

        # 创建个人 Frame
        personal_frame = tk.Frame(self.frame, bg="lightblue", bd=2, relief="sunken")
        personal_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        self.create_personal_frame(personal_frame)

        # 创建宗门 Frame
        faction_frame = tk.Frame(self.frame, bg="lightgreen", bd=2, relief="sunken")
        faction_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        self.create_faction_frame(faction_frame)

        # 创建系统 Frame
        system_frame = tk.Frame(self.frame, bg="lightcoral", bd=2, relief="sunken")
        system_frame.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")
        self.create_system_frame(system_frame)

        # 创建宗门信息 Frame
        faction_info_frame = tk.Frame(self.frame, bg="lightyellow", bd=2, relief="sunken")
        faction_info_frame.grid(row=2, column=4, padx=10, pady=10, sticky="nsew")
        self.create_faction_info_frame(faction_info_frame)

        # 创建个人信息 Frame
        personal_info_frame = tk.Frame(self.frame, bg="lightpink", bd=2, relief="sunken")
        personal_info_frame.grid(row=2, column=5, padx=10, pady=10, sticky="nsew")
        self.create_personal_info_frame(personal_info_frame)

    def create_personal_frame(self, personal_frame):
        """创建个人 Frame"""
        tk.Label(personal_frame, text="【个人】", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(personal_frame, text="修炼", width=15).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(personal_frame, text="探索", width=15).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(personal_frame, text="炼丹", width=15).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(personal_frame, text="打造武器",command=self.create_weapon_dialog,  width=15).grid(row=4, column=0, padx=10, pady=10)

    def create_faction_frame(self, faction_frame):
        """创建宗门 Frame"""
        tk.Label(faction_frame, text="【宗门】", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(faction_frame, text="创建门派", width=15).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(faction_frame, text="管理门派", width=15).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(faction_frame, text="招募弟子", width=15).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(faction_frame, text="培养弟子", width=15).grid(row=4, column=0, padx=10, pady=10)

    def create_system_frame(self, system_frame):
        """创建系统 Frame"""
        tk.Label(system_frame, text="【系统】", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(system_frame, text="触发事件", width=15).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(system_frame, text="退出游戏", 
                command=lambda: [
                    self.eventcontroller.publish('exit'),  # 触发保存
                ], width=15).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(system_frame, text="手动刷新",command=lambda:self.eventcontroller.publish('show_main_view'), width=15).grid(row=4, column=0, padx=10, pady=10)

    def update_player_info(self):
        if hasattr(self,'is_show') and self.is_show is True:
            # 通过after方法调度到主线程
            self.frame.after(0, self._real_update_player_info)

    def _real_update_player_info(self):
        # 实际更新操作
        personal_info_frame = tk.Frame(self.frame, bg="lightpink", bd=2, relief="sunken")
        personal_info_frame.grid(row=2, column=5, padx=10, pady=10, sticky="nsew")
        self.create_personal_info_frame(personal_info_frame)


    def update(self):
        self.logger.info("手动刷新")
        self.create_main_menu()
   
    def create_weapon_dialog(self):
        """创建武器打造弹窗"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("打造武器")
        
        # 武器信息展示
        info_frame = tk.Frame(dialog)
        info_frame.pack(padx=10, pady=10)
        
        # 分配下拉列表
        assign_frame = tk.Frame(dialog)
        assign_frame.pack(padx=10, pady=5)
        
        # 再创建武器之间应该还存在一个资源判定过程，预留这部分逻辑判断
        if 1==1:
            weapon = self.eventcontroller.publish('weapon_created')[0]
            print(weapon)
            # 显示武器信息
            for widget in info_frame.winfo_children():
                widget.destroy()
            tk.Label(info_frame, text=f"成功打造：{weapon.name}").pack()
            tk.Label(info_frame, text=f"品级：{weapon.level}").pack()
            tk.Label(info_frame, text=f"类型：{weapon.part_type}").pack()
            tk.Label(assign_frame, text="分配给：").pack(side="left")

            disciples = ['宗门'] + list(self.playercontroller.playerList.keys()) # 需要实现getDisciples方法
            self.assign_var = tk.StringVar(value='宗门')
            tk.OptionMenu(assign_frame, self.assign_var, *disciples).pack(side="left")
            # 确认按钮
            tk.Button(dialog, text="确认", command=lambda: [
                self.eventcontroller.publish('weapon_assigned', (self.assign_var.get(),weapon)),  # 触发保存
                dialog.destroy()
            ]).pack(pady=10)
        else:
            pass
    
    def update(self):
        self.logger.info("手动刷新")
        self.create_main_menu()
   
    def create_faction_info_frame(self, faction_info_frame):
        """创建宗门信息 Frame"""
        # 标题
        tk.Label(faction_info_frame, text="【宗门信息】", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # 创建 Text 组件
        info_text = tk.Text(faction_info_frame, width=30, height=10, wrap=tk.WORD)
        info_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


        # 插入宗门信息
        faction_info = (
            "名称:\t 青云门\t\n"
            "等级:\t 3\t\n"
            "灵石:\t 1000\t\n"
            "灵药:\t 50\t\n"
            "内门:\t 10\t\n"
            "外门:\t 20\t\n"
        )
        info_text.insert(tk.END, faction_info)
        info_text.config(state=tk.DISABLED)  # 设置为只读


    def create_personal_info_frame(self, personal_info_frame):
        """创建个人信息 Frame"""

        k,player = self.playercontroller.get_master()
        # 创建并放置标签和文本框
        tk.Label(personal_info_frame, text="掌门").grid(row=0, column=0, padx=10, pady=10)
        # tk.Button(personal_info_frame, text="查看",command=lambda:self.eventcontroller.publish('show_player_view',player)).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(personal_info_frame, text=player.name,command=lambda:self.eventcontroller.publish('show_player_view',player)).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(personal_info_frame, text=f"{player.realm.current_realm['name']}").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(personal_info_frame, text=f"年龄 {player.age}/{player.realm.lifespan}").grid(row=1, column=1, padx=10, pady=10)

        tk.Label(personal_info_frame, text="修为").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(personal_info_frame, text=f"{int(player.current_exp)}/{player.realm.current_exp_required}+{player.spiritroot.getRate():.2f}").grid(row=2, column=1, padx=10, pady=10)

        tk.Label(personal_info_frame, text="灵根").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(personal_info_frame, text=f"{player.spiritroot}").grid(row=3, column=1, padx=10, pady=10)


    def clear_window(self):
        """清空窗口内容"""
        for widget in self.frame.winfo_children():
            widget.destroy()
if __name__ == "__main__":
    # ui = TkUI()
    root = tk.Tk()
    app = MainView(root,None) 
    app.start()
    