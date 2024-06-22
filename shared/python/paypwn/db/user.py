from uuid import UUID, uuid4

from sqlalchemy import String, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from paypwn_pb.User_pb2 import User as User_pb2
from paypwn_pb.User_pb2 import LoginActivity as LoginActivity_pb2
from paypwn_pb.Site_pb2 import Site as Site_pb2

Base: DeclarativeMeta = declarative_base()

class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), primary_key=True, default=uuid4)
    site: Mapped[str] = mapped_column(String)
    bot: Mapped[bool] = mapped_column(Boolean)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    mobile_number: Mapped[str] = mapped_column(String)
    given_name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)

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
        ret = cls()
        ret.uuid = UUID(user.uuid)
        ret.site = Site_pb2.Name(user.site)
        ret.bot = user.bot
        ret.username = user.username
        ret.password = user.password
        ret.email = user.email
        ret.mobile_number = user.mobile_number
        ret.given_name = user.given_name
        ret.surname = user.surname
        ret.address = user.address
        return ret

    @classmethod
    def create(cls, engine: Engine) -> None:
        Base.metadata.create_all(engine)

class LoginActivity(Base):
    __tablename__ = 'login_activity'

    uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), primary_key=True, default=uuid4)
    user_uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), default=uuid4)
    login_time: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    success: Mapped[bool] = mapped_column(Boolean)
    ip_address: Mapped[str] = mapped_column(String)

    def to_protobuf(self) -> LoginActivity_pb2:
        entry = LoginActivity_pb2()
        entry.uuid = str(self.uuid)
        entry.user_uuid = str(self.user_uuid)
        entry.login_time = int(self.login_time)
        entry.success = bool(self.success)
        entry.ip_address = str(self.ip_address)
        return entry

    @classmethod
    def from_protobuf(cls, entry: LoginActivity_pb2) -> 'LoginActivity':
        ret = cls()
        ret.uuid = UUID(entry.uuid)
        ret.user_uuid = UUID(entry.user_uuid)
        ret.login_time = entry.login_time
        ret.success = entry.success
        ret.ip_address = entry.ip_address
        return ret

    @classmethod
    def create(cls, engine: Engine) -> None:
        Base.metadata.create_all(engine)
