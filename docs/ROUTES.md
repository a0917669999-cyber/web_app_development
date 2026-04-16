# API 與路由設計文件 (API Design)

這份文件規劃了食譜管理系統的 URL 路由、對應的 HTTP 方法，以及用來渲染畫面的 Jinja2 模板清單。

## 1. 路由總覽表格

| 功能項目 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | :---: | --- | --- | --- |
| **首頁 / 食譜總覽** | `GET` | `/` | `recipes/index.html` | 顯示所有食譜，支援 `?q=關鍵字` 或是 `?ingredients=食材` 進行搜尋或推薦過濾。 |
| **新增食譜表單** | `GET` | `/recipes/new` | `recipes/new.html` | 顯示空白的新增食譜表單。 |
| **建立食譜** | `POST` | `/recipes` | *(無)* | 接收表單資料，寫入資料庫，並重導向回首頁。 |
| **食譜詳情** | `GET` | `/recipes/<int:id>` | `recipes/show.html` | 根據 ID 查詢資料庫，展示特定食譜的食材、步驟與標籤。 |
| **編輯食譜表單** | `GET` | `/recipes/<int:id>/edit` | `recipes/edit.html` | 取得特定 ID 食譜的原始資料，帶入編輯表單。 |
| **更新食譜** | `POST` | `/recipes/<int:id>/update` | *(無)* | 由於瀏覽器原生表單不支援 PUT，故使用 POST 更新資料庫，完成後重導向至該食譜詳情頁面。 |
| **刪除食譜** | `POST` | `/recipes/<int:id>/delete` | *(無)* | 使用 POST 刪除特定食譜，並重導向回首頁。 |

## 2. 每個路由的詳細說明

### `GET /`
- **輸入**：URL Query String（例如 `?q=牛肉` 或 `?ingredient=雞蛋`）。
- **處理邏輯**：
  - 如果沒有參數，呼叫 `Recipe.get_all()` 回傳全部清單。
  - 有參數則執行關鍵字查詢，或結合關聯表做食材查詢。
- **輸出**：渲染 `recipes/index.html`。

### `GET /recipes/new`
- **輸入**：無。
- **處理邏輯**：單純回傳頁面。
- **輸出**：渲染 `recipes/new.html`。

### `POST /recipes`
- **輸入**：HTML 表單資料 (包含 title, description, instructions，以及動態新增的 ingredients/tags)。
- **處理邏輯**：
  - 呼叫 `Recipe.create()`，取得新的 `recipe_id`。
  - 迴圈處理 `ingredients` 與 `tags`，連結至 `recipe_id`。
- **輸出**：HTTP `302 Redirect` 至 `/`。
- **錯誤處理**：如果必填欄位 (title) 為空，可使用 flash() 傳遞錯誤訊息然後重新渲染 `recipes/new.html`。

### `GET /recipes/<int:id>`
- **輸入**：URL 路徑上的 `<id>`。
- **處理邏輯**：
  - 呼叫 `Recipe.get_by_id(id)`，若找不到回報 404 Not Found。
  - 同時撈取對應的 Ingredients 與 Tags 資料。
- **輸出**：渲染 `recipes/show.html`，傳入食譜完整資料。

### `GET /recipes/<int:id>/edit`
- **輸入**：URL 路徑上的 `<id>`。
- **處理邏輯**：
  - 取出 `Recipe`、`Ingredients`、`Tags` 放入表單。
- **輸出**：渲染 `recipes/edit.html`。

### `POST /recipes/<int:id>/update`
- **輸入**：URL 路徑上的 `<id>`, HTML 表單修改後的資料。
- **處理邏輯**：
  - 執行 `Recipe.update()`。
  - 覆寫食材與標籤 (先刪除舊有關聯再重新寫入)。
- **輸出**：HTTP `302 Redirect` 至 `/recipes/<id>`。

### `POST /recipes/<int:id>/delete`
- **輸入**：URL 路徑上的 `<id>`。
- **處理邏輯**：呼叫 `Recipe.delete(id)`，仰賴 CASCADE 刪除相關食材與標籤關聯。
- **輸出**：HTTP `302 Redirect` 至 `/`。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates` 中。

1. **`base.html`**
   - 全網站的共通骨架，包含 `<head>`、Navbar、Footer 等。
   - 提供 `{% block content %}{% endblock %}` 讓子模板繼承。
2. **`recipes/index.html`** (繼承 `base.html`)
   - 包含搜尋列、食譜清單 (卡片或列表呈現)。
3. **`recipes/new.html`** (繼承 `base.html`)
   - 提供新增表單介面。
4. **`recipes/show.html`** (繼承 `base.html`)
   - 瀏覽食譜介面明細，並帶有「編輯」與「刪除」按鈕。
5. **`recipes/edit.html`** (繼承 `base.html`)
   - 功能與 `new.html` 類似，但在渲染時 value 會帶入原始食譜資訊。
