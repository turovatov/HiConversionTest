from db.connection import db_mgr


class BaseDataManager(object):
    """
    Базовый класс для менеджеров, работающих с таблицами БД
    """

    table = None

    @staticmethod
    def as_dict(row) -> dict or None:
        """
        Представляем ORM в виде словаря
        :param row: ORM объект
        :return:
        """
        if row:
            columns = row.__table__.columns.keys()
            return dict((col, getattr(row, col)) for col in columns)
        return None

    def get_table(self):
        """
        Прочитать значение "Шаблон письма".
        Если не указали, то генерируем ошибку
        :return:
        """
        if not self.table:
            raise NotImplementedError('Table property is not defined')
        return self.table

    def get_by(self, **kwargs) -> dict:
        """
        Выбрать запись из таблицы по параметрам
        :param kwargs: ИД пользователя
        :return:
        """
        with db_mgr.session_scope() as session:
            table = self.get_table()
            iter_ = session.query(table)
            for col, value in kwargs.items():
                col = 'id' if col == '_id' else col
                iter_ = iter_.filter(getattr(table, col) == value)
            iter_ = iter_.first()
            return self.as_dict(iter_)

    def add(self, **kwargs) -> dict:
        """
        Добавить запись в таблицу
        :param kwargs: Данные для создания
        :return:
        """
        with db_mgr.session_scope() as session:
            table = self.get_table()
            orm_obj = table(**kwargs)
            session.add(orm_obj)
            session.flush()
            return self.as_dict(orm_obj)

    def update(self, _id: int, **kwargs) -> dict:
        """
        Обновить запись в таблице
        :param _id: ID записи
        :param kwargs: Данные для создания
        :return:
        """
        with db_mgr.session_scope() as session:
            table = self.get_table()
            orm_obj = session.query(table) \
                .filter(table.id == _id) \
                .first()

            for col, value in kwargs.items():
                setattr(orm_obj, col, value)

            session.flush()
            return self.as_dict(orm_obj)
