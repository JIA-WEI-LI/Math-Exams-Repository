import os
from pathlib import Path

# 設定基礎路徑
BASE_DIR = Path("src/2026/高一上-數學")
OUTPUT_FILE = BASE_DIR / "檔案索引.md"

def generate_markdown():
    print(f"🔍 正在掃描目錄: {BASE_DIR.absolute()}")
    
    lines = ["# 2026 年度數學試卷索引\n", "## 段考系列\n", 
             "| 編號 | 名稱 | 考試範圍 | 原始碼(TEX) | PDF |\n", 
             "| :--- | :--- | :--- | :--- | :--- |\n"]
    
    quizzes = ["\n## 週考系列\n", 
               "| 編號 | 名稱 | 考試範圍 | 原始碼(TEX) | PDF |\n", 
               "| :--- | :--- | :--- | :--- | :--- |\n"]

    if not BASE_DIR.exists():
        print(f"❌ 錯誤: 找不到路徑 '{BASE_DIR}'")
        return

    # 取得所有子資料夾並排序
    folders = sorted([f for f in BASE_DIR.iterdir() if f.is_dir()])
    
    if not folders:
        print(f"⚠️ 警告: 在 '{BASE_DIR}' 底下沒有發現任何子資料夾。")
        return

    found_count = 0
    for folder in folders:
        name = folder.name
        print(f"📂 檢查資料夾: {name}")
        
        parts = name.split("-")
        
        # --- 檔案檢查機制 ---
        tex_file = folder / "main.tex"
        pdf_file = folder / f"{name}.pdf"

        # 判定 TeX 連結
        if tex_file.exists():
            tex_link = f"[TeX](./{name}/main.tex)"
            tex_status = "✅"
        else:
            tex_link = "🚫 缺失"
            tex_status = "❌"

        # 判定 PDF 連結
        if pdf_file.exists():
            pdf_link = f"[PDF](./{name}/{name}.pdf)"
            pdf_status = "✅"
        else:
            pdf_link = "⏳ 待上傳"
            pdf_status = "📁"

        # --- 寫入邏輯 ---
        if "段考" in name:
            try:
                no = parts[0]
                display_name = parts[2] if len(parts) > 2 else "未命名段考"
                lines.append(f"| {no} | {display_name} | 待補充 | {tex_link} | {pdf_link} |\n")
                print(f"   {tex_status}{pdf_status} 已加入段考: {display_name}")
                found_count += 1
            except IndexError:
                print(f"   ⚠️ 跳過: 名稱 '{name}' 格式不符")

        elif "週考" in name:
            try:
                no = f"{parts[0]}-{parts[2]}"
                display_name = parts[3] if len(parts) > 3 else "未命名週考"
                quizzes.append(f"| {no} | {display_name} | 待補充 | {tex_link} | {pdf_link} |\n")
                print(f"   {tex_status}{pdf_status} 已加入週考: {display_name}")
                found_count += 1
            except IndexError:
                print(f"   ⚠️ 跳過: 名稱 '{name}' 分段不足")

    # 寫入檔案
    if found_count > 0:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines + quizzes)
        print(f"\n✨ 成功更新 {OUTPUT_FILE}")
        print(f"📊 統計：共處理 {found_count} 個資料夾")
    else:
        print("\n💨 掃描完成，無符合資料。")

if __name__ == "__main__":
    generate_markdown()