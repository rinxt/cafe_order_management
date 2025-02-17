import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Класс для хранения конфигурационных параметров.

    Атрибуты:
        SECRET_KEY (str): Секретный ключ для шифрования данных.
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    if not SECRET_KEY:
        raise ValueError("Необходимо указать SECRET_KEY в .env файле.")
    if not isinstance(SECRET_KEY, str):
        raise TypeError("SECRET_KEY должен быть строкой.")