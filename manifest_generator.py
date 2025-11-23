import os
import hashlib
import json

# --- ⚠️ НАСТРОЙ ЗДЕСЬ ⚠️ ---
REPO_PATH = r"C:\GitHub\hkef82h-pq91hggbfe14-gqh392gqwfurg921vbo3"
BASE_URL = "https://raw.githubusercontent.com/ukrainskiy04/hkef82h-pq91hggbfe14-gqh392gqwfurg921vbo3/main"
OUTPUT_FILE = "manifest.json"
IGNORE_LIST = [".git", ".gitignore", OUTPUT_FILE, "manifest_generator.py"]
# --- --------------------- ---

def calculate_sha1(filepath):
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def main():
    manifest = []
    repo_root = os.path.normpath(REPO_PATH)
    print(f"Сканирование папки: {repo_root}...")

    for root, dirs, files in os.walk(repo_root, topdown=True):
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
        
        for file in files:
            if file in IGNORE_LIST:
                continue
                
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_root).replace(os.sep, '/')
            file_hash = calculate_sha1(file_path)
            
            # --- 🔥 ВОТ НОВОЕ ИЗМЕНЕНИЕ 🔥 ---
            file_size = os.path.getsize(file_path) 
            # ---------------------------------
            
            file_url = f"{BASE_URL}/{relative_path}"
            
            manifest.append({
                "path": relative_path,
                "hash": file_hash,
                "url": file_url,
                "size": file_size  # <-- И МЫ ДОБАВЛЯЕМ ЕГО СЮДА
            })
            
            print(f"Добавлен: {relative_path} ({file_size} байт)")

    output_path = os.path.join(os.path.dirname(repo_root), OUTPUT_FILE)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4)
        
    print(f"\nГотово! Манифест сохранен в: {output_path}")
    print(f"Всего файлов: {len(manifest)}")

if __name__ == "__main__":
    main()