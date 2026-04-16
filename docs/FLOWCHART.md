# 流程圖文件 (Flowchart) - 個人記帳簿

這份文件基於產品需求文件 (PRD) 與系統架構文件 (Architecture) 所設計的流程視覺化圖表，旨在說明使用者的操作路徑與系統內部的資料互動過程。

## 1. 使用者流程圖 (User Flow)

此圖描述使用者從進入記帳系統開始的完整操作路徑，包含瀏覽與新增資料等核心動作。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[這月統計首頁]
    
    Home --> ViewBalance[查看總收入、總支出與餘額]
    Home --> ViewChart[查看本月支出比例圓餅圖]
    
    Home -->|點擊查看明細| History[歷史收支紀錄頁]
    History -->|返回| Home
    
    Home -->|點擊新增紀錄| AddPage[新增收支頁面]
    History -->|點擊新增紀錄| AddPage
    
    AddPage --> FillForm{填寫表單內容}
    FillForm -->|輸入金額、選擇分類| Submit[點擊送出]
    
    Submit --> Save[(儲存成功)]
    Save -->|系統自動導向| Home
```

## 2. 系統序列圖 (System Flow - 新增紀錄)

此圖描述使用者執行「新增一筆收支紀錄」時，系統前後端及資料庫之間完整的互動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端)
    participant Flask Route as 路由控制器 (Flask)
    participant Model as 資料模型 (Python)
    participant DB as SQLite 資料庫

    User->>Browser: 填寫收支表單 (金額=100, 分類=午餐)
    User->>Browser: 點按「送出」按鈕
    Browser->>Flask Route: 傳送 POST /add 請求 (附帶表單資料)
    
    rect rgb(240, 248, 255)
        Note over Flask Route, Model: 系統內部處理階段
        Flask Route->>Flask Route: 驗證資料格式正確性
        Flask Route->>Model: 呼叫新增紀錄常式 (add_record)
        Model->>DB: 執行 INSERT INTO 語法將資料寫入資料表
        DB-->>Model: 回傳新列 ID (寫入成功)
        Model-->>Flask Route: 紀錄新增成功
    end
    
    Flask Route-->>Browser: HTTP 302 Redirect (重新導向至首頁 /)
    Browser->>Flask Route: 發出 GET / 取得最新首頁
    Note over Flask Route, Browser: 重新運算包含最新紀錄的餘額與圖表並回傳渲染頁面
    Browser-->>User: 畫面更新，顯示最新餘額與新增的紀錄
```

## 3. 功能清單與路由對照表

本表統整了上述流程圖中所對應到的基礎軟體功能、與其在 Flask 開發時將設定之路由 (Route)。

| 功能名稱 | 介面說明 | 對應 URL 路徑 | HTTP 方法 |
| :--- | :--- | :--- | :--- |
| **首頁與餘額概況** | 顯示當月總收入、總支出、結餘數字與支出圓餅圖 | `/` | `GET` |
| **新增紀錄介面** | 提供下拉選單選擇分類，輸入金額與備註的表單 | `/add` | `GET` |
| **送出新增紀錄** | 接收表單傳遞過來的資料並寫入資料庫 | `/add` | `POST` |
| **歷史紀錄列表** | 提供表格狀的收支歷史明細（依時間倒序） | `/history` | `GET` |

> 註：這些路由對應的是 MVP 核心階段所必須實作的功能範圍。未來如擴充編輯、刪除或匯出 CSV 功能，將在此表後續擴展對應的 `/edit/<id>`, `/delete/<id>`, 與 `/export` 路由。
