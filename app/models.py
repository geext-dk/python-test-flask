from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
import itertools
from config import Config

ADMIN_LOGIN = "admin"

sql_engine = create_engine(Config.POSTGRES_CONNECTION, echo=True)
Session = sessionmaker(bind=sql_engine)

Base = declarative_base()

# недоенум для удобства сравнивания. Можно было бы отнаследовать от Enum, но в данном приложении не очень-то нужно
class Role:
    USER = 0
    ADMIN = 1

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    # роль - целое число. Можно было бы использовать Enum, но для этого нужно создавать свой тип, т. е. встроенной
    # поддержки нет в SQLAlchemy. Целым числом гораздо проще, тем более в БД оно все равно так и будет храниться
    role = Column(Integer)

class SampleData(Base):
    __tablename__ = "sample_data"

    id = Column(Integer, primary_key=True)
    name = Column(String)

# Метод первоначального заполнения БД
# Если в БД не будет админа при запуске, или всех SampleData, то они создадутся заново
def seed(engine):
    with engine.connect() as conn:
        session = Session(bind=conn)

        # Позволяет создать все таблицы, которых нет
        Base.metadata.create_all(engine)

        # демонстрация использования raw SQL
        result = conn.execute(f"SELECT * FROM users WHERE login = '{ADMIN_LOGIN}'").first()
        if result is None:
            # демонстрация использования ORM
            admin = User(login="admin", password="admin", role=1)
            session.add(admin)
            session.commit()
        
        # Снова raw-SQL
        result = conn.execute(f"SELECT * FROM sample_data").first()
        if result is None:
            # Опять raw-SQL
            conn.execute("INSERT INTO sample_data VALUES " + str.join(', ',  map(
                lambda x: f"({x}, 'Test {x}')",
                itertools.chain(range(1, 11), range(31, 41)))))

