import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String ,ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_engine("sqlite:///mymain.db", echo=True)


class User(Base):
    __tablename__ = "users"
    
    username = Column(String, primary_key=True)
    password = Column(String)

    def __repr__(self):
        return "<User(username='%s')>" % (
            self.username,
        )

class Conference(Base):
    __tablename__ = "conferences"
    
    # owner = Column(String, ForeignKey('users.username'))
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    Capacity = Column(Integer)
    items = Column(String)


    def __repr__(self):
        return "<User(title='%s')>" % (
            self.title,
        )


        
Base.metadata.create_all(engine)

