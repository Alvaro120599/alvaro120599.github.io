from sqlalchemy import Column, Integer, String
#from yourapplication.database import Base


class User(Base):
    
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    last_name = Column(String(150))
    age = Column(Integer)
    language = Column(String(150))

    def __init__(self, name=None, age=None, language=None):
        self.name = name
        self.age=age
        self.language=language

    def __repr__(self):
        return f'<User {self.name!r}>'


class Message(Base):
    
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(String(150))
    
    def __repr__(self):
        return f'<Message {self.id!r}>'


# User.query.all() # users
# User.query.filter(User.name == '{}'.format(name)).first() # user_by_name