import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID as PSQL_UUID
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.engine.base import Engine
from sqlalchemy_utils import UUIDType

from paypwn.User_pb2 import User as User_pb2
from paypwn.Site_pb2 import Site as Site_pb2

Base: DeclarativeMeta = declarative_base()

class User(Base):
    __tablename__ = 'users'

    uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    site = Column(String)
    bot = Column(Boolean)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    mobile_number = Column(String)
    given_name = Column(String)
    surname = Column(String)
    address = Column(String)

    def to_protobuf(self) -> User_pb2:
        user = User_pb2()
        user.uuid = str(self.uuid)
        user.site = Site_pb2.Value(str(self.site))
        user.bot = bool(self.bot)
        user.username = str(self.username)
        user.password = str(self.password)
        user.mobile_number = str(self.mobile_number)
        user.given_name = str(self.given_name)
        user.surname = str(self.surname)
        user.address = str(self.address)
        return user

    @classmethod
    def from_protobuf(cls, user: User_pb2) -> 'User':
        return cls(
            uuid=uuid.UUID(user.uuid),
            site=Site_pb2.Name(user.site),
            bot=user.bot,
            username=user.username,
            password=user.password,
            email=user.email,
            mobile_number=user.mobile_number,
            given_name=user.given_name,
            surname=user.surname,
            address=user.address,
        )

    @classmethod
    def create(cls, engine: Engine) -> None:
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()

        Base.metadata.create_all(engine)
