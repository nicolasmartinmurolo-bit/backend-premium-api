import os

OUTPUT_FILE = "proyecto_completo.txt"
VALID_EXTENSIONS = (".py", ".env", ".ini", ".md", ".json", ".txt")
EXCLUDE_DIRS = {".venv", "__pycache__", ".git", ".pytest_cache", "alembic/versions"}

def export_project():
    print("Iniciando empaquetado del proyecto...")
    count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8", errors="ignore") as outfile:
        for root, dirs, files in os.walk("."):
            # Excluimos carpetas no deseadas modificando dirs in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file.endswith(VALID_EXTENSIONS) and file != OUTPUT_FILE:
                    file_path = os.path.join(root, file)
                    print(f"Procesando: {file_path}")
                    
                    outfile.write(f"\n\n{'='*80}\n")
                    outfile.write(f"ARCHIVO: {file_path}\n")
                    outfile.write(f"{'='*80}\n\n")
                    
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                            outfile.write(infile.read())
                        count += 1
                    except Exception as e:
                        outfile.write(f"[Error al leer el archivo: {e}]\n")
                        
    print(f"\n¡Éxito total! Se empaquetaron {count} archivos en: {OUTPUT_FILE}")

if __name__ == "__main__":
    export_project()