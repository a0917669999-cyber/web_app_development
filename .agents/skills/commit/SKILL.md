---
name: commit
description: 提交並推送程式碼變更。用於每個開發階段完成後，將成果儲存到 Git 並推送到 GitHub。
---

# Commit Skill — 提交與推送程式碼

這個 skill 會引導 AI agent 幫你完成 Git 提交與推送，並在必要時設定 Git 身份識別資訊。

## When to use this skill

- 完成某個開發階段後，想要儲存進度
- 要把程式碼推送到 GitHub，讓組員可以取得最新版本
- 遇到 Git 要求設定 `user.name` 或 `user.email` 的提示

## ⚠️ 設定 Git 使用者身份

如果 Git 顯示以下提示，需要先設定身份才能 commit：

```
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```

請使用 `antigravity` 作為 username 與 email：

```bash
git config --global user.name "antigravity"
git config --global user.email "antigravity"
```

> 這樣設定後，之後所有 commit 都不需要再重新設定。

## How to use it

### 基本用法：提交並推送

```
請幫我將目前的變更提交並推送到 GitHub。

commit 訊息：[描述這次做了什麼，例如：docs: add PRD]
```

AI 會執行以下步驟：
1. 確認 Git 使用者身份是否已設定（若無則設定為 `antigravity`）
2. `git add .` — 加入所有變更
3. `git commit -m "[你的訊息]"` — 建立 commit
4. `git push` — 推送到 GitHub

---

### 完整提示語（可直接複製使用）

```
請幫我提交並推送目前的變更：

1. 如果尚未設定 Git 身份，請先執行：
   git config --global user.name "antigravity"
   git config --global user.email "antigravity"

2. 然後執行：
   git add .
   git commit -m "[在此填入 commit 訊息]"
   git push

完成後告訴我推送成功，並顯示 commit 的 hash 值。
```

---

## Commit 訊息格式建議

遵循以下格式，讓歷史紀錄更清楚：

| 類型   | 使用時機              | 範例                         |
| ------ | --------------------- | ---------------------------- |
| `docs` | 新增或修改文件        | `docs: add PRD`              |
| `feat` | 新增功能              | `feat: add task create form` |
| `fix`  | 修復錯誤              | `fix: form validation error` |
| `chore`| 設定、初始化等雜項    | `chore: init project`        |

---

## 各開發階段建議的 commit 訊息

| 階段       | 建議 commit 訊息                          |
| ---------- | ----------------------------------------- |
| 階段一完成 | `docs: add PRD`                           |
| 階段二完成 | `docs: add system architecture`           |
| 階段三完成 | `docs: add user flowchart`                |
| 階段四完成 | `feat: add database schema and models`    |
| 階段五完成 | `feat: add route skeleton and template plan` |
| 階段六完成 | `feat: implement [功能名稱]`              |

---

## 常見問題

**Q: push 時要求輸入帳號密碼？**

GitHub 已停止支援密碼驗證，請使用 Personal Access Token（PAT）：
1. 到 GitHub → Settings → Developer settings → Personal access tokens
2. 產生一個新 token（勾選 `repo` 權限）
3. push 時，「密碼」欄位貼上 token 即可

**Q: push 被拒絕（rejected）？**

可能是遠端有別的組員更新過，先執行：
```bash
git pull --rebase
git push
```

**Q: 不小心 commit 了不該 commit 的檔案？**

告訴 AI：「我剛才不小心 commit 了 [檔案名稱]，請幫我移除。」

**Q: 環境設定檔案與重要的機密文件要加入嗎?**

環境設定檔案（如 `.env`、`.env.local`、`.venv`）和機密文件（如 `secrets.py`、`config.py`）**絕對不要**加入 Git 追蹤。這些檔案通常包含敏感資訊（如 API 金鑰、資料庫密碼），應該被加入 `.gitignore` 中。
