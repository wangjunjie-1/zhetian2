from controllers import GameEngine
from core.logger import configure_logger

if __name__ == "__main__":
    configure_logger()  # 初始化日志系统
    core = GameEngine()
    core.start()

    # core.playercontroller.buildPlayer(name='wjj')
    # 使用 join 阻塞主线程
    # core.UI_thread.join()