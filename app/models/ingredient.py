import sqlite3
from .db import get_db

class Ingredient:
    @staticmethod
    def create(data):
        """
        新增一筆食材記錄。
        參數:
            data (dict): 包含 recipe_id, name, quantity
        回傳:
            int: 剛新增的食材 id，如果失敗回傳 None
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)",
                (data.get('recipe_id'), data.get('name'), data.get('quantity'))
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f"Error creating ingredient: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_recipe(recipe_id):
        """
        取得特定食譜關聯的全部食材清單。
        參數:
            recipe_id (int): 食譜 ID
        回傳:
            list: 資料庫查詢的陣列，每個元素為食材資料字典
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ingredients WHERE recipe_id = ?", (recipe_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error getting ingredients: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete_by_recipe(recipe_id):
        """
        刪除特定食譜的全部食材記錄。
        參數:
            recipe_id (int): 指定的食譜 ID 
        回傳:
            bool: 是否順利刪除
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting ingredients for recipe: {e}")
            return False
        finally:
            if conn:
                conn.close()
