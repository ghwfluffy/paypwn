from uuid import UUID, uuid4

from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Mapped
from sqlalchemy_utils import UUIDType

from Transfer_pb2 import Transfer as Transfer_pb2

Base: DeclarativeMeta = declarative_base()

class Transfer(Base):
    __tablename__ = 'paybuddy_transfers'

    uuid: Mapped[UUID] = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    sender_uuid: Mapped[UUID] = Column(UUIDType(binary=False), default=uuid4)
    receiver_uuid: Mapped[UUID] = Column(UUIDType(binary=False), default=uuid4)
    transfer_time: Mapped[int] = Column(BigInteger)
    dollars: Mapped[int] = Column(BigInteger)
    cents: Mapped[int] = Column(Integer)
    notes: Mapped[str] = Column(String)

    def to_protobuf(self) -> Transfer_pb2:
        transfer = Transfer_pb2()
        transfer.uuid = str(self.uuid)
        transfer.sender_uuid = str(self.sender_uuid)
        transfer.receiver_uuid = str(self.receiver_uuid)
        transfer.transfer_time = int(self.transfer_time)
        transfer.dollars = int(self.dollars)
        transfer.cents = int(self.cents)
        transfer.notes = str(self.notes)
        return transfer

    @classmethod
    def from_protobuf(cls, transfer: Transfer_pb2) -> 'Transfer':
        return cls(
            uuid=UUID(transfer.uuid),
            sender_uuid=UUID(transfer.sender_uuid),
            receiver_uuid=UUID(transfer.receiver_uuid),
            transfer_time=transfer.transfer_time,
            dollars=transfer.dollars,
            cents=transfer.cents,
            notes=transfer.notes,
        )

    @classmethod
    def create(cls, engine: Engine) -> None:
        Base.metadata.create_all(engine)
