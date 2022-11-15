from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.types import Date
from marshmallow import Schema, fields
from config import Base

'''models for users'''
class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    email = Column(String(50), unique=True)
    password = Column(String(3000), nullable=False)

    def __repr__(self):
        return 'id: {}, name: {}, email: {}, password: {}'.format(
            self.id, 
            self.name,
            self.email,
            self.password
            )


'''schema for user model'''
class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()