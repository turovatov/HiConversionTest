import os

import yaml


class ConfigManager(object):
    """
    Менеджер работы с конфигурацией
    """

    def __init__(self):
        self.default_filename = 'config.yaml'
        self.filename = None
        self.values = None

    def get_config_file(self, name: str) -> str:
        """
        Получаем полное имя файла конфигурации
        :param name: Краткое имя файла
        :return:
        """
        return '/'.join([os.getcwd(), name or self.default_filename])

    def init_values(self, filename: str) -> None:
        """
        Зачитать настройки из файла
        :param filename: Полное имя файла
        :return:
        """
        with open(self.get_config_file(name=filename), 'r') as f:
            try:
                self.values = yaml.load(f)
            except yaml.YAMLError as exc:
                print(exc)

    def add_value(self, key, value):
        """
        Добавляем значение в конфигурацию
        :param key: Ключ
        :param value: Значение
        :return:
        """
        self.values[key] = value

    def get_db_values(self):
        """
        Получить из конфигурации настройки БД
        :return:
        """
        return self.values.get('database')

    def get_smtp_values(self):
        """
        Получить из конфигурации настройки SMTP-сервера
        :return:
        """
        return self.values.get('smtp')

    def get_debug(self):
        """
        Получить из конфигурации настройки режима запуска
        :return:
        """
        return self.values.get('debug')


config_mgr = ConfigManager()
