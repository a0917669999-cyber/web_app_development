from .db import get_db
import sqlite3

class Recipe:
    @staticmethod
    def create(data):
        """
        新增一筆食譜記錄。
        參數:
            data (dict): 包含 title, description, instructions
        回傳:
            int: 新增食譜的 id，若發生例外則回傳 None
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO recipes (title, description, instructions) VALUES (?, ?, ?)",
                (data.get('title'), data.get('description'), data.get('instructions'))
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f"Error creating recipe: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有記錄。
        回傳:
            list: 包含字典形式結果的清單，一筆對應一個食譜
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error getting all recipes: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(id):
        """
        取得單筆記錄。
        參數:
            id (int): 指定的食譜 ID
        回傳:
            dict: 若找得到則回傳單筆記錄的字典，否則為 None
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM recipes WHERE id = ?", (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error getting recipe by id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(id, data):
        """
        更新記錄。
        參數:
            id (int): 指定的食譜 ID
            data (dict): 包含 title, description, instructions 欲更新之資料
        回傳:
            bool: 更新成功與否
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE recipes SET title = ?, description = ?, instructions = ? WHERE id = ?",
                (data.get('title'), data.get('description'), data.get('instructions'), id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating recipe: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(id):
        """
        刪除記錄。
        參數:
            id (int): 指定的食譜 ID
        回傳:
            bool: 刪除成功與否
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipes WHERE id = ?", (id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting recipe: {e}")
            return False
        finally:
            if conn:
                conn.close()
