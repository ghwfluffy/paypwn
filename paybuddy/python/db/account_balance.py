import uuid

from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.engine.base import Engine
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import Mapped

from AccountBalance_pb2 import AccountBalance as AccountBalance_pb2

Base: DeclarativeMeta = declarative_base()

class AccountBalance(Base):
    __tablename__ = 'paybuddy_account_balances'

    user_uuid: Mapped[uuid.UUID] = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    current_dollars: Mapped[int] = Column(BigInteger)
    current_cents: Mapped[int] = Column(BigInteger)

    def to_protobuf(self) -> AccountBalance_pb2:
        balance = AccountBalance_pb2()
        balance.user_uuid = str(self.user_uuid)
        balance.current_dollars = int(self.current_dollars)
        balance.current_cents = int(self.current_cents)
        return balance

    @classmethod
    def from_protobuf(cls, balance: AccountBalance_pb2) -> 'AccountBalance':
        return cls(
            user_uuid=uuid.UUID(balance.user_uuid),
            current_dollars=int(balance.current_dollars),
            current_cents=int(balance.current_cents),
        )

    @classmethod
    def create(cls, engine: Engine) -> None:
        Base.metadata.create_all(engine)
