import os
import subprocess

def run_git_push():
    # 1. Запрашиваем ссылку на репозиторий и сообщение к коммиту
    repo_url = input("Введите ссылку на GitHub репозиторий (или нажмите Enter, если уже привязано): ").strip()
    commit_message = input("Введите описание изменений (по умолчанию 'Quick update'): ").strip() or "Quick update"

    try:
        # Проверяем, инициализирован ли git
        if not os.path.exists(".git"):
            print("📦 Инициализация Git...")
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "branch", "-M", "main"], check=True)

        # Добавляем изменения
        subprocess.run(["git", "add", "."], check=True)

        # Делаем коммит
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Если введена ссылка, привязываем удаленный репозиторий
        if repo_url:
            # Пытаемся добавить origin, если не получится — меняем существующий
            try:
                subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)

        # Отправляем данные
        print("🚀 Отправка файлов на GitHub...")
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        print("✅ Готово! Проект на GitHub.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при выполнении команды: {e}")
    except Exception as e:
        print(f"❓ Что-то пошло не так: {e}")

if __name__ == "__main__":
    run_git_push()