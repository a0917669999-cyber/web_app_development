from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.tag import Tag

# 建立 Recipe 模組的 Blueprint
bp = Blueprint('recipe', __name__)

@bp.route('/')
def index():
    """首頁 / 食譜總覽與搜尋"""
    search_query = request.args.get('q', '').strip()
    
    # 取得資料庫中所有的食譜
    recipes = Recipe.get_all()
    
    # 若有搜尋條件，簡單判斷名稱或敘述是否相符
    if search_query:
        recipes = [r for r in recipes if search_query.lower() in str(r.get('title', '')).lower() 
                   or search_query.lower() in str(r.get('description', '')).lower()]
        
    return render_template('recipes/index.html', recipes=recipes, search_query=search_query)

@bp.route('/recipes/new', methods=['GET'])
def new():
    """進入新增食譜頁面"""
    return render_template('recipes/new.html')

@bp.route('/recipes', methods=['POST'])
def create():
    """送出表單建立新食譜"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    instructions = request.form.get('instructions', '').strip()
    
    # 執行基本輸入驗證
    if not title:
        flash('食譜名稱為必填項目！', 'danger')
        return render_template('recipes/new.html', description=description, instructions=instructions)
        
    recipe_data = {
        'title': title,
        'description': description,
        'instructions': instructions
    }
    
    # 建立 Recipe
    recipe_id = Recipe.create(recipe_data)
    if not recipe_id:
        flash('建立食譜時發生系統錯誤，請重試！', 'danger')
        return render_template('recipes/new.html', description=description, instructions=instructions)
        
    # 處理食材清單 (以逗號分隔字串作為假設)
    ingredients_raw = request.form.get('ingredients', '')
    if ingredients_raw:
        for item in ingredients_raw.split(','):
            item = item.strip()
            if item: # 避免空白項目
                Ingredient.create({
                    'recipe_id': recipe_id,
                    'name': item,
                    'quantity': '' # 暫時簡化格式
                })
                
    # 處理標籤清單 (以逗號分隔字串作為假設)
    tags_raw = request.form.get('tags', '')
    if tags_raw:
        for item in tags_raw.split(','):
            item = item.strip()
            if item:
                tag_id = Tag.create({'name': item})
                if tag_id:
                    Tag.add_to_recipe(recipe_id, tag_id)
                    
    flash('食譜建立成功！', 'success')
    return redirect(url_for('recipe.index'))

@bp.route('/recipes/<int:id>', methods=['GET'])
def show(id):
    """顯示詳細食譜內容"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該篇食譜！', 'danger')
        return redirect(url_for('recipe.index'))
        
    ingredients = Ingredient.get_by_recipe(id)
    tags = Tag.get_by_recipe(id)
    
    return render_template('recipes/show.html', recipe=recipe, ingredients=ingredients, tags=tags)

@bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit(id):
    """進入編輯食譜頁面"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))
        
    # 為了讓前端表單能顯示以逗號分隔的舊資料字串
    ingredients = Ingredient.get_by_recipe(id)
    tags = Tag.get_by_recipe(id)
    ingredients_str = ", ".join([ing.get('name', '') for ing in ingredients])
    tags_str = ", ".join([tag.get('name', '') for tag in tags])
    
    return render_template('recipes/edit.html', recipe=recipe, ingredients_str=ingredients_str, tags_str=tags_str)

@bp.route('/recipes/<int:id>/update', methods=['POST'])
def update(id):
    """送出表單更新食譜資料"""
    # 檢查目標在不在
    if not Recipe.get_by_id(id):
        flash('欲修改的食譜不存在！', 'danger')
        return redirect(url_for('recipe.index'))
        
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    instructions = request.form.get('instructions', '').strip()
    
    if not title:
        flash('食譜名稱為必填項目！', 'danger')
        return redirect(url_for('recipe.edit', id=id)) # 原則上轉回編輯頁面並提示錯誤
        
    recipe_data = {
        'title': title,
        'description': description,
        'instructions': instructions
    }
    
    if not Recipe.update(id, recipe_data):
        flash('更新食譜過程發生錯誤！', 'danger')
        return redirect(url_for('recipe.edit', id=id))
        
    # 更新食材：砍掉重練是最簡單防錯的方法
    Ingredient.delete_by_recipe(id)
    ingredients_raw = request.form.get('ingredients', '')
    if ingredients_raw:
        for item in ingredients_raw.split(','):
            item = item.strip()
            if item:
                Ingredient.create({
                    'recipe_id': id,
                    'name': item,
                    'quantity': ''
                })
                
    # 更新標籤：同樣先砍斷關係橋接後再重新建立關聯
    Tag.clear_recipe_tags(id)
    tags_raw = request.form.get('tags', '')
    if tags_raw:
        for item in tags_raw.split(','):
            item = item.strip()
            if item:
                tag_id = Tag.create({'name': item})
                if tag_id:
                    Tag.add_to_recipe(id, tag_id)
                    
    flash('食譜更新成功囉！', 'success')
    return redirect(url_for('recipe.show', id=id))

@bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除指定食譜資料"""
    if Recipe.delete(id):
        flash('食譜已成功刪除！', 'success')
    else:
        flash('刪除食譜時發生錯誤。', 'danger')
        
    return redirect(url_for('recipe.index'))
