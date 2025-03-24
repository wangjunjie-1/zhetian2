import sqlite3
import logging


class UserQuery:
    def __init__(self, db_path='./asserts/zhetian2.db'):
        """
        初始化数据库连接
        :param db_path: 数据库文件路径
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            self.logger.error(f"数据库连接失败: {e}")
            print(f"数据库连接失败: {e}")
            raise sqlite3.Error(f"数据库连接失败: {e}")
        self.logger.info("数据库连接成功")
        print("数据库连接成功")

    def _execute_query(self, query, params=()):
        """
        执行查询并返回结果
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 查询结果
        """
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            self.logger.error(f"查询失败: {e}")
            return []

    def _execute_update(self, query, params=()):
        """
        执行更新操作（插入、更新、删除）
        :param query: SQL 语句
        :param params: 参数
        """
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            self.logger.info("操作成功")
        except sqlite3.Error as e:
            self.logger.error(f"操作失败: {e}")
            raise sqlite3.Error(f"操作失败: {e}")

    def get_user_by_id(self, user_id):
        """
        按 id 查询指定用户
        :param user_id: 用户 id
        :return: 查询结果（字典形式）
        """
        query = "SELECT * FROM players WHERE id = ?"
        result = self._execute_query(query, (user_id,))
        return self._format_result(result[0]) if result else None

    def get_users_by_realm_level(self, realm_level):
        """
        根据 realm_level 查询用户
        :param realm_level: 境界等级
        :return: 查询结果（列表形式）
        """
        query = "SELECT * FROM players WHERE realm_level = ?"
        results = self._execute_query(query, (realm_level,))
        return [self._format_result(row) for row in results]

    def get_users_by_parent_id(self, parent_id):
        """
        根据 father_id 或 mother_id 查询用户
        :param parent_id: 父亲或母亲的 id
        :return: 查询结果（列表形式）
        """
        query = "SELECT * FROM players WHERE father_id = ? OR mother_id = ?"
        results = self._execute_query(query, (parent_id, parent_id))
        return [self._format_result(row) for row in results]

    def get_all_users(self):
        """
        返回所有用户
        :return: 查询结果（列表形式）
        """
        query = "SELECT * FROM players"
        results = self._execute_query(query)
        return [self._format_result(row) for row in results]

    def get_master_user(self):
        """
        返回 isMaster = 1 的用户
        :return: 查询结果（列表形式）
        """
        query = "SELECT * FROM players WHERE isMaster = 1"
        result = self._execute_query(query)
        return self._format_result(result[0]) if result else None
   
    def update_user(self, player):
        """
        根据传入的 player 对象更新数据库中的记录
        :param player: 包含更新数据的 player 对象
        """
        query = """
        UPDATE players
        SET name = ?, age = ?, sex = ?, root = ?, father_id = ?, mother_id = ?,
            teacher_id = ?, realm_level = ?, base_breakup_probability = ?, isMaster = ?, isDead = ?, current_exp = ?
        WHERE id = ?
        """
        params = (
            player.name,
            player.age,
            player.sex,
            player.root,
            player.father_id,
            player.mother_id,
            player.teacher_id,
            player.realm_level,
            player.base_breakup_probability,
            player.isMaster,
            player.isDead,  # 默认值为 False
            player.current_exp,
            player.id,
        )
        self._execute_update(query, params)

    def delete_user(self, user_id):
        """
        标记用户为“死亡”（设置 isDead 为 True）
        :param user_id: 用户 id
        """
        query = "UPDATE players SET isDead = ? WHERE id = ?"
        params = (True, user_id)
        self._execute_update(query, params)

    def add_user(self, player):
        """
        根据传入的 player 对象创建新记录，并返回新记录的 id
        :param player: 包含新用户数据的 player 对象
        :return: 新记录的 id
        """
        query = """
        INSERT INTO players (name, age, sex, root, father_id, mother_id, teacher_id,
                             realm_level, base_breakup_probability, isMaster, isDead,current_exp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        """
        params = (
            player.name,
            player.age,
            player.sex,
            player.root,
            player.father_id,
            player.mother_id,
            player.teacher_id,
            player.realm_level,
            player.base_breakup_probability,
            player.isMaster,
            player.isDead,  # 默认值为 False
            player.current_exp,
        )
        self._execute_update(query, params)

        # 获取新记录的 id
        new_id = self.cursor.lastrowid
        return new_id

    def _format_result(self, result):
        """
        格式化查询结果
        :param result: 查询结果（元组形式）
        :return: 字典形式的查询结果
        """
        if not result:
            return None
        return {
            "id": result[0],
            "name": result[1],
            "age": result[2],
            "sex": result[3],
            "root": result[4],
            "realm_level": result[5],
            "base_breakup_probability": result[6],
            "isMaster": result[7],
            "father_id": result[8],
            "mother_id": result[9],
            "teacher_id": result[10],
            "isDead": result[11],
            'current_exp': result[12] if len(result) > 12 else False,  # 兼容旧表结构
        }

    def close(self):
        """
        关闭数据库连接
        """
        self.conn.close()


# 示例用法
if __name__ == "__main__":
    db_path = "./asserts/zhetian2.db"  # 替换为你的数据库文件路径
    query = UserQuery(db_path)

    # 1. 按 id 查询指定用户
    user = query.get_user_by_id(1)
    print("按 id 查询用户:", user)

    # 2. 根据 realm_level 查询用户
    realm_users = query.get_users_by_realm_level(0)
    print("根据 realm_level 查询用户:", realm_users)

    # 3. 根据 father_id 或 mother_id 查询用户
    parent_users = query.get_users_by_parent_id(1)
    print("根据 father_id 或 mother_id 查询用户:", parent_users)

    # 4. 返回所有用户
    all_users = query.get_all_users()
    print("所有用户:", all_users)

    # 5. 返回 isMaster = 1 的用户
    master_users = query.get_master_users()
    print("isMaster = 1 的用户:", master_users)

    # 6. 更新用户
    updated_player = {
        "id": 1,
        "name": "龙傲天",
        "age": 17,
        "sex": 0,
        "root": "金木水火土_天",
        "father_id": -1,
        "mother_id": -1,
        "teacher_id": -1,
        "realm_level": 1,
        "base_breakup_probability": 0.2,
        "isMaster": 1,
        "isDead": False,
    }
    query.update_user(updated_player)
    print("更新后的用户:", query.get_user_by_id(1))

    # 7. 标记用户为“死亡”
    query.delete_user(1)
    print("标记死亡后的用户:", query.get_user_by_id(1))

    # 8. 添加新用户
    new_player = {
        "name": "张三",
        "age": 20,
        "sex": 1,
        "root": "金木",
        "father_id": 1,
        "mother_id": -1,
        "teacher_id": -1,
        "realm_level": 0,
        "base_breakup_probability": 0.1,
        "isMaster": 0,
        "isDead": False,
    }
    new_id = query.add_user(new_player)
    print("新增用户的 id:", new_id)
    print("新增用户:", query.get_user_by_id(new_id))  # 查询新用户

    # 关闭数据库连接
    query.close()