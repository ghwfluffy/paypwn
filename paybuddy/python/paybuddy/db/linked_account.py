from uuid import UUID, uuid4
from typing import Optional

from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils import UUIDType

from paybuddy_pb.LinkedAccount_pb2 import AccountType as AccountType_pb2
from paybuddy_pb.LinkedAccount_pb2 import LinkedAccount as LinkedAccount_pb2
from paybuddy_pb.LinkedAccount_pb2 import CardInformation as CardInformation_pb2
from paybuddy_pb.LinkedAccount_pb2 import BankInformation as BankInformation_pb2

Base: DeclarativeMeta = declarative_base()

class BankInformation(Base):
    __tablename__ = 'paybuddy_bank_information'

    account_uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), ForeignKey('paybuddy_linked_accounts.uuid'), primary_key=True)
    bank: Mapped[str] = mapped_column(String)
    routing: Mapped[str] = mapped_column(String)
    account: Mapped[str] = mapped_column(String)

    linked_account: Mapped['LinkedAccount'] = relationship(
        "LinkedAccount",
        back_populates="bank_information",
    )

class CardInformation(Base):
    __tablename__ = 'paybuddy_card_information'

    account_uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), ForeignKey('paybuddy_linked_accounts.uuid'), primary_key=True)
    cardholder: Mapped[str] = mapped_column(String)
    account_number: Mapped[str] = mapped_column(String)
    cvv: Mapped[int] = mapped_column(Integer)
    expiration_month: Mapped[int] = mapped_column(Integer)
    expiration_year: Mapped[int] = mapped_column(Integer)

    linked_account: Mapped['LinkedAccount'] = relationship(
        "LinkedAccount",
        back_populates="card_information",
    )

class LinkedAccount(Base):
    __tablename__ = 'paybuddy_linked_accounts'

    uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), primary_key=True, default=uuid4)
    user_uuid: Mapped[UUID] = mapped_column(UUIDType(binary=False), default=uuid4)
    account_name: Mapped[str] = mapped_column(String)
    account_type: Mapped[str] = mapped_column(String)
    rank: Mapped[int] = mapped_column(Integer)
    verified: Mapped[bool] = mapped_column(Boolean)

    bank_information: Mapped[Optional['BankInformation']] = relationship(
        "BankInformation",
        uselist=False,
        back_populates="linked_account",
        cascade="all, delete-orphan"
    )

    card_information: Mapped[Optional['CardInformation']] = relationship(
        "CardInformation",
        uselist=False,
        back_populates="linked_account",
        cascade="all, delete-orphan"
    )

    def to_protobuf(self) -> LinkedAccount_pb2:
        account = LinkedAccount_pb2()
        account.uuid = str(self.uuid)
        account.user_uuid = str(self.user_uuid)
        account.account_name = self.account_name
        account.account_type = AccountType_pb2.Value(str(self.account_type))
        account.rank = self.rank
        account.verified = self.verified
        if self.account_type == AccountType_pb2.BankAccount and self.bank_information:
            account.bank_information.bank = self.bank_information.bank
            account.bank_information.routing = self.bank_information.routing
            account.bank_information.account = self.bank_information.account
        elif self.account_type == AccountType_pb2.BankCard and self.card_information:
            account.card_information.cardholder = self.card_information.cardholder
            account.card_information.account_number = self.card_information.account_number
            account.card_information.cvv = self.card_information.cvv
            account.card_information.expiration_month = self.card_information.expiration_month
            account.card_information.expiration_year = self.card_information.expiration_year
        return account

    @classmethod
    def from_protobuf(cls, account: LinkedAccount_pb2) -> 'LinkedAccount':
        bank_information = None
        card_information = None
        if account.account_type == AccountType_pb2.BankAccount:
            bank_information = BankInformation()
            bank_information.account_uuid = UUID(account.uuid)
            bank_information.bank = account.bank_information.bank
            bank_information.routing = account.bank_information.routing
            bank_information.account = account.bank_information.account
        elif account.account_type == AccountType_pb2.BankCard:
            card_information = CardInformation()
            card_information.account_uuid = UUID(account.uuid)
            card_information.cardholder = account.card_information.cardholder
            card_information.account_number = account.card_information.account_number
            card_information.cvv = account.card_information.cvv
            card_information.expiration_month = account.card_information.expiration_month
            card_information.expiration_year = account.card_information.expiration_year
        ret = cls()
        ret.uuid = UUID(account.uuid)
        ret.user_uuid = UUID(account.user_uuid)
        ret.account_name = account.account_name
        ret.account_type = AccountType_pb2.Name(account.account_type)
        ret.rank = account.rank
        ret.verified = account.verified
        ret.bank_information = bank_information
        ret.card_information = card_information
        return ret

    @classmethod
    def create(cls, engine: Engine) -> None:
        Base.metadata.create_all(engine)
