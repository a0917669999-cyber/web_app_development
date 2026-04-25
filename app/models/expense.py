from app.models.db import get_db

class ExpenseModel:
    @staticmethod
    def create(type_, amount, category, description=""):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (type, amount, category, description) VALUES (?, ?, ?, ?)",
            (type_, amount, category, description)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        return record_id

    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC")
        records = cursor.fetchall()
        conn.close()
        return [dict(record) for record in records]

    @staticmethod
    def get_by_id(record_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (record_id,))
        record = cursor.fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def update(record_id, type_, amount, category, description=""):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE transactions SET type = ?, amount = ?, category = ?, description = ? WHERE id = ?",
            (type_, amount, category, description, record_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    @staticmethod
    def delete(record_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (record_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    @staticmethod
    def get_summary():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT type, SUM(amount) as total FROM transactions GROUP BY type")
        results = cursor.fetchall()
        conn.close()
        
        income = 0
        expense = 0
        for row in results:
            if row['type'] == 'income':
                income = row['total'] or 0
            elif row['type'] == 'expense':
                expense = row['total'] or 0
                
        return {
            "total_income": income,
            "total_expense": expense,
            "balance": income - expense
        }
