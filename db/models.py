from sqlalchemy import Column, Integer, String


from db_config import Base, sessionmanager


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True, nullable=True)
    name = Column(String)
    inn = Column(String, nullable=True)
    organization_name = Column(String)


def create_user(user_data: dict):
    user = User(**user_data)
    db = sessionmanager()
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user
