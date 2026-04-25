from flask import Blueprint, render_template, request, redirect, url_for
from app.models.expense import ExpenseModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁 / 餘額概況
    - 呼叫 ExpenseModel.get_summary() 取得收支與結餘統計。
    - 渲染 index.html，並將統計數據傳入以供畫面與圓餅圖渲染。
    """
    pass

@main_bp.route('/add', methods=['GET', 'POST'])
def add_record():
    """
    新增紀錄介面與送出新增紀錄
    - GET: 單純回傳新增收支的表單頁面 (add.html)。
    - POST: 接收 HTML 表單資料（type, amount, category, description）。
            驗證資料後呼叫 ExpenseModel.create() 將紀錄寫入 SQLite。
            成功後 HTTP 302 Redirect 至首頁 (/)。
    """
    pass

@main_bp.route('/history')
def history():
    """
    歷史紀錄列表
    - 呼叫 ExpenseModel.get_all() 取得所有歷史收支紀錄。
    - 渲染 history.html，並傳入紀錄清單以呈現表格。
    """
    pass
