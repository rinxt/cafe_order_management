import os
import sys

def main():
    """Главная функция Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_order_management.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. "
            "Убедитесь, что Django установлен и активировано виртуальное окружение. "
            "Подробности: {}".format(exc)
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()