import sqlite3
from .db import get_db

class Tag:
    @staticmethod
    def create(data):
        """
        新增一筆標籤記錄，如果該名稱已存在則回傳標籤的舊 ID。
        參數:
            data (dict): 包含 name
        回傳:
            int: 標籤的 id，出錯時回傳 None
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tags (name) VALUES (?)", (data.get('name'),))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            try: # 處理 Unique Constraint Failed 現象，取得原有 ID 
                cursor.execute("SELECT id FROM tags WHERE name = ?", (data.get('name'),))
                row = cursor.fetchone()
                return row['id']
            except sqlite3.Error as e:
                print(f"Error fetching existing tag by name: {e}")
                return None
        except sqlite3.Error as e:
            print(f"Error creating tag: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得系統內所有標籤。
        回傳:
            list: 字典資料包組合而成的全標籤清單
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tags ORDER BY name ASC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error getting all tags: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def add_to_recipe(recipe_id, tag_id):
        """
        建立食譜與標籤的多對多橋接關聯。
        參數:
            recipe_id (int): 食譜 ID
            tag_id (int): 標籤 ID
        回傳:
            bool: 設定成功與否
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)",
                (recipe_id, tag_id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return True # 代表該關聯已被建立過，無視即可
        except sqlite3.Error as e:
            print(f"Error linking tag: {e}")
            return False
        finally:
            if conn:
                conn.close()
        
    @staticmethod
    def get_by_recipe(recipe_id):
        """
        回傳特定食譜底下所有掛載的標籤列。
        參數:
            recipe_id (int): 特定食譜 ID
        回傳:
            list: 標籤記錄清單 (為字典結構)
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.* FROM tags t
                JOIN recipe_tags rt ON t.id = rt.tag_id
                WHERE rt.recipe_id = ?
            """, (recipe_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching tags for recipe: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def clear_recipe_tags(recipe_id):
        """
        移除該食譜的所有橋接標籤紀錄（例如用在修改表單前將舊狀態歸零）。
        參數:
            recipe_id (int):
        回傳:
            bool: 順利與否
        """
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipe_tags WHERE recipe_id = ?", (recipe_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error clearing recipe's tags: {e}")
            return False
        finally:
            if conn:
                conn.close()
