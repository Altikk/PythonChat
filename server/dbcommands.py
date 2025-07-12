from sqlalchemy import create_engine, select
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, sessionmaker
import os
from typing import List

current_file_path = os.path.abspath(__file__)
db_path = os.path.dirname(current_file_path)

class Base(DeclarativeBase):
    """Базовый класс для декларативных моделей SQLAlchemy."""
    pass

class Messages(Base):
    """Модель таблицы messages для хранения сообщений."""
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column()


def main() -> None:
    """
    Инициализирует базу данных и создает все таблицы, определенные в моделях.
    
    Создает файл базы данных SQLite в той же директории, где находится скрипт,
    и создает все таблицы, унаследованные от Base.
    """
    engine = create_engine(f"sqlite:///{db_path}/messages.db")
    Base.metadata.create_all(bind=engine)

def add_message_to_db(message: str) -> None:
    """
    Добавляет новое сообщение в базу данных.
    
    Args:
        message (str): Текст сообщения для добавления в базу данных.
    """
    engine = create_engine(f"sqlite:///{db_path}/messages.db")
    Session = sessionmaker(bind=engine)
    message = Messages(message=message)
    with Session() as session:
        session.add(message)
        session.commit()

def get_history() -> List[str]:
    """
    Получает историю всех сообщений из базы данных.
    
    Returns:
        List[str]: Список всех сообщений в обратном порядке (последнее сообщение первым).
    """
    data = []
    engine = create_engine(f"sqlite:///{db_path}/messages.db")
    Session = sessionmaker(bind=engine)
    selected = select(Messages)
    with Session() as session:
        messages = session.scalars(selected).all()
    for i in messages:
        data.append(i.message)
    return data[::-1]

if __name__ == "__main__":
    main()