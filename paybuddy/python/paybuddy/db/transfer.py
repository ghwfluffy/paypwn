from uuid import UUID, uuid4

from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import UUIDType # type: ignore

from paybuddy_pb.Transfer_pb2 import Transfer as Transfer_pb2

Base: DeclarativeMeta = declarative_base()

class Transfer(Base):
    __tablename__ = 'paybuddy_transfers'

    uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), primary_key=True, default=uuid4)
    sender_uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), default=uuid4)
    receiver_uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), default=uuid4)
    transfer_time: Mapped[int] = mapped_column(BigInteger)
    dollars: Mapped[int] = mapped_column(BigInteger)
    cents: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(String)

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
        ret = cls()
        ret.uuid = UUID(transfer.uuid)
        ret.sender_uuid = UUID(transfer.sender_uuid)
        ret.receiver_uuid = UUID(transfer.receiver_uuid)
        ret.transfer_time = transfer.transfer_time
        ret.dollars = transfer.dollars
        ret.cents = transfer.cents
        ret.notes = transfer.notes
        return ret

    @classmethod
    def create(cls, engine: Engine) -> None:
        Base.metadata.create_all(engine)
