import os
import subprocess

def run_git_push():
    repo_url = input("Ссылка на GitHub: ").strip()
    commit_message = input("Описание (Enter для 'Quick update'): ").strip() or "Quick update"

    try:
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)

        # Переименовываем ветку в main, чтобы избежать конфликтов
        subprocess.run(["git", "branch", "-M", "main"], check=True)

        subprocess.run(["git", "add", "."], check=True)

        # Коммит может не сработать, если нет изменений
        subprocess.run(["git", "commit", "-m", commit_message])

        if repo_url:
            # Обновляем URL репозитория (даже если он уже существует)
            subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=False)
            # Если set-url не сработал (репозитория еще нет), пробуем add
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=False)

        print("🚀 Отправка на GitHub...")
        # Принудительно отправляем текущую ветку main
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        print("✅ Успешно!")

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка Git: {e}")

if __name__ == "__main__":
    run_git_push()