from typing import Any, Optional
import datetime
import decimal

from sqlalchemy import CHAR, Column, DECIMAL, Date, DateTime, Float, Identity, Index, Integer, LargeBinary, NCHAR, Numeric, PrimaryKeyConstraint, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import MONEY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


t_AC = Table(
    'AC', Base.metadata,
    Column('AC', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AName', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ADesc', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AN', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LT', String(255, 'SQL_Latin1_General_CP1_CI_AS'))
)


class APP(Base):
    __tablename__ = 'APP'
    __table_args__ = (
        PrimaryKeyConstraint('AppId', name='PK_APP'),
    )

    AppId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ReqNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    APPDT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    APPTM: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class APPI(Base):
    __tablename__ = 'APPI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_APPI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    AppId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    GRP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ItemCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    BP: Mapped[Optional[Any]] = mapped_column(MONEY)
    DL: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    RT: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))


class ASR(Base):
    __tablename__ = 'ASR'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_ASR'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    cat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cqno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    payee: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    acc: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    bal: Mapped[Optional[Any]] = mapped_column(MONEY)


class AttLog(Base):
    __tablename__ = 'AttLog'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_AttLog'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    WK: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class AttLogW(Base):
    __tablename__ = 'AttLogW'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_AttLogW'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    D1: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D2: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D3: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D4: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D5: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D6: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D7: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    wk: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class BAccState(Base):
    __tablename__ = 'BAccState'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_BAccState'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AccNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    DR: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR: Mapped[Optional[Any]] = mapped_column(MONEY)
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))


t_BBF = Table(
    'BBF', Base.metadata,
    Column('Dt', DateTime, nullable=False),
    Column('Usr', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BBF', MONEY),
    Column('EDt', DateTime),
    Column('EBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Notes', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RAmt', MONEY),
    Column('RNotes', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('bf', MONEY)
)


class BCat(Base):
    __tablename__ = 'BCat'
    __table_args__ = (
        PrimaryKeyConstraint('CID', name='PK_BCat'),
    )

    CID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CATNAME: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class BGRP(Base):
    __tablename__ = 'BGRP'
    __table_args__ = (
        PrimaryKeyConstraint('GName', name='PK_BGRP'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    GName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class BOQ(Base):
    __tablename__ = 'BOQ'
    __table_args__ = (
        PrimaryKeyConstraint('BOQId', name='PK_BOQ'),
    )

    BOQId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    BDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    BTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    BBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    BTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    UrtBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class BOQI(Base):
    __tablename__ = 'BOQI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_BOQI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    BOQID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    BP: Mapped[Optional[Any]] = mapped_column(MONEY)
    QTY: Mapped[Optional[float]] = mapped_column(Float(53))
    ConPrice: Mapped[Optional[Any]] = mapped_column(MONEY)
    Margin: Mapped[Optional[Any]] = mapped_column(MONEY)
    Source: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RQ: Mapped[Optional[float]] = mapped_column(Float(53))
    ATH: Mapped[Optional[float]] = mapped_column(Float(53))
    DL: Mapped[Optional[float]] = mapped_column(Float(53))
    RT: Mapped[Optional[float]] = mapped_column(Float(53))
    UrtBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class BQGLog(Base):
    __tablename__ = 'BQGLog'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_BQGLog'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    BQNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    GRP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EQTY: Mapped[Optional[float]] = mapped_column(Float(53))
    NQTY: Mapped[Optional[float]] = mapped_column(Float(53))
    QTY: Mapped[Optional[float]] = mapped_column(Float(53))
    CT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class BQGRP(Base):
    __tablename__ = 'BQGRP'
    __table_args__ = (
        PrimaryKeyConstraint('BOQNO', 'GRP', name='PK_BQGRP'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    BOQNO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    GRP: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    QTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    REQ: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ATH: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    RTN: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    DL: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    BAL: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class BRECON(Base):
    __tablename__ = 'BRECON'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_BRECON'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    AccNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Mon: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Det: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Amt1: Mapped[Optional[Any]] = mapped_column(MONEY)
    Amt2: Mapped[Optional[Any]] = mapped_column(MONEY)


class BRecon2(Base):
    __tablename__ = 'BRecon2'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_BRecon2'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    month: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    yr: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    accno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    bbs: Mapped[Optional[Any]] = mapped_column(MONEY)
    up: Mapped[Optional[Any]] = mapped_column(MONEY)
    uc: Mapped[Optional[Any]] = mapped_column(MONEY)
    bc: Mapped[Optional[Any]] = mapped_column(MONEY)
    bcb: Mapped[Optional[Any]] = mapped_column(MONEY)
    ecb: Mapped[Optional[Any]] = mapped_column(MONEY)
    diff: Mapped[Optional[Any]] = mapped_column(MONEY)


class BSPay(Base):
    __tablename__ = 'BSPay'
    __table_args__ = (
        PrimaryKeyConstraint('BNo', name='PK_BSPay'),
    )

    BNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PModeNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CB: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PDT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    baccno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cqdt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    cqb: Mapped[Optional[int]] = mapped_column(Integer)
    cbdt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    cbu: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    p: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0), server_default=text('((0))'))


class BTAcc(Base):
    __tablename__ = 'BTAcc'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_BTAcc'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    edate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    tdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    tfrom: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    tvote: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    tto: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    ttovote: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    amt: Mapped[Optional[Any]] = mapped_column(MONEY)


class BTran(Base):
    __tablename__ = 'BTran'
    __table_args__ = (
        PrimaryKeyConstraint('TraNo', name='PK_BTran'),
    )

    TraNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    AccNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class BTranI(Base):
    __tablename__ = 'BTranI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_BTranI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Mode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CqNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Drawer: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    MDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    Narrate: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    MStatus: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CStatus: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CB: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class Bank(Base):
    __tablename__ = 'Bank'
    __table_args__ = (
        PrimaryKeyConstraint('Bank', name='PK_Bank'),
    )

    Bank: Mapped[str] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class BankAcc(Base):
    __tablename__ = 'BankAcc'
    __table_args__ = (
        PrimaryKeyConstraint('AccNo', name='PK_BankAcc'),
    )

    AccNo: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    AccName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Bank_: Mapped[Optional[str]] = mapped_column('Bank', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Branch: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Balance: Mapped[Optional[Any]] = mapped_column(MONEY)
    GRP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    act: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    mp: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class Bt(Base):
    __tablename__ = 'Bt'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_Bt'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AccNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CIn: Mapped[Optional[Any]] = mapped_column(MONEY)
    COut: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CA(Base):
    __tablename__ = 'CA'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CA'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Cashier: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    MONIN: Mapped[Optional[Any]] = mapped_column(MONEY)
    MONOUT: Mapped[Optional[Any]] = mapped_column(MONEY)


class CAH(Base):
    __tablename__ = 'CAH'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_CAH'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    AMT: Mapped[Optional[Any]] = mapped_column(MONEY)


class CB(Base):
    __tablename__ = 'CB'
    __table_args__ = (
        PrimaryKeyConstraint('recid', name='PK_CB_1'),
    )

    recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Tm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    MCat: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    MCat2: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    cin: Mapped[Optional[Any]] = mapped_column(MONEY)
    cout: Mapped[Optional[Any]] = mapped_column(MONEY)
    bin: Mapped[Optional[Any]] = mapped_column(MONEY)
    bout: Mapped[Optional[Any]] = mapped_column(MONEY)
    accno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    dby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    MCat3: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    GRP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CCInv(Base):
    __tablename__ = 'CCInv'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CCInv'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Idno: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TraDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CRefNo: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Detail: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Paid: Mapped[Optional[Any]] = mapped_column(MONEY)
    Balance: Mapped[Optional[Any]] = mapped_column(MONEY)
    NBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    Ret: Mapped[Optional[Any]] = mapped_column(MONEY)


class CCustPayPur(Base):
    __tablename__ = 'CCustPayPur'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_CCustPayPur'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CustId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PurchaseDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PurchaseTraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PurchaseAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    PayDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PayTrano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PayAmount: Mapped[Optional[Any]] = mapped_column(MONEY)


class CCustPayment(Base):
    __tablename__ = 'CCustPayment'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_CCustPayment'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PayDate: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    PayMode: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CustId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CCustPurchase(Base):
    __tablename__ = 'CCustPurchase'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_CCustPurchase'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PurDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    CustId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CCustStatement(Base):
    __tablename__ = 'CCustStatement'
    __table_args__ = (
        PrimaryKeyConstraint('CustId', name='PK_CCustStatement'),
    )

    CustId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    Obal: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalPurchase: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalPay: Mapped[Optional[Any]] = mapped_column(MONEY)
    CurrBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    StartDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EndDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class CDBAL(Base):
    __tablename__ = 'CDBAL'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_CDBAL'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ACC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DTIM: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    BAL: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CDInv(Base):
    __tablename__ = 'CDInv'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CDInv'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Idno: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TraDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CRefNo: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Detail: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Paid: Mapped[Optional[Any]] = mapped_column(MONEY)
    Balance: Mapped[Optional[Any]] = mapped_column(MONEY)
    NBal: Mapped[Optional[Any]] = mapped_column(MONEY)


class CDPP(Base):
    __tablename__ = 'CDPP'
    __table_args__ = (
        PrimaryKeyConstraint('AccNo', name='PK_CDPP'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    AccNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))


class CExpense(Base):
    __tablename__ = 'CExpense'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CExpense'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EntryDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ECat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(3000, 'SQL_Latin1_General_CP1_CI_AS'))
    PAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    ABy: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    PTo: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Cyear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ChequeNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CInv(Base):
    __tablename__ = 'CInv'
    __table_args__ = (
        PrimaryKeyConstraint('InvNo', name='PK_CInv'),
    )

    InvNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CallId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    InvDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    InvTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    InvTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    INvBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CVAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    CGTOTAL: Mapped[Optional[Any]] = mapped_column(MONEY)
    P: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CInvItem(Base):
    __tablename__ = 'CInvItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CInvItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    InvNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    BP: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)
    Source: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemVat: Mapped[Optional[Any]] = mapped_column(MONEY)


class CItem(Base):
    __tablename__ = 'CItem'
    __table_args__ = (
        PrimaryKeyConstraint('ItemId', name='PK_CItem'),
    )

    ItemId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CNoteNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    SubTotal: Mapped[Optional[Any]] = mapped_column(MONEY)


class CLPROJ(Base):
    __tablename__ = 'CLPROJ'
    __table_args__ = (
        PrimaryKeyConstraint('CNO', 'CYEAR', name='PK_CLPROJ'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    CNO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    CYEAR: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    RETAINVAT: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    VATAMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    WTAXR: Mapped[Optional[float]] = mapped_column(Float(53))
    WTAXAMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    RETAINR: Mapped[Optional[float]] = mapped_column(Float(53))
    RETAINAMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    DTDUE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CD: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class CLog(Base):
    __tablename__ = 'CLog'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CLog'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    MDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    DR: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR: Mapped[Optional[Any]] = mapped_column(MONEY)
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)


class CNote(Base):
    __tablename__ = 'CNote'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CNote'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DTo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ABy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    SaleDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Reason: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))


class COMPP(Base):
    __tablename__ = 'COMPP'
    __table_args__ = (
        PrimaryKeyConstraint('COMP', name='PK_COMPP'),
    )

    COMP: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    GP: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    RP: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    ETR: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))


class COrder(Base):
    __tablename__ = 'COrder'
    __table_args__ = (
        PrimaryKeyConstraint('OrderNo', name='PK_COrder'),
    )

    OrderNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ODate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    OTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    OFrom: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RefNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    VatRate: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Rec: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Dis: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    OQty: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Rebate: Mapped[Optional[Any]] = mapped_column(MONEY)


class COrderItem(Base):
    __tablename__ = 'COrderItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_COrderItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    OrderNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Dest: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NBag: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    SubTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    VATAmt: Mapped[Optional[Any]] = mapped_column(MONEY)
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    Detail: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class COrderPay(Base):
    __tablename__ = 'COrderPay'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_COrderPay'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    OrderNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CqNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Cb: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Cashier: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CPNo(Base):
    __tablename__ = 'CPNo'
    __table_args__ = (
        PrimaryKeyConstraint('PNo', name='PK_CPNo'),
    )

    PNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PById: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PByName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RefNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CPNoD(Base):
    __tablename__ = 'CPNoD'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CPNoD'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    InvNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CPrice(Base):
    __tablename__ = 'CPrice'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CPrice'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CPrice: Mapped[Optional[Any]] = mapped_column(MONEY)


class CQ(Base):
    __tablename__ = 'CQ'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_Cheque'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Debtor: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CqNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    CDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Banked: Mapped[Optional[str]] = mapped_column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'))
    BDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    BTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    BBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Cleared: Mapped[Optional[str]] = mapped_column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'))
    Bounced: Mapped[Optional[str]] = mapped_column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'))
    CON: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PD: Mapped[Optional[str]] = mapped_column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'))
    Charge: Mapped[Optional[Any]] = mapped_column(MONEY)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Cat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cn: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CReceive(Base):
    __tablename__ = 'CReceive'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CReceive'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    OrderNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DocNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RQty: Mapped[Optional[float]] = mapped_column(Float(53))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CReceiveCredit(Base):
    __tablename__ = 'CReceive_Credit'
    __table_args__ = (
        PrimaryKeyConstraint('trano', name='PK_CReceive_Credit'),
    )

    trano: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 0), Identity(start=1, increment=1), primary_key=True)
    RefNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    id: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 0))
    pmode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    DAllowed: Mapped[Optional[Any]] = mapped_column(MONEY)
    tradate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    chequeno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    dbank: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PN: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CRemit(Base):
    __tablename__ = 'CRemit'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CRemit'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SPerson: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ECash: Mapped[Optional[Any]] = mapped_column(MONEY)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CSM(Base):
    __tablename__ = 'CSM'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_CMS'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    C1: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    C2: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    C3: Mapped[Optional[Any]] = mapped_column(MONEY)
    C4: Mapped[Optional[Any]] = mapped_column(MONEY)


class CStockMonitor(Base):
    __tablename__ = 'CStockMonitor'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_CStockMonitor'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    StockDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CUserlogged: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ItemCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CStock: Mapped[Optional[float]] = mapped_column(Float(53))


class CTPNo(Base):
    __tablename__ = 'CTPNo'
    __table_args__ = (
        PrimaryKeyConstraint('PNo', name='PK_CTPNo'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    PNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    PDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PById: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PByName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RefNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CTPNoD(Base):
    __tablename__ = 'CTPNoD'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CTPNoD'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    InvNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CUB(Base):
    __tablename__ = 'CUB'
    __table_args__ = (
        PrimaryKeyConstraint('ACCNO', name='PK_CUB'),
    )

    ACCNO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    UB: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))


class CV(Base):
    __tablename__ = 'CV'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CV'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EDesc: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    aIn: Mapped[Optional[Any]] = mapped_column(MONEY)
    aOut: Mapped[Optional[Any]] = mapped_column(MONEY)
    aTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    aDBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CVN(Base):
    __tablename__ = 'CVN'
    __table_args__ = (
        PrimaryKeyConstraint('CVN', name='PK_CVN'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    CVN: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    TY: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    budg: Mapped[Optional[Any]] = mapped_column(MONEY)


class CW(Base):
    __tablename__ = 'CW'
    __table_args__ = (
        PrimaryKeyConstraint('WNo', name='PK_CW'),
    )

    WNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Votehead: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EndDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class CWI(Base):
    __tablename__ = 'CWI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CWI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    WNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Rate: Mapped[Optional[Any]] = mapped_column(MONEY)
    Days: Mapped[Optional[float]] = mapped_column(Float(53))
    STotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    Deduction: Mapped[Optional[Any]] = mapped_column(MONEY)
    Net: Mapped[Optional[Any]] = mapped_column(MONEY)
    TRef: Mapped[Optional[Any]] = mapped_column(MONEY)
    AccRef: Mapped[Optional[Any]] = mapped_column(MONEY)
    OT: Mapped[Optional[Any]] = mapped_column(MONEY)


class CWage(Base):
    __tablename__ = 'CWage'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CWage'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    WDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Wno: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CaIO(Base):
    __tablename__ = 'CaIO'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CaIO'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Tm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CIn: Mapped[Optional[Any]] = mapped_column(MONEY)
    COut: Mapped[Optional[Any]] = mapped_column(MONEY)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DComp: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    RBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CallItem(Base):
    __tablename__ = 'CallItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_CallItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CallId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Code: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[float]] = mapped_column(Float(53))
    SubT: Mapped[Optional[Any]] = mapped_column(MONEY)
    Source: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class CashCustomer(Base):
    __tablename__ = 'Cash_Customer'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_Cash_Customer'),
    )

    id: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    address: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    phone: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cperiod: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    balance: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    datedue: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Route: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    SCost: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ScostP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ScostPv: Mapped[Optional[float]] = mapped_column(Float(53))
    CP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CPTel: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IntD: Mapped[Optional[str]] = mapped_column(CHAR(18, 'SQL_Latin1_General_CP1_CI_AS'))
    cD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))
    Email: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class ConPay(Base):
    __tablename__ = 'ConPay'
    __table_args__ = (
        PrimaryKeyConstraint('PayNo', name='PK_ConPay'),
    )

    PayNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ChequeNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_ConState = Table(
    'ConState', Base.metadata,
    Column('RecId', Numeric(18, 0)),
    Column('TDate', DateTime),
    Column('CNO', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('TCLass', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TDesc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DR', Float(53)),
    Column('CR', Float(53))
)


class Contract(Base):
    __tablename__ = 'Contract'
    __table_args__ = (
        PrimaryKeyConstraint('CNo', 'CYear', name='PK_Contract'),
    )

    CNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    CYear: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    Company: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CompanyD: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    CPerson: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CPersonTel: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    LPONo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    InvAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    VATAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    GTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EntryDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DWork: Mapped[Optional[str]] = mapped_column(Unicode(4000, 'SQL_Latin1_General_CP1_CI_AS'))
    CBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    KPLC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CREF: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    VCode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    AmtP: Mapped[Optional[Any]] = mapped_column(MONEY)
    Mat: Mapped[Optional[Any]] = mapped_column(MONEY)
    Sal: Mapped[Optional[Any]] = mapped_column(MONEY)
    M: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    VAR: Mapped[Optional[Any]] = mapped_column(MONEY)
    comp: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class CreditCustomer(Base):
    __tablename__ = 'Credit_Customer'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_Credit_Customer'),
    )

    id: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    address: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    phone: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cperiod: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    balance: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    datedue: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Route: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    SCost: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ScostP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ScostPv: Mapped[Optional[float]] = mapped_column(Float(53))
    CP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CPTel: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IntD: Mapped[Optional[str]] = mapped_column(CHAR(18, 'SQL_Latin1_General_CP1_CI_AS'))
    cD: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))
    Email: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class DAS(Base):
    __tablename__ = 'DAS'
    __table_args__ = (
        PrimaryKeyConstraint('recid', name='PK_DAS'),
    )

    recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    did: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    a30: Mapped[Optional[Any]] = mapped_column(MONEY)
    a60: Mapped[Optional[Any]] = mapped_column(MONEY)
    a90: Mapped[Optional[Any]] = mapped_column(MONEY)
    a120: Mapped[Optional[Any]] = mapped_column(MONEY)
    aover: Mapped[Optional[Any]] = mapped_column(MONEY)
    atotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    UB: Mapped[Optional[Any]] = mapped_column(MONEY)


t_DAllowed = Table(
    'DAllowed', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(start=1, increment=1), nullable=False),
    Column('SaleNo', Numeric(18, 0)),
    Column('Amount', MONEY),
    Column('DDate', DateTime),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


class DDBAL(Base):
    __tablename__ = 'DDBAL'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_DDBAL'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ACC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    BAL: Mapped[Optional[Any]] = mapped_column(MONEY)
    DTIM: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_DF = Table(
    'DF', Base.metadata,
    Column('FID', Numeric(18, 0), Identity(start=1, increment=1), nullable=False),
    Column('FTEXT', Unicode(4000, 'SQL_Latin1_General_CP1_CI_AS'))
)


class DInv(Base):
    __tablename__ = 'DInv'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DInv'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Idno: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TraDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Trano: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CRefNo: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Detail: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Paid: Mapped[Optional[Any]] = mapped_column(MONEY)
    Balance: Mapped[Optional[Any]] = mapped_column(MONEY)
    NBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    Ret: Mapped[Optional[Any]] = mapped_column(MONEY)


class DIssueItem(Base):
    __tablename__ = 'DIssueItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DIssueItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    IDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    IQty: Mapped[Optional[float]] = mapped_column(Float(53))
    SQty: Mapped[Optional[float]] = mapped_column(Float(53))
    RQty: Mapped[Optional[float]] = mapped_column(Float(53))
    Diff: Mapped[Optional[float]] = mapped_column(Float(53))
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Tinqty: Mapped[Optional[float]] = mapped_column(Float(53))
    tqty: Mapped[Optional[float]] = mapped_column(Float(53))


class DLog(Base):
    __tablename__ = 'DLog'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DLog'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    MDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    DR: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR: Mapped[Optional[Any]] = mapped_column(MONEY)
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)


class DOBal(Base):
    __tablename__ = 'DOBal'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DOBal'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    IDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class DPP(Base):
    __tablename__ = 'DPP'
    __table_args__ = (
        PrimaryKeyConstraint('AccNo', name='PK_DPP'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    AccNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))


class DS(Base):
    __tablename__ = 'DS'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DS'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Description: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)


class DState(Base):
    __tablename__ = 'DState'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DState'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TDesc: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Amount2: Mapped[Optional[Any]] = mapped_column(MONEY)


class DT(Base):
    __tablename__ = 'DT'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_DT'),
    )

    DT: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)


class DTL(Base):
    __tablename__ = 'DTL'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DTL'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    NDt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    COn: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CTm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    COMP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class DamagedStock(Base):
    __tablename__ = 'DamagedStock'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_DamagedStock'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ItemCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    DDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EnteredBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    BP: Mapped[Optional[Any]] = mapped_column(MONEY)


class DelPrices(Base):
    __tablename__ = 'DelPrices'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_DelPrices'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Itemcode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    bp: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    nbp: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    spw: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    nspw: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    spr: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    nspr: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    QtyStock: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NQtyStock: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))
    Doneby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class DelRepItem(Base):
    __tablename__ = 'DelRepItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_DelRepItem'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    RepNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ItemPrice: Mapped[Optional[Any]] = mapped_column(MONEY)
    Qty: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ItemCost: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemVAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DelDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class DelReplenishitem(Base):
    __tablename__ = 'DelReplenishitem'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_DelReplenishitem'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    ItemCost: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemVAT: Mapped[Optional[Any]] = mapped_column(MONEY)


class DelReplenishment(Base):
    __tablename__ = 'DelReplenishment'
    __table_args__ = (
        PrimaryKeyConstraint('CNo', name='PK_DelReplenishment'),
    )

    CNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Trano: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    Dmode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DocNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Supplier: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Issuedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DateDue: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Replenishdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    VATAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Doneby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DoneOn: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class DelSale(Base):
    __tablename__ = 'DelSale'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DelSale'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Tradate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Tratype: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Saletype: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IdNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Cashier: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    Cash: Mapped[Optional[Any]] = mapped_column(MONEY)
    Change: Mapped[Optional[Any]] = mapped_column(MONEY)
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DoneOn: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class DelSaleItem(Base):
    __tablename__ = 'DelSaleItem'
    __table_args__ = (
        PrimaryKeyConstraint('Itemno', name='PK_DelSaleItem'),
    )

    Itemno: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Tradate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Itemcode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    Itemcost: Mapped[Optional[Any]] = mapped_column(MONEY)
    Vat: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemBP: Mapped[Optional[Any]] = mapped_column(MONEY)


class Delivery(Base):
    __tablename__ = 'Delivery'
    __table_args__ = (
        PrimaryKeyConstraint('Dno', name='PK_Delivery'),
    )

    Dno: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    Transactedby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Shop: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ShopNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ProjId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ProjName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ITO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CAT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))
    phy: Mapped[Optional[Any]] = mapped_column(MONEY)
    sid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    sname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CASH: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    pdamt: Mapped[Optional[Any]] = mapped_column(MONEY)


class DeliveryItems(Base):
    __tablename__ = 'DeliveryItems'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DeliveryItems'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Pcode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    RTQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ItemPrice: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemVat: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemCost: Mapped[Optional[Any]] = mapped_column(MONEY)
    BP: Mapped[Optional[Any]] = mapped_column(MONEY)
    lp: Mapped[Optional[Any]] = mapped_column(MONEY)
    h: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_Department = Table(
    'Department', Base.metadata,
    Column('DName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('DDesc', Unicode(200, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('HOD', Numeric(18, 0))
)


class Dis(Base):
    __tablename__ = 'Dis'
    __table_args__ = (
        PrimaryKeyConstraint('DisNo', name='PK_Dis'),
    )

    DisNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    OrderNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    DDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    DisQty: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class DisI(Base):
    __tablename__ = 'DisI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_DisI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DisNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Qty: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))


class EG(Base):
    __tablename__ = 'EG'
    __table_args__ = (
        PrimaryKeyConstraint('eg', name='PK_EG'),
    )

    recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1001, increment=1), nullable=False)
    eg: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    EXP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class EItem(Base):
    __tablename__ = 'EItem'
    __table_args__ = (
        PrimaryKeyConstraint('EitemName', name='PK_EItem'),
    )

    EitemName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    VName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_EOD = Table(
    'EOD', Base.metadata,
    Column('Recid', Numeric(18, 0), Identity(start=1, increment=1), nullable=False),
    Column('Dt', DateTime),
    Column('RCat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDet', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amt', MONEY)
)


t_EOM = Table(
    'EOM', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(start=1, increment=1), nullable=False),
    Column('Yr', Numeric(18, 0)),
    Column('Mon', Numeric(18, 0)),
    Column('sdt', DateTime),
    Column('edt', DateTime),
    Column('RCat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDet', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CY', MONEY),
    Column('TD', MONEY),
    Column('CLM', MONEY),
    Column('lms', DateTime),
    Column('lme', DateTime)
)


class EOY(Base):
    __tablename__ = 'EOY'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_YTD'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    FYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Votehead: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DR: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR: Mapped[Optional[Any]] = mapped_column(MONEY)
    DR2: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR2: Mapped[Optional[Any]] = mapped_column(MONEY)
    AE: Mapped[Optional[Any]] = mapped_column(MONEY)
    COM: Mapped[Optional[Any]] = mapped_column(MONEY)
    BCOLL: Mapped[Optional[Any]] = mapped_column(MONEY)
    BCOM: Mapped[Optional[Any]] = mapped_column(MONEY)
    AC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    sg: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class EOY2(Base):
    __tablename__ = 'EOY2'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_EOY2'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    FYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Votehead: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DR: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR: Mapped[Optional[Any]] = mapped_column(MONEY)
    DR2: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR2: Mapped[Optional[Any]] = mapped_column(MONEY)
    AE: Mapped[Optional[Any]] = mapped_column(MONEY)
    COM: Mapped[Optional[Any]] = mapped_column(MONEY)
    BCOLL: Mapped[Optional[Any]] = mapped_column(MONEY)
    BCOM: Mapped[Optional[Any]] = mapped_column(MONEY)
    AC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    sg: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class EV(Base):
    __tablename__ = 'EV'
    __table_args__ = (
        PrimaryKeyConstraint('VName', name='PK_EV'),
    )

    VName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    VDesc: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    eg: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    egid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class EVS(Base):
    __tablename__ = 'EVS'
    __table_args__ = (
        PrimaryKeyConstraint('EVS', name='PK_EVS'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    EVS: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class Emp(Base):
    __tablename__ = 'Emp'
    __table_args__ = (
        PrimaryKeyConstraint('EmpNo', name='PK_Emp'),
    )

    EmpNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    EmpName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EmpIDNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    MStatus: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CTelNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ACName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ACTelNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NSSF: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NHIF: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EmpDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Department: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Designation: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    JobType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    JobGroup: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    GrossSalary: Mapped[Optional[Any]] = mapped_column(MONEY)
    PAdd: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CAdd: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TelNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EMail: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Province: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    District: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Location: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SubLocation: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Village: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Religion: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PPayroll: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PAcc: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Remarks: Mapped[Optional[str]] = mapped_column(Unicode(4000, 'SQL_Latin1_General_CP1_CI_AS'))
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(38, 0))
    DOB: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Bank_: Mapped[Optional[str]] = mapped_column('Bank', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Branch: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class EmpDA(Base):
    __tablename__ = 'EmpDA'
    __table_args__ = (
        PrimaryKeyConstraint('DMonth', 'DYear', 'EmpNo', name='PK_EmpDA'),
    )

    DMonth: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    DYear: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    EmpNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    HA: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    HAAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    MA: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    MAAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    ENSSF: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ENSSFAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    NSSF: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NSSFAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    BIC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    BICA: Mapped[Optional[Any]] = mapped_column(MONEY)
    ARR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ARRA: Mapped[Optional[Any]] = mapped_column(MONEY)
    CWWG: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CWWGAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    PAYE: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PAYEAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    UnionD: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    UnionAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    NHIF: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NHIFAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Elimu: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ElimuAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Rent: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RentAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Advance: Mapped[Optional[str]] = mapped_column(CHAR(50, 'SQL_Latin1_General_CP1_CI_AS'))
    AdvanceAmount: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    COTU: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    COTUA: Mapped[Optional[Any]] = mapped_column(MONEY)
    CIC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CICA: Mapped[Optional[Any]] = mapped_column(MONEY)
    MAD: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    MADA: Mapped[Optional[Any]] = mapped_column(MONEY)
    EWC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    EWCA: Mapped[Optional[Any]] = mapped_column(MONEY)
    CIN: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CINA: Mapped[Optional[Any]] = mapped_column(MONEY)


class EmpF(Base):
    __tablename__ = 'EmpF'
    __table_args__ = (
        PrimaryKeyConstraint('EmpNo', name='PK_EmpF'),
    )

    EmpNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    HA: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    MA: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    ENSSF: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    BIC: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    ARR: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    NSSF: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    PAYE: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    UnionD: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Elimu: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Rent: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Advance: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    NHIF: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    COTU: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Upendo: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    CIC: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    MAD: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    EWC: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    CIN: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))


class EmpKin(Base):
    __tablename__ = 'EmpKin'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_EmpKin'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    KinName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    KinIdNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    KinAdd: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    KinTelNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Relation: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Remarks: Mapped[Optional[str]] = mapped_column(Unicode(254, 'SQL_Latin1_General_CP1_CI_AS'))


class Expiry(Base):
    __tablename__ = 'Expiry'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_Expiry'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    BatchNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    MDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class GDEL(Base):
    __tablename__ = 'GDEL'
    __table_args__ = (
        PrimaryKeyConstraint('DELNO', name='PK_GDEL'),
    )

    DELNO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DELDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DELT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    APPID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class GDELI(Base):
    __tablename__ = 'GDELI'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_GDELI'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DELNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    APPINO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    QTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    PR: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    RT: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    Cat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class GEN(Base):
    __tablename__ = 'GEN'
    __table_args__ = (
        PrimaryKeyConstraint('SNO', name='PK_GEN'),
    )

    GID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    SNO: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    CID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    OD: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    LSD: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class GREQ(Base):
    __tablename__ = 'GREQ'
    __table_args__ = (
        PrimaryKeyConstraint('ReqNo', name='PK_GREQ'),
    )

    ReqNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    BQNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RBY: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RTIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RUSER: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class GREQI(Base):
    __tablename__ = 'GREQI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_GREQI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    REQNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    GRP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    QTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    APP_: Mapped[Optional[float]] = mapped_column('APP', Float(53), server_default=text('((0))'))
    DL: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    RT: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))


class GRT(Base):
    __tablename__ = 'GRT'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_GRT'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    itemcode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    qty: Mapped[Optional[float]] = mapped_column(Float(53))
    gdelino: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    rby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class GSR(Base):
    __tablename__ = 'GSR'
    __table_args__ = (
        PrimaryKeyConstraint('ReqNo', name='PK_GSR'),
    )

    ReqNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    GenId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SBY: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    INV: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    INVDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class GSRItem(Base):
    __tablename__ = 'GSRItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_GSRItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ReqNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    UQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    RQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    BP: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)
    SOURCE: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class GeneralInv(Base):
    __tablename__ = 'GeneralInv'
    __table_args__ = (
        PrimaryKeyConstraint('invno', name='PK_GeneralInv'),
    )

    invno: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    issuedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    particulars: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    issuedto: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    doneby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class GeneralInvPayment(Base):
    __tablename__ = 'GeneralInvPayment'
    __table_args__ = (
        PrimaryKeyConstraint('TraNo', name='PK_GeneralInvPayment'),
    )

    TraNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    InvNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PayDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)


class HS(Base):
    __tablename__ = 'HS'
    __table_args__ = (
        PrimaryKeyConstraint('HSNO', name='PK_HS'),
    )

    HSNO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DT_: Mapped[Optional[datetime.datetime]] = mapped_column('DT', DateTime)
    HBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    HT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    HRE: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Cust: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    SType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    stat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    rd: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    rby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    sno: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    HTY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SSNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    STY: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class HSI(Base):
    __tablename__ = 'HSI'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_HSI'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    HSNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CODE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    INAME: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    QTY: Mapped[Optional[float]] = mapped_column(Float(53))
    PRICE: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    TOT: Mapped[Optional[Any]] = mapped_column(MONEY)
    BP: Mapped[Optional[Any]] = mapped_column(MONEY)
    VTR: Mapped[Optional[float]] = mapped_column(Float(53))
    SALEIN: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class IPD(Base):
    __tablename__ = 'IPD'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_IPD'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SD: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ED: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Status: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class IRItem(Base):
    __tablename__ = 'IRItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_IRItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    RNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class IReturn(Base):
    __tablename__ = 'IReturn'
    __table_args__ = (
        PrimaryKeyConstraint('RNo', name='PK_IReturn'),
    )

    RNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    IDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    REFNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class InvB(Base):
    __tablename__ = 'InvB'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_InvB'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    bdt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    btm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    narr: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    ref: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class InvCallItem(Base):
    __tablename__ = 'InvCallItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_InvCallItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CallId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Code: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[float]] = mapped_column(Float(53))
    SubT: Mapped[Optional[Any]] = mapped_column(MONEY)
    Source: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RQty: Mapped[Optional[float]] = mapped_column(Float(53))
    ItemVat: Mapped[Optional[Any]] = mapped_column(MONEY)


class Issue(Base):
    __tablename__ = 'Issue'
    __table_args__ = (
        PrimaryKeyConstraint('INo', 'IYear', name='PK_Issue'),
    )

    INo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    IYear: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    IDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ITo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    IBy: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    IStatus: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    ITime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ITotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    LpoNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Route: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CUST: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class IssueItem(Base):
    __tablename__ = 'IssueItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_IssueItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    INo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    IYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCOde: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    IQty: Mapped[Optional[float]] = mapped_column(Float(53))
    RQty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    Itemcost: Mapped[Optional[Any]] = mapped_column(MONEY)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class IssueTranfer(Base):
    __tablename__ = 'IssueTranfer'
    __table_args__ = (
        PrimaryKeyConstraint('recid', name='PK_IssueTranfer'),
    )

    recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    F: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    T: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCODE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    QTY: Mapped[Optional[float]] = mapped_column(Float(53))
    tno: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class IssueTransferM(Base):
    __tablename__ = 'IssueTransferM'
    __table_args__ = (
        PrimaryKeyConstraint('TNO', name='PK_IssueTransferM'),
    )

    TNO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DT_: Mapped[Optional[datetime.datetime]] = mapped_column('DT', DateTime)


class LDD(Base):
    __tablename__ = 'LDD'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_LDD'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    src: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    dst: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    dby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class LDDR(Base):
    __tablename__ = 'LDDR'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_LDDR'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    src: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    dst: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    dby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class LN(Base):
    __tablename__ = 'LN'
    __table_args__ = (
        PrimaryKeyConstraint('EmpNo', name='PK_LN'),
    )

    EmpNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    CRate: Mapped[Optional[Any]] = mapped_column(MONEY)
    RP: Mapped[Optional[int]] = mapped_column(Integer)


class LNA(Base):
    __tablename__ = 'LNA'
    __table_args__ = (
        PrimaryKeyConstraint('EmpNo', name='PK_LNA'),
    )

    EmpNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    CRate: Mapped[Optional[Any]] = mapped_column(MONEY)
    RP: Mapped[Optional[int]] = mapped_column(Integer)


class LNH(Base):
    __tablename__ = 'LNH'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_LNH'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)
    LUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Type: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))


class LNHA(Base):
    __tablename__ = 'LNHA'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_LNHA'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)
    LUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Type: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))


class LNHM(Base):
    __tablename__ = 'LNHM'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_LNHM'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)
    LUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Type: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))


class LNI(Base):
    __tablename__ = 'LNI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_ILN'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    InitAmt: Mapped[Optional[Any]] = mapped_column(MONEY)
    InitInstall: Mapped[Optional[Any]] = mapped_column(MONEY)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    NewInstall: Mapped[Optional[Any]] = mapped_column(MONEY)
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class LNIA(Base):
    __tablename__ = 'LNIA'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_ILNA'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    InitAmt: Mapped[Optional[Any]] = mapped_column(MONEY)
    InitInstall: Mapped[Optional[Any]] = mapped_column(MONEY)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    NewInstall: Mapped[Optional[Any]] = mapped_column(MONEY)
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class LNIM(Base):
    __tablename__ = 'LNIM'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_ILNM'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    InitAmt: Mapped[Optional[Any]] = mapped_column(MONEY)
    InitInstall: Mapped[Optional[Any]] = mapped_column(MONEY)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    NewInstall: Mapped[Optional[Any]] = mapped_column(MONEY)
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class LNM(Base):
    __tablename__ = 'LNM'
    __table_args__ = (
        PrimaryKeyConstraint('EmpNo', name='PK_LNM'),
    )

    EmpNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    CRate: Mapped[Optional[Any]] = mapped_column(MONEY)
    RP: Mapped[Optional[int]] = mapped_column(Integer)


class LPO(Base):
    __tablename__ = 'LPO'
    __table_args__ = (
        PrimaryKeyConstraint('LpoNo', name='PK_LPO'),
    )

    LpoNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Notes: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    GT: Mapped[Optional[Any]] = mapped_column(MONEY)
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)


class LPOI(Base):
    __tablename__ = 'LPOI'
    __table_args__ = (
        PrimaryKeyConstraint('Recid', name='PK_lpoi'),
    )

    Recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    LpoNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ICode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    DQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)
    Nar: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IVat: Mapped[Optional[Any]] = mapped_column(MONEY)
    IncExc: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class LPOItem(Base):
    __tablename__ = 'LPOItem'
    __table_args__ = (
        PrimaryKeyConstraint('ArticleID', name='PK_LPOItem'),
    )

    ArticleID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    LPONo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Itemname: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    SubTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    I_E: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TRQty: Mapped[Optional[float]] = mapped_column(Float(53))
    BalQty: Mapped[Optional[float]] = mapped_column(Float(53))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class MAN(Base):
    __tablename__ = 'MAN'
    __table_args__ = (
        PrimaryKeyConstraint('MANID', name='PK_MAN'),
    )

    MANID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    MAN: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class MON(Base):
    __tablename__ = 'MON'
    __table_args__ = (
        PrimaryKeyConstraint('MN', name='PK_MON'),
    )

    MN: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    MName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class MRoll(Base):
    __tablename__ = 'MRoll'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_MRoll'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EMPNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PMONTH: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PYEAR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    VOTEHEAD: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TYPE: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    AMOUNT: Mapped[Optional[Any]] = mapped_column(MONEY)


t_MSale = Table(
    'MSale', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('tratype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('total', MONEY),
    Column('cash', MONEY),
    Column('change', MONEY),
    Column('vat', MONEY),
    Column('SaleTime', DateTime),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InvNo', Numeric(18, 0)),
    Column('PostedOn', DateTime),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SPId', Numeric(18, 0)),
    Column('Da', MONEY),
    Column('Dis', Numeric(18, 0)),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OrderNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SH', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('phy', MONEY),
    Column('yvat', MONEY),
    Column('nvat', MONEY),
    Column('c1', MONEY),
    Column('mp', MONEY),
    Column('mpc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_MSaleD = Table(
    'MSaleD', Base.metadata,
    Column('SaleItemNo', Numeric(18, 0), Identity(), nullable=False),
    Column('trano', Numeric(18, 0)),
    Column('TraDate', DateTime),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('total', MONEY),
    Column('itemcost', MONEY),
    Column('vat', MONEY),
    Column('ItemBP', MONEY),
    Column('EDate', DateTime),
    Column('EId', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LP', MONEY),
    Column('H', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vrc', NCHAR(5, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vr', Float(53))
)


t_MUB = Table(
    'MUB', Base.metadata,
    Column('YR', Numeric(18, 0)),
    Column('mon', Numeric(18, 0)),
    Column('vote', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('budg', MONEY)
)


t_MYPNO = Table(
    'MYPNO', Base.metadata,
    Column('PNo', Numeric(18, 0), Identity(), nullable=False),
    Column('PDate', DateTime),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Total', MONEY),
    Column('AccNo', Numeric(18, 0)),
    Column('PMode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PById', Numeric(18, 0)),
    Column('PByName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RefNo', Numeric(18, 0))
)


t_MYPNOD = Table(
    'MYPNOD', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('PNo', Numeric(18, 0)),
    Column('InvNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amount', MONEY),
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


class NDel(Base):
    __tablename__ = 'NDel'
    __table_args__ = (
        PrimaryKeyConstraint('DelId', name='PK_NDel'),
    )

    DelId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ReqNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DelDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DelTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DelBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class NDelI(Base):
    __tablename__ = 'NDelI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_NDelI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DelId: Mapped[Optional[str]] = mapped_column(NCHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))
    ItemCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))


class NHIF(Base):
    __tablename__ = 'NHIF'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_NHIF'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    LB: Mapped[Optional[Any]] = mapped_column(MONEY)
    UB: Mapped[Optional[Any]] = mapped_column(MONEY)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)


class NSSF(Base):
    __tablename__ = 'NSSF'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_NSSF'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    LB: Mapped[Optional[Any]] = mapped_column(MONEY)
    UB: Mapped[Optional[Any]] = mapped_column(MONEY)
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)


class NewReq(Base):
    __tablename__ = 'NewReq'
    __table_args__ = (
        PrimaryKeyConstraint('ReqNo', name='PK_NewReq'),
    )

    ReqNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    BOQ_: Mapped[Optional[decimal.Decimal]] = mapped_column('BOQ', Numeric(18, 0))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class NewReqItem(Base):
    __tablename__ = 'NewReqItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_NewReqItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    REQNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    BOQ_: Mapped[Optional[decimal.Decimal]] = mapped_column('BOQ', Numeric(18, 0))
    BOQID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    BOQREFNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CODE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    NAME: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    QTY: Mapped[Optional[float]] = mapped_column(Float(53))
    PRICE: Mapped[Optional[Any]] = mapped_column(MONEY)
    SUBTOTAL: Mapped[Optional[Any]] = mapped_column(MONEY)
    ATH: Mapped[Optional[float]] = mapped_column(Float(53))
    DL: Mapped[Optional[float]] = mapped_column(Float(53))
    RT: Mapped[Optional[float]] = mapped_column(Float(53))


class OCA(Base):
    __tablename__ = 'OCA'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_OCA'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    NARR: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DR: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR: Mapped[Optional[Any]] = mapped_column(MONEY)
    BAL: Mapped[Optional[Any]] = mapped_column(MONEY)


class OEntry(Base):
    __tablename__ = 'OEntry'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_OEntry'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Votehead: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EItem_: Mapped[Optional[str]] = mapped_column('EItem', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(3000, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ChequeNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    AccNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ABy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Cat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CB_: Mapped[Optional[decimal.Decimal]] = mapped_column('CB', Numeric(18, 0))
    subv: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    brEFnO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class OPost(Base):
    __tablename__ = 'OPost'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_OPost'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PName: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    PDesc: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    DrCr: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    DeCre: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    rbt: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    disc: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class OStockMonitor(Base):
    __tablename__ = 'OStockMonitor'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_StockMonitor'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    StockDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    STime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    OUserlogged: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Itemcode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    OStock: Mapped[Optional[float]] = mapped_column(Float(53))


class OTCat(Base):
    __tablename__ = 'OTCat'
    __table_args__ = (
        PrimaryKeyConstraint('PName', name='PK_OTCat'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    PName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    PDesc: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    PType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class OTCatE(Base):
    __tablename__ = 'OTCatE'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_OTCatE'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AccNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Cat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amt: Mapped[Optional[Any]] = mapped_column(MONEY)
    Narrate: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class OpsR(Base):
    __tablename__ = 'OpsR'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_OpsR'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Dt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SaleNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Acc: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    SoldTo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Cash: Mapped[Optional[Any]] = mapped_column(MONEY)
    Inv: Mapped[Optional[Any]] = mapped_column(MONEY)
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_PA2 = Table(
    'PA2', Base.metadata,
    Column('TR', MONEY),
    Column('MAXG', MONEY)
)


class PAPP(Base):
    __tablename__ = 'PAPP'
    __table_args__ = (
        PrimaryKeyConstraint('AppId', name='PK_KAPP'),
    )

    AppId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CustId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    AppDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PAPPR(Base):
    __tablename__ = 'PAPPR'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_PAPPR'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    AppId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PrDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Comment: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PAYE(Base):
    __tablename__ = 'PAYE'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_PAYE'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    GMIN: Mapped[Optional[Any]] = mapped_column(MONEY)
    GMAX: Mapped[Optional[Any]] = mapped_column(MONEY)
    FAMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    AAMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    RATE: Mapped[Optional[float]] = mapped_column(Float(53))


t_PC = Table(
    'PC', Base.metadata,
    Column('Amount', MONEY)
)


class PCEntry(Base):
    __tablename__ = 'PCEntry'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_PCEntry'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Votehead: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(300, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Pmode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ABy: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    RBy: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Cat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    OBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    CB_: Mapped[Optional[decimal.Decimal]] = mapped_column('CB', Numeric(18, 0))
    Item: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    subacc: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PCat(Base):
    __tablename__ = 'PCat'
    __table_args__ = (
        PrimaryKeyConstraint('CName', name='PK_PCat'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    CName: Mapped[str] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class PF(Base):
    __tablename__ = 'PF'
    __table_args__ = (
        PrimaryKeyConstraint('PF', name='PK_PF'),
    )

    PF: Mapped[Any] = mapped_column(MONEY, primary_key=True)


class PInv(Base):
    __tablename__ = 'PInv'
    __table_args__ = (
        PrimaryKeyConstraint('InvNo', name='PK_PInv'),
    )

    InvNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    InvTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    InvBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    InvDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    InvTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    INVGT: Mapped[Optional[Any]] = mapped_column(MONEY)


class PInvItem(Base):
    __tablename__ = 'PInvItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_PInvItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    InvNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[float]] = mapped_column(Float(53))
    SubTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PNo(Base):
    __tablename__ = 'PNo'
    __table_args__ = (
        PrimaryKeyConstraint('PNo', name='PK_PNo'),
    )

    PNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PById: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PByName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RefNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class PNoD(Base):
    __tablename__ = 'PNoD'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_PNoD'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PNo_: Mapped[Optional[decimal.Decimal]] = mapped_column('PNo', Numeric(18, 0))
    InvNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PP(Base):
    __tablename__ = 'PP'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_PP'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Amt: Mapped[Any] = mapped_column(MONEY, nullable=False)


class PPA(Base):
    __tablename__ = 'PPA'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_PPA_1'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ADATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYEAR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NARR: Mapped[Optional[str]] = mapped_column(Unicode(2000, 'SQL_Latin1_General_CP1_CI_AS'))
    CIN: Mapped[Optional[Any]] = mapped_column(MONEY)
    COUT: Mapped[Optional[Any]] = mapped_column(MONEY)
    BAL: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PPAS(Base):
    __tablename__ = 'PPAS'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_PPAS'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ADATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    NARR: Mapped[Optional[str]] = mapped_column(Unicode(2000, 'SQL_Latin1_General_CP1_CI_AS'))
    CIN: Mapped[Optional[Any]] = mapped_column(MONEY)
    COUT: Mapped[Optional[Any]] = mapped_column(MONEY)
    BAL: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PPR(Base):
    __tablename__ = 'PPR'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_PPR'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    RDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    RBYEMPNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RBYEMPNAME: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ABY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NEWBAL: Mapped[Optional[Any]] = mapped_column(MONEY)


class PVAR(Base):
    __tablename__ = 'PVAR'
    __table_args__ = (
        PrimaryKeyConstraint('VarId', name='PK_PVAR'),
    )

    VarId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYEAR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    VDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    ORAMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    VARS: Mapped[Optional[Any]] = mapped_column(MONEY)
    NAMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    VARVAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    VARBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PackageMode(Base):
    __tablename__ = 'PackageMode'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_PackageMode'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Package: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class PayDetail(Base):
    __tablename__ = 'PayDetail'
    __table_args__ = (
        PrimaryKeyConstraint('PayMonth', 'PayYear', 'EmpNo', name='PK_PayDetail'),
    )

    PayMonth: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    PayYear: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    EmpNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    PAcc: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Gross: Mapped[Optional[Any]] = mapped_column(MONEY)
    HAAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    MAAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    ENSSFAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    BIC: Mapped[Optional[Any]] = mapped_column(MONEY)
    ARR: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalGross: Mapped[Optional[Any]] = mapped_column(MONEY)
    NSSF_: Mapped[Optional[Any]] = mapped_column('NSSF', MONEY)
    CWWG: Mapped[Optional[Any]] = mapped_column(MONEY)
    PAYE_: Mapped[Optional[Any]] = mapped_column('PAYE', MONEY)
    UnionD: Mapped[Optional[Any]] = mapped_column(MONEY)
    NHIF_: Mapped[Optional[Any]] = mapped_column('NHIF', MONEY)
    Elimu: Mapped[Optional[Any]] = mapped_column(MONEY)
    Rent: Mapped[Optional[Any]] = mapped_column(MONEY)
    Advance: Mapped[Optional[Any]] = mapped_column(MONEY)
    COTU: Mapped[Optional[Any]] = mapped_column(MONEY)
    CIC: Mapped[Optional[Any]] = mapped_column(MONEY)
    MAD: Mapped[Optional[Any]] = mapped_column(MONEY)
    EWC: Mapped[Optional[Any]] = mapped_column(MONEY)
    CIN: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalDeduction: Mapped[Optional[Any]] = mapped_column(MONEY)
    NetSalary: Mapped[Optional[Any]] = mapped_column(MONEY)
    TR: Mapped[Optional[Any]] = mapped_column(MONEY)
    act: Mapped[Optional[Any]] = mapped_column(MONEY)
    lbal: Mapped[Optional[Any]] = mapped_column(MONEY)
    mbal: Mapped[Optional[Any]] = mapped_column(MONEY)
    abal: Mapped[Optional[Any]] = mapped_column(MONEY)


class PayMaster(Base):
    __tablename__ = 'PayMaster'
    __table_args__ = (
        PrimaryKeyConstraint('PayMonth', 'PayYear', name='PK_PayMaster'),
    )

    PayMonth: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    PayYear: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    RunOn: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RunBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RunTime: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TotalGross: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalBasic: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalAllowance: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalDeduction: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalNet: Mapped[Optional[Any]] = mapped_column(MONEY)


class PayPurSummary(Base):
    __tablename__ = 'PayPurSummary'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_PayPurSummary'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CustId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Description: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PurchaseAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    PayAmount: Mapped[Optional[Any]] = mapped_column(MONEY)


class Payment(Base):
    __tablename__ = 'Payment'
    __table_args__ = (
        PrimaryKeyConstraint('payno', name='PK_Payment'),
    )

    payno: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 0), Identity(start=1, increment=1), primary_key=True)
    trano: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Sid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    paydate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    bal: Mapped[Optional[Any]] = mapped_column(MONEY)
    paymode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    chequeno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    dbank: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ddocno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    BNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CB_: Mapped[Optional[decimal.Decimal]] = mapped_column('CB', Numeric(18, 0))


t_Product = Table(
    'Product', Base.metadata,
    Column('Pcategory', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Gcode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Pcode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pname', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Bprice', MONEY),
    Column('Sprice', MONEY),
    Column('Wprice', MONEY),
    Column('Opqty', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ReLevel', Float(53)),
    Column('Model', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VatCode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PBarCode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('purQty', Float(53)),
    Column('SalesQty', Integer),
    Column('ITNIn', Float(53)),
    Column('ITNOut', Float(53)),
    Column('CreditQty', Float(53)),
    Column('DebitQty', Float(53)),
    Column('StockQty', Float(53)),
    Column('OptPoison', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


class Proj(Base):
    __tablename__ = 'Proj'
    __table_args__ = (
        PrimaryKeyConstraint('PId', name='PK_Proj'),
    )

    PId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ShopId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class ProjC(Base):
    __tablename__ = 'ProjC'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_ProjC'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    V1: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    V2: Mapped[Optional[Any]] = mapped_column(MONEY)
    V3: Mapped[Optional[Any]] = mapped_column(MONEY)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Est: Mapped[Optional[Any]] = mapped_column(MONEY)
    QTY: Mapped[Optional[float]] = mapped_column(Float(53))
    PR: Mapped[Optional[Any]] = mapped_column(MONEY)


class QUOTE(Base):
    __tablename__ = 'QUOTE'
    __table_args__ = (
        PrimaryKeyConstraint('QUOTENo', name='PK_QUOTE'),
    )

    QUOTENo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Notes: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    GT: Mapped[Optional[Any]] = mapped_column(MONEY)
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)
    ct: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class QUOTEI(Base):
    __tablename__ = 'QUOTEI'
    __table_args__ = (
        PrimaryKeyConstraint('Recid', name='PK_QUOTEI'),
    )

    Recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    QUOTENo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ICode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)
    NAr: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    VATRate: Mapped[Optional[float]] = mapped_column(Float(53))
    VATAmt: Mapped[Optional[Any]] = mapped_column(MONEY)
    VATsTAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_Query1 = Table(
    'Query1', Base.metadata,
    Column('pcode', Integer),
    Column('name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('man', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_Query2 = Table(
    'Query2', Base.metadata,
    Column('Expr1000', Integer)
)


class RAllocate(Base):
    __tablename__ = 'RAllocate'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_RAllocate'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SPId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Route: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class REMAPP(Base):
    __tablename__ = 'REMAPP'
    __table_args__ = (
        PrimaryKeyConstraint('UN', name='PK_REMAPP'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    UN: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    CNT: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class REQASS(Base):
    __tablename__ = 'REQASS'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_REQASS'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ReqNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    GRP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    REQQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    APPQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    DLQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    RTQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    ITEMCODE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ITEMNAME: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SOURCE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    BP: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    BUYP: Mapped[Optional[Any]] = mapped_column(MONEY)


class RHist(Base):
    __tablename__ = 'RHist'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_RHist'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Aby: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CB_: Mapped[Optional[decimal.Decimal]] = mapped_column('CB', Numeric(18, 0))


class RL(Base):
    __tablename__ = 'RL'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_RL'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ETime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ReqNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))


class RORD(Base):
    __tablename__ = 'RORD'
    __table_args__ = (
        PrimaryKeyConstraint('QUOTENo', name='PK_RORD'),
    )

    QUOTENo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Notes: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    GT: Mapped[Optional[Any]] = mapped_column(MONEY)
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    LUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)
    CYEAR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CCLIENT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class RORDI(Base):
    __tablename__ = 'RORDI'
    __table_args__ = (
        PrimaryKeyConstraint('Recid', name='PK_RORDI'),
    )

    Recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    QUOTENo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ICode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    ST: Mapped[Optional[Any]] = mapped_column(MONEY)
    NAr: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class Rebate(Base):
    __tablename__ = 'Rebate'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_Rebate'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Rebate: Mapped[Optional[Any]] = mapped_column(MONEY)


class ReceiveCredit(Base):
    __tablename__ = 'Receive_Credit'
    __table_args__ = (
        PrimaryKeyConstraint('trano', name='PK_Receive_Credit'),
    )

    trano: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 0), Identity(start=1, increment=1), primary_key=True)
    RefNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    id: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 0))
    pmode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    DAllowed: Mapped[Optional[Any]] = mapped_column(MONEY)
    tradate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    chequeno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    dbank: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PN: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    VatWith: Mapped[Optional[Any]] = mapped_column(MONEY)
    VatWithRefNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class Reconcile(Base):
    __tablename__ = 'Reconcile'
    __table_args__ = (
        PrimaryKeyConstraint('TraDate', name='PK_Reconcile'),
    )

    TraDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    CashSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    Creditors: Mapped[Optional[Any]] = mapped_column(MONEY)
    Invoices: Mapped[Optional[Any]] = mapped_column(MONEY)
    GrossCash: Mapped[Optional[Any]] = mapped_column(MONEY)
    Expenses: Mapped[Optional[Any]] = mapped_column(MONEY)
    NetCash: Mapped[Optional[Any]] = mapped_column(MONEY)
    Banked: Mapped[Optional[Any]] = mapped_column(MONEY)
    DefSurp: Mapped[Optional[Any]] = mapped_column(MONEY)
    Comment: Mapped[Optional[str]] = mapped_column(Unicode(300, 'SQL_Latin1_General_CP1_CI_AS'))
    CreditSale: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(18, 2), server_default=text('((0))'))


class Req(Base):
    __tablename__ = 'Req'
    __table_args__ = (
        PrimaryKeyConstraint('ReqNo', name='PK_Req'),
    )

    ReqNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ITo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    LPoNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    VNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    SEId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DL: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class ReqItem(Base):
    __tablename__ = 'ReqItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_ReqItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Aid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    SubTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    Source: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Reqno: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DL: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    APP_: Mapped[Optional[str]] = mapped_column('APP', CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))


class ReturnOutWardItem(Base):
    __tablename__ = 'Return_OutWard_Item'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_Return_OutWard_Item'),
    )

    ReturnNo: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 0), nullable=False)
    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Reason: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DQty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    St: Mapped[Optional[Any]] = mapped_column(MONEY)
    VatAmt: Mapped[Optional[Any]] = mapped_column(MONEY)
    TT: Mapped[Optional[Any]] = mapped_column(MONEY)


class ReturnOutward(Base):
    __tablename__ = 'Return_Outward'
    __table_args__ = (
        PrimaryKeyConstraint('ReturnNo', name='PK_Return_Outward'),
    )

    ReturnNo: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 0), Identity(start=1, increment=1), primary_key=True)
    Trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TotalAmt: Mapped[Optional[Any]] = mapped_column(MONEY)
    ReturnDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Route(Base):
    __tablename__ = 'Route'
    __table_args__ = (
        PrimaryKeyConstraint('RName', name='PK_Route'),
    )

    RId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    RName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    RDesc: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))


class SALESUMMARY(Base):
    __tablename__ = 'SALESUMMARY'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SALESUMMARY'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PCODE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SaleQty: Mapped[Optional[float]] = mapped_column(Float(53))
    DelQty: Mapped[Optional[float]] = mapped_column(Float(53))
    Ostock: Mapped[Optional[float]] = mapped_column(Float(53))
    Cstock: Mapped[Optional[float]] = mapped_column(Float(53))
    Pstock: Mapped[Optional[float]] = mapped_column(Float(53))
    QEdit1: Mapped[Optional[float]] = mapped_column(Float(53))
    QEdit2: Mapped[Optional[float]] = mapped_column(Float(53))
    QOff: Mapped[Optional[float]] = mapped_column(Float(53))


class SCard(Base):
    __tablename__ = 'SCard'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SCard'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    MDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Category: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    QIn: Mapped[Optional[float]] = mapped_column(Float(53))
    QOut: Mapped[Optional[float]] = mapped_column(Float(53))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NewQty: Mapped[Optional[float]] = mapped_column(Float(53))
    AllQty: Mapped[Optional[float]] = mapped_column(Float(53))
    GRP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_SConvert = Table(
    'SConvert', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(start=1, increment=1), nullable=False),
    Column('FCode', Numeric(18, 0)),
    Column('CQty', Float(53)),
    Column('BQty', Float(53)),
    Column('NQty', Float(53)),
    Column('TCode', Numeric(18, 0)),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CDate', DateTime)
)


class SDAS(Base):
    __tablename__ = 'SDAS'
    __table_args__ = (
        PrimaryKeyConstraint('recid', name='PK_SDAS'),
    )

    recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    sid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    a30: Mapped[Optional[Any]] = mapped_column(MONEY)
    a60: Mapped[Optional[Any]] = mapped_column(MONEY)
    a90: Mapped[Optional[Any]] = mapped_column(MONEY)
    a120: Mapped[Optional[Any]] = mapped_column(MONEY)
    aover: Mapped[Optional[Any]] = mapped_column(MONEY)
    atotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    UB: Mapped[Optional[Any]] = mapped_column(MONEY)


class SE(Base):
    __tablename__ = 'SE'
    __table_args__ = (
        PrimaryKeyConstraint('VNo', name='PK_SE'),
    )

    VNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EntryDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EntryTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DoneBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    VTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class SEI(Base):
    __tablename__ = 'SEI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SEI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    VNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Votehead: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    ABy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PTo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ChequeNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class SIP(Base):
    __tablename__ = 'SIP'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_SIP'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SHOPID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    ITEMCODE: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    PRICE: Mapped[Optional[Any]] = mapped_column(MONEY)


class SInv(Base):
    __tablename__ = 'SInv'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SInv'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    InvDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TraNo: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Detail: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Supplier: Mapped[Optional[str]] = mapped_column(Unicode(150, 'SQL_Latin1_General_CP1_CI_AS'))
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    InvAmount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Paid: Mapped[Optional[Any]] = mapped_column(MONEY)
    Balance: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SL(Base):
    __tablename__ = 'SL'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SL'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TTIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    NARR: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    QIN: Mapped[Optional[Any]] = mapped_column(MONEY)
    QOUT: Mapped[Optional[Any]] = mapped_column(MONEY)
    BAL: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))


class SM(Base):
    __tablename__ = 'SM'
    __table_args__ = (
        PrimaryKeyConstraint('RECNO', name='PK_SM_1'),
    )

    RECNO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    OTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    OQty: Mapped[Optional[float]] = mapped_column(Float(53))
    OPrice: Mapped[Optional[Any]] = mapped_column(MONEY)
    OUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CQty: Mapped[Optional[float]] = mapped_column(Float(53))
    CPrice_: Mapped[Optional[Any]] = mapped_column('CPrice', MONEY)
    CUser: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SOPost(Base):
    __tablename__ = 'SOPost'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SOPost'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    IDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Cat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SPItem(Base):
    __tablename__ = 'SPItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SPItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    SubTotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class SPM(Base):
    __tablename__ = 'SPM'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SPM'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    DID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class SPSD(Base):
    __tablename__ = 'SP_S_D'
    __table_args__ = (
        PrimaryKeyConstraint('recid', name='PK_SP_S_D'),
    )

    recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    tdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    spid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    spname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    itemname: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    qty: Mapped[Optional[float]] = mapped_column(Float(53))
    cos: Mapped[Optional[Any]] = mapped_column(MONEY)
    total: Mapped[Optional[Any]] = mapped_column(MONEY)
    prof: Mapped[Optional[Any]] = mapped_column(MONEY)
    cat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    STO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SPay(Base):
    __tablename__ = 'SPay'
    __table_args__ = (
        PrimaryKeyConstraint('PayNo', name='PK_SPay'),
    )

    PayNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    AMT: Mapped[Optional[Any]] = mapped_column(MONEY)
    SID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PTIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PMODE: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CQNO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TRDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TFROM: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ACCNO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TTO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TBANK: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cd: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    spay: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PDT: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class SPerson(Base):
    __tablename__ = 'SPerson'
    __table_args__ = (
        PrimaryKeyConstraint('Name', name='PK_SPerson'),
    )

    SId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    Name: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Address: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TelNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IDNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DRoute: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SR(Base):
    __tablename__ = 'SR'
    __table_args__ = (
        PrimaryKeyConstraint('DNo', name='PK_SR'),
    )

    DNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    TBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Shop: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SRItem(Base):
    __tablename__ = 'SRItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SRItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    DNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    ItemPrice: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemVAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemCost: Mapped[Optional[Any]] = mapped_column(MONEY)


class SSTL(Base):
    __tablename__ = 'SSTL'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SSTL'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Narrate: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    CIN: Mapped[Optional[float]] = mapped_column(Float(53))
    COUT: Mapped[Optional[float]] = mapped_column(Float(53))
    NQTY: Mapped[Optional[float]] = mapped_column(Float(53))
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))


class SSTR(Base):
    __tablename__ = 'SSTR'
    __table_args__ = (
        PrimaryKeyConstraint('TR', name='PK_SSTR'),
    )

    TR: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    T: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    TNAME: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SSTRI(Base):
    __tablename__ = 'SSTRI'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_SSTRI'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCODE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PNAME: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    QTY: Mapped[Optional[float]] = mapped_column(Float(53))


class SState(Base):
    __tablename__ = 'SState'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SState'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Category: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DR: Mapped[Optional[Any]] = mapped_column(MONEY)
    CR: Mapped[Optional[Any]] = mapped_column(MONEY)
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)


t_SStatement = Table(
    'SStatement', Base.metadata,
    Column('Id', Numeric(18, 0)),
    Column('TraDate', DateTime),
    Column('Narrate', Unicode(200, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DR', MONEY),
    Column('CR', MONEY)
)


class ST(Base):
    __tablename__ = 'ST'
    __table_args__ = (
        PrimaryKeyConstraint('STNo', name='PK_ST'),
    )

    STNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    STAT: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))
    CDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class STE(Base):
    __tablename__ = 'STE'
    __table_args__ = (
        PrimaryKeyConstraint('EntNo', name='PK_STE'),
    )

    EntNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    StNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    StArea: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RegNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))


class STEI(Base):
    __tablename__ = 'STEI'
    __table_args__ = (
        PrimaryKeyConstraint('RECID', name='PK_STEI'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    STNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCODE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    QTY: Mapped[Optional[float]] = mapped_column(Float(53))


class STI(Base):
    __tablename__ = 'STI'
    __table_args__ = (
        PrimaryKeyConstraint('STNO', 'PCODE', name='PK_STI'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    STNO: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    PCODE: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    FQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    FSH: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    FFS: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    FBS: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    CQTY: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    CSH: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    CFS: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    CBS: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))


class SUB(Base):
    __tablename__ = 'SUB'
    __table_args__ = (
        PrimaryKeyConstraint('sid', name='PK_SUB'),
    )

    sid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    ub: Mapped[Optional[Any]] = mapped_column(MONEY)


class Sale(Base):
    __tablename__ = 'Sale'
    __table_args__ = (
        PrimaryKeyConstraint('TraNo', name='PK_Sale'),
    )

    TraNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    tradate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    tratype: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    saletype: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    idno: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 0))
    cashier: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    total: Mapped[Optional[Any]] = mapped_column(MONEY)
    cash: Mapped[Optional[Any]] = mapped_column(MONEY)
    change: Mapped[Optional[Any]] = mapped_column(MONEY)
    vat: Mapped[Optional[Any]] = mapped_column(MONEY)
    SaleTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SoldTo: Mapped[Optional[str]] = mapped_column(Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
    InvNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PostedOn: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    OBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    SPId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Da: Mapped[Optional[Any]] = mapped_column(MONEY)
    Dis_: Mapped[Optional[decimal.Decimal]] = mapped_column('Dis', Numeric(18, 0))
    RegNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    OrderNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DNO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SH: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0), server_default=text('((1))'))
    PartNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    phy: Mapped[Optional[Any]] = mapped_column(MONEY)
    yvat: Mapped[Optional[Any]] = mapped_column(MONEY)
    nvat: Mapped[Optional[Any]] = mapped_column(MONEY)
    c1: Mapped[Optional[Any]] = mapped_column(MONEY)
    mp: Mapped[Optional[Any]] = mapped_column(MONEY)
    mpc: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SaleBank(Base):
    __tablename__ = 'SaleBank'
    __table_args__ = (
        PrimaryKeyConstraint('TraDate', name='PK_SaleBank'),
    )

    TraDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    ShamataSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    ShamataBank: Mapped[Optional[Any]] = mapped_column(MONEY)
    RongaiSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    RongaiBank: Mapped[Optional[Any]] = mapped_column(MONEY)
    NyahururuSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    NyahururuBank: Mapped[Optional[Any]] = mapped_column(MONEY)
    KiserianSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    KiserianBank: Mapped[Optional[Any]] = mapped_column(MONEY)
    NgongSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    NgongBank: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalBank: Mapped[Optional[Any]] = mapped_column(MONEY)


class SaleP(Base):
    __tablename__ = 'SaleP'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_SMan'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TraDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class SaleDeleted(Base):
    __tablename__ = 'Sale_Deleted'
    __table_args__ = (
        PrimaryKeyConstraint('DelId', name='PK__Sale_Del__D6853A54E0CA8D02'),
    )

    DelId: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    TraNo: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    tradate: Mapped[Optional[datetime.date]] = mapped_column(Date)
    tratype: Mapped[Optional[str]] = mapped_column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cashier: Mapped[Optional[str]] = mapped_column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    SoldTo: Mapped[Optional[str]] = mapped_column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    total: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(18, 2))
    vat: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(18, 2))
    cash: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(18, 2))
    DeletedAt: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))


class SaleItem(Base):
    __tablename__ = 'Sale_Item'
    __table_args__ = (
        PrimaryKeyConstraint('SaleItemNo', name='PK_Sale_Item'),
    )

    SaleItemNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TraDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ItemCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    qty: Mapped[Optional[float]] = mapped_column(Float(53))
    total: Mapped[Optional[Any]] = mapped_column(MONEY)
    itemcost: Mapped[Optional[Any]] = mapped_column(MONEY)
    vat: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemBP: Mapped[Optional[Any]] = mapped_column(MONEY)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PartNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    LP: Mapped[Optional[Any]] = mapped_column(MONEY)
    H: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    vrc: Mapped[Optional[str]] = mapped_column(NCHAR(5, 'SQL_Latin1_General_CP1_CI_AS'))
    vr: Mapped[Optional[float]] = mapped_column(Float(53))


class SaleItemPrint(Base):
    __tablename__ = 'Sale_Item_Print'
    __table_args__ = (
        PrimaryKeyConstraint('SaleItemNo', name='PK_Sale_Item_Print'),
    )

    SaleItemNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TraNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    TraDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ItemCode: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    ItemName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Qty: Mapped[float] = mapped_column(Float(53), nullable=False)
    Total: Mapped[Any] = mapped_column(MONEY, nullable=False)
    Itemcost: Mapped[Any] = mapped_column(MONEY, nullable=False)
    VAT: Mapped[Any] = mapped_column(MONEY, nullable=False)
    ItemBP: Mapped[Any] = mapped_column(MONEY, nullable=False)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PartNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class SalePrint(Base):
    __tablename__ = 'Sale_Print'
    __table_args__ = (
        PrimaryKeyConstraint('TraNo', name='PK_Sale_Print'),
    )

    TraNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    TraDate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    TraType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SaleType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IdNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Cashier: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    Cash: Mapped[Optional[Any]] = mapped_column(MONEY)
    Change: Mapped[Optional[Any]] = mapped_column(MONEY)
    VAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    SaleTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PostedOn: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    InvNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    SoldTo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    OBal: Mapped[Optional[Any]] = mapped_column(MONEY)
    SPId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RegNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ORDERNO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DNO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    da: Mapped[Optional[Any]] = mapped_column(MONEY)
    PartNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    phy: Mapped[Optional[Any]] = mapped_column(MONEY)


class SerSal(Base):
    __tablename__ = 'SerSal'
    __table_args__ = (
        PrimaryKeyConstraint('SalNo', name='PK_SerSal'),
    )

    SerNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1000, increment=1), nullable=False)
    SalNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)


class Shelf(Base):
    __tablename__ = 'Shelf'
    __table_args__ = (
        PrimaryKeyConstraint('SName', name='PK_Shelf'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    SName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class Shop(Base):
    __tablename__ = 'Shop'
    __table_args__ = (
        PrimaryKeyConstraint('ShopID', name='PK_Shop'),
    )

    ShopID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    ShopName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Location: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Bal: Mapped[Optional[Any]] = mapped_column(MONEY)


class SoldIn(Base):
    __tablename__ = 'SoldIn'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_SoldIn'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    SoldIn: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class StockCheck(Base):
    __tablename__ = 'StockCheck'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_StockCheck'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TraNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TraDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    WP: Mapped[Optional[Any]] = mapped_column(MONEY)
    SP: Mapped[Optional[Any]] = mapped_column(MONEY)
    OverC: Mapped[Optional[Any]] = mapped_column(MONEY)
    UnderC: Mapped[Optional[Any]] = mapped_column(MONEY)
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class StockReplenish(Base):
    __tablename__ = 'Stock_Replenish'
    __table_args__ = (
        PrimaryKeyConstraint('trano', name='PK_Stock_Replenish'),
    )

    trano: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 0), primary_key=True)
    dmode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    docno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    supplier: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    issuedate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    datedue: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    replenishdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    vatamount: Mapped[Optional[Any]] = mapped_column(MONEY)
    Cb: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYEAR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CLIENT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ATT: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ATTTO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    VA: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    sid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class StockReplenishItem(Base):
    __tablename__ = 'Stock_Replenish_Item'
    __table_args__ = (
        PrimaryKeyConstraint('RepNo', name='PK_Stock_Replenish_Item'),
    )

    RepNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Trano: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 0))
    ItemName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))
    ItemCost: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemVAT: Mapped[Optional[Any]] = mapped_column(MONEY)
    BatchNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    MDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DQty: Mapped[Optional[float]] = mapped_column(Float(53))
    LREFNO: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    dest: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    DiscR: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    DiscAmt: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    NetAmt: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    VATInc: Mapped[Optional[str]] = mapped_column(CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'), server_default=text('((0))'))
    VATP: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    SubT: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY, server_default=text('((0))'))
    NewPrice: Mapped[Optional[Any]] = mapped_column(MONEY)


class StockItem(Base):
    __tablename__ = 'Stock_item'
    __table_args__ = (
        PrimaryKeyConstraint('pcode', name='PK_Stock_item'),
    )

    pcode: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    man: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    bpw: Mapped[Optional[Any]] = mapped_column(MONEY)
    spw: Mapped[Optional[Any]] = mapped_column(MONEY)
    spr: Mapped[Optional[Any]] = mapped_column(MONEY)
    sppercent: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    vat: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    vatamount: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    qtystock: Mapped[Optional[float]] = mapped_column(Float(53))
    RLevel: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Package: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PackageQty: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    SoldIn_: Mapped[Optional[str]] = mapped_column('SoldIn', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    SaleQty: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    PCategory: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    GCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Cat: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Expire: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    VATCode: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Loc: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    BQGRP_: Mapped[Optional[str]] = mapped_column('BQGRP', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    SHQTY: Mapped[Optional[float]] = mapped_column(Float(53))
    STQTY: Mapped[Optional[float]] = mapped_column(Float(53))
    PARTNO: Mapped[Optional[str]] = mapped_column(Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
    Col026: Mapped[Optional[str]] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    BCODE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Col028: Mapped[Optional[str]] = mapped_column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    lp: Mapped[Optional[Any]] = mapped_column(MONEY)
    lo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    hot: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    BC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class Store(Base):
    __tablename__ = 'Store'
    __table_args__ = (
        PrimaryKeyConstraint('SName', name='PK_Store'),
    )

    SID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    SName: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class StoreItem(Base):
    __tablename__ = 'StoreItem'
    __table_args__ = (
        PrimaryKeyConstraint('StoreID', 'PCode', name='PK_StoreItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    StoreID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    PCode: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))


class StoreStock(Base):
    __tablename__ = 'StoreStock'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_StoreStock'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    StoreID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    PCode: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), nullable=False)
    Qty: Mapped[Optional[float]] = mapped_column(Float(53))


class Supplier(Base):
    __tablename__ = 'Supplier'
    __table_args__ = (
        PrimaryKeyConstraint('supplierid', name='PK_Supplier'),
    )

    supplierid: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 0), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    telno: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    fax: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    postal: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    email: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    town: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    street: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    house: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cperson: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    cpersontel: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    AmountOwing: Mapped[Optional[Any]] = mapped_column(MONEY)
    vat: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    pin: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    vata: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    sta: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


t_Supplier2 = Table(
    'Supplier2', Base.metadata,
    Column('NAME', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AMOUNTOWING', String(255, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_Supplier2_0 = Table(
    'Supplier2_0', Base.metadata,
    Column('supplierid', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('name', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('telno', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('fax', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('postal', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('email', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('town', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('street', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('house', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('cperson', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('cpersontel', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AmountOwing', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vat', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('pin', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vata', String(255, 'SQL_Latin1_General_CP1_CI_AS'))
)


class SupplierProduct(Base):
    __tablename__ = 'Supplier_Product'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_Supplier_Product'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    productname: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    supplierid: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 0))


class TCall(Base):
    __tablename__ = 'TCall'
    __table_args__ = (
        PrimaryKeyConstraint('CallId', name='PK_TCall'),
    )

    CallId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    CustId: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    CBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Narr: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    PR: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ASS: Mapped[Optional[str]] = mapped_column(CHAR(1, 'SQL_Latin1_General_CP1_CI_AS'))
    ASSBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ATO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    WRK: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    DIA: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    INV: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CustName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CustType: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RegNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Make: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Model: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Mileage: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    OtherDetail: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    Spare: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Radio: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Jack: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ToolKit: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PayBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PayAC: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PayACName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class TG(Base):
    __tablename__ = 'TG'
    __table_args__ = (
        PrimaryKeyConstraint('GId', name='PK_TG'),
    )

    GId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    GName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    GPrice: Mapped[Optional[Any]] = mapped_column(MONEY)


class TI(Base):
    __tablename__ = 'TI'
    __table_args__ = (
        PrimaryKeyConstraint('IID', name='PK_TI'),
    )

    IID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    IDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    TID: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ITO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PROJ: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PROJYR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RTBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ATT: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ATTCAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ATTTO: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    URTBY: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class TIssue(Base):
    __tablename__ = 'TIssue'
    __table_args__ = (
        PrimaryKeyConstraint('INo', 'IYear', name='PK_TIssue'),
    )

    INo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    IYear: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    IDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ITo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    IBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IStatus: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ITime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ITotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    LpoNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Route_: Mapped[Optional[str]] = mapped_column('Route', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    IP: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CUST: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class TIssueItem(Base):
    __tablename__ = 'TIssueItem'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_TIssueItem'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    INo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    IYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PCode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    IQty: Mapped[Optional[float]] = mapped_column(Float(53))
    Price: Mapped[Optional[Any]] = mapped_column(MONEY)
    ItemCost: Mapped[Optional[Any]] = mapped_column(MONEY)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TL(Base):
    __tablename__ = 'TL'
    __table_args__ = (
        PrimaryKeyConstraint('TId', name='PK_TL'),
    )

    TId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ISS: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TR: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    OK: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    GRP: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class TPL(Base):
    __tablename__ = 'TPL'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_TPL'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Val1: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Val2: Mapped[Optional[Any]] = mapped_column(MONEY)
    VAL3: Mapped[Optional[Any]] = mapped_column(MONEY)


class TPNo(Base):
    __tablename__ = 'TPNo'
    __table_args__ = (
        PrimaryKeyConstraint('PNo', name='PK_TPNo'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    PNo_: Mapped[decimal.Decimal] = mapped_column('PNo', Numeric(18, 0), primary_key=True)
    PDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Total: Mapped[Optional[Any]] = mapped_column(MONEY)
    AccNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PMode: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    PById: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    PByName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    RefNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class TPNoD(Base):
    __tablename__ = 'TPNoD'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_TPNoD'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PNo_: Mapped[Optional[decimal.Decimal]] = mapped_column('PNo', Numeric(18, 0))
    InvNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    CAT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class Trading(Base):
    __tablename__ = 'Trading'
    __table_args__ = (
        PrimaryKeyConstraint('StartDate', 'EndDate', name='PK_Trading'),
    )

    StartDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    EndDate: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)
    OpeningStock: Mapped[Optional[Any]] = mapped_column(MONEY)
    Purchases: Mapped[Optional[Any]] = mapped_column(MONEY)
    ReturnOutwards: Mapped[Optional[Any]] = mapped_column(MONEY)
    CarriageInwards: Mapped[Optional[Any]] = mapped_column(MONEY)
    ClosingStock: Mapped[Optional[Any]] = mapped_column(MONEY)
    CostOfGoods: Mapped[Optional[Any]] = mapped_column(MONEY)
    GrossProfit: Mapped[Optional[Any]] = mapped_column(MONEY)
    Sales: Mapped[Optional[Any]] = mapped_column(MONEY)
    ReturnInwards: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalDR: Mapped[Optional[Any]] = mapped_column(MONEY)
    TotalCr: Mapped[Optional[Any]] = mapped_column(MONEY)
    TDEL: Mapped[Optional[Any]] = mapped_column(MONEY)


class Ts(Base):
    __tablename__ = 'Ts'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_TS'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    TDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    RefNo: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Description: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    CashSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    CreditSale: Mapped[Optional[Any]] = mapped_column(MONEY)
    Debtor: Mapped[Optional[Any]] = mapped_column(MONEY)
    Supplier_: Mapped[Optional[Any]] = mapped_column('Supplier', MONEY)
    CNote_: Mapped[Optional[Any]] = mapped_column('CNote', MONEY)
    qty: Mapped[Optional[float]] = mapped_column(Float(53))


class UG(Base):
    __tablename__ = 'UG'
    __table_args__ = (
        PrimaryKeyConstraint('GCODE', name='PK_UG'),
    )

    GCODE: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    GNAME: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class UGR(Base):
    __tablename__ = 'UGR'
    __table_args__ = (
        PrimaryKeyConstraint('GCODE', 'ACODE', name='PK_UGR'),
    )

    RECID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    GCODE: Mapped[decimal.Decimal] = mapped_column(Numeric(19, 0), primary_key=True)
    ACODE: Mapped[str] = mapped_column(Unicode(5, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    ACC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class UP(Base):
    __tablename__ = 'UP'
    __table_args__ = (
        PrimaryKeyConstraint('recid', name='PK_UP'),
    )

    recid: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    u1: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    u2: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    u3: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    u4: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class Users(Base):
    __tablename__ = 'Users'
    __table_args__ = (
        PrimaryKeyConstraint('Username', name='PK_Users'),
    )

    Username: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    FName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    LName: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Password: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ACode: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Area: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Status: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Opc: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ACT: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    MU: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    APPR: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    ts: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    fo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class VATCode(Base):
    __tablename__ = 'VATCode'
    __table_args__ = (
        PrimaryKeyConstraint('VCode', name='PK_VATCode'),
    )

    VCode: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    VRate: Mapped[Optional[float]] = mapped_column(Float(53))


class VAttLog(Base):
    __tablename__ = 'VAttLog'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_VAttLog'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    LDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    WK: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class VAttLogW(Base):
    __tablename__ = 'VAttLogW'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_VAttLogW'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    WK: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    D1: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D2: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D3: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D4: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D5: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D6: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    D7: Mapped[Optional[str]] = mapped_column(Unicode(500, 'SQL_Latin1_General_CP1_CI_AS'))
    DBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class VCW(Base):
    __tablename__ = 'VCW'
    __table_args__ = (
        PrimaryKeyConstraint('WNo', name='PK_VCW'),
    )

    WNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Votehead: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EBy: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EndDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class VCWI(Base):
    __tablename__ = 'VCWI'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_VCWI'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    WNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Name: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Rate: Mapped[Optional[Any]] = mapped_column(MONEY)
    Days: Mapped[Optional[float]] = mapped_column(Float(53))
    STotal: Mapped[Optional[Any]] = mapped_column(MONEY)
    Deduction: Mapped[Optional[Any]] = mapped_column(MONEY)
    Net: Mapped[Optional[Any]] = mapped_column(MONEY)
    TRef: Mapped[Optional[Any]] = mapped_column(MONEY)
    AccRef: Mapped[Optional[Any]] = mapped_column(MONEY)


class VCWage(Base):
    __tablename__ = 'VCWage'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_VCWage'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    WDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EmpNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    CYear: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    Amount: Mapped[Optional[Any]] = mapped_column(MONEY)
    WNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class VEH(Base):
    __tablename__ = 'VEH'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_VEH'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    Reg: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Make: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Rate: Mapped[Optional[Any]] = mapped_column(MONEY)


class VoteT(Base):
    __tablename__ = 'VoteT'
    __table_args__ = (
        PrimaryKeyConstraint('RecNo', name='PK_VoteT'),
    )

    RecNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    RNo: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))
    TraDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Votehead: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    CR: Mapped[Optional[Any]] = mapped_column(MONEY)
    DR: Mapped[Optional[Any]] = mapped_column(MONEY)
    Narration: Mapped[Optional[str]] = mapped_column(Unicode(300, 'SQL_Latin1_General_CP1_CI_AS'))
    Narr2: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    PT: Mapped[Optional[str]] = mapped_column(Unicode(200, 'SQL_Latin1_General_CP1_CI_AS'))
    grp: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


class Votehead(Base):
    __tablename__ = 'Votehead'
    __table_args__ = (
        PrimaryKeyConstraint('Votehead', name='PK_Votehead'),
    )

    Votehead: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Description: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Status: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))


class WK(Base):
    __tablename__ = 'WK'
    __table_args__ = (
        PrimaryKeyConstraint('WKYear', 'WKNo', name='PK_WK'),
    )

    WeekID: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), nullable=False)
    WKYear: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    WKNo: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    SDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EDate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Acm(Base):
    __tablename__ = 'acm'
    __table_args__ = (
        PrimaryKeyConstraint('RecId', name='PK_acm'),
    )

    RecId: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), Identity(start=1, increment=1), primary_key=True)
    PT: Mapped[Optional[str]] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
    AC: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(18, 0))


t_cwCWage = Table(
    'cwCWage', Base.metadata,
    Column('WDate', DateTime),
    Column('EmpNo', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CYear', Numeric(18, 0)),
    Column('CNo', Numeric(18, 0)),
    Column('Amount', MONEY)
)


class Emptest(Base):
    __tablename__ = 'emptest'
    __table_args__ = (
        PrimaryKeyConstraint('empno', name='PK_emptest'),
    )

    empno: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class Mvb(Base):
    __tablename__ = 'mvb'
    __table_args__ = (
        PrimaryKeyConstraint('yr', 'mon', 'vote', name='PK_mub'),
    )

    yr: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    mon: Mapped[decimal.Decimal] = mapped_column(Numeric(18, 0), primary_key=True)
    vote: Mapped[str] = mapped_column(Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    budg: Mapped[Optional[Any]] = mapped_column(MONEY)


class Sysdiagrams(Base):
    __tablename__ = 'sysdiagrams'
    __table_args__ = (
        PrimaryKeyConstraint('diagram_id', name='PK__sysdiagr__C2B05B6155CAA640'),
        Index('UK_principal_name', 'principal_id', 'name', mssql_clustered=False, unique=True)
    )

    name: Mapped[str] = mapped_column(Unicode(128, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    principal_id: Mapped[int] = mapped_column(Integer, nullable=False)
    diagram_id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    version: Mapped[Optional[int]] = mapped_column(Integer)
    definition: Mapped[Optional[bytes]] = mapped_column(LargeBinary)


t_vwAC = Table(
    'vwAC', Base.metadata,
    Column('AC', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AName', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ADesc', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AN', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LT', String(255, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwACM = Table(
    'vwACM', Base.metadata,
    Column('RecId', Numeric(18, 0), nullable=False),
    Column('PT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AC', Numeric(18, 0)),
    Column('eg', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EXP', Numeric(18, 0))
)


t_vwAPCQ = Table(
    'vwAPCQ', Base.metadata,
    Column('BNo', Numeric(18, 0), nullable=False),
    Column('SId', Numeric(18, 0)),
    Column('PDate', DateTime),
    Column('Amount', MONEY),
    Column('PMode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PModeNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CB', Numeric(18, 0)),
    Column('PDT', DateTime),
    Column('baccno', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('cqdt', DateTime),
    Column('cqb', Integer, nullable=False),
    Column('cbdt', DateTime),
    Column('cbu', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('p', Numeric(18, 0), nullable=False),
    Column('SupplierName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwAPCQR = Table(
    'vwAPCQR', Base.metadata,
    Column('BNo', Numeric(18, 0), nullable=False),
    Column('SId', Numeric(18, 0)),
    Column('PDate', DateTime),
    Column('Amount', MONEY),
    Column('PMode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PModeNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CB', Numeric(18, 0)),
    Column('PDT', DateTime),
    Column('baccno', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('cqdt', DateTime),
    Column('cqb', Integer, nullable=False),
    Column('cbdt', DateTime),
    Column('cbu', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('p', Numeric(18, 0), nullable=False),
    Column('SupplierName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwAPP = Table(
    'vwAPP', Base.metadata,
    Column('AppId', Numeric(18, 0), nullable=False),
    Column('ReqNo', Numeric(18, 0)),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('APPDT', DateTime),
    Column('APPTM', DateTime),
    Column('GRP', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemCode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('bp', MONEY),
    Column('SubTotal', Float(53)),
    Column('CID', Numeric(18, 0)),
    Column('CYEAR', Numeric(18, 0)),
    Column('CCLIENT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwAUTHBAL = Table(
    'vwAUTHBAL', Base.metadata,
    Column('REQNO', Numeric(18, 0)),
    Column('BDate', DateTime),
    Column('BTime', DateTime),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BOQID', Numeric(18, 0)),
    Column('CODE', Numeric(18, 0)),
    Column('NAME', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('PRICE', MONEY),
    Column('SUBTOTAL', MONEY),
    Column('ATH', Float(53)),
    Column('AUTHBAL', Float(53)),
    Column('comp', Numeric(18, 0))
)


t_vwAttLog = Table(
    'vwAttLog', Base.metadata,
    Column('EmpNo', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LDate', DateTime),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('WK', Numeric(18, 0))
)


t_vwBOQ = Table(
    'vwBOQ', Base.metadata,
    Column('BOQId', Numeric(18, 0), nullable=False),
    Column('BDate', DateTime),
    Column('BTime', DateTime),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('BBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BTotal', MONEY),
    Column('ItemCode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BP', MONEY),
    Column('SubT1', Float(53)),
    Column('ConPrice', MONEY),
    Column('ConTotal', Float(53)),
    Column('BOQT', Float(53)),
    Column('Margin', MONEY),
    Column('Source', Numeric(18, 0)),
    Column('DLQTY', Float(53)),
    Column('QTY', Float(53)),
    Column('CATNAME', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CID', Numeric(18, 0))
)


t_vwBOQDetail = Table(
    'vwBOQDetail', Base.metadata,
    Column('BOQId', Numeric(18, 0), nullable=False),
    Column('BDate', DateTime),
    Column('BTime', DateTime),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwBQGRP = Table(
    'vwBQGRP', Base.metadata,
    Column('BOQNO', Numeric(18, 0), nullable=False),
    Column('GRP', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('QTY', Float(53)),
    Column('REQ', Float(53)),
    Column('ReqBal', Float(53)),
    Column('ATH', Float(53)),
    Column('AthBal', Float(53)),
    Column('DL', Float(53)),
    Column('RTN', Float(53)),
    Column('DLBAL', Float(53)),
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('BAL', Float(53)),
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwBTran = Table(
    'vwBTran', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('TDate', DateTime),
    Column('AccNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Mode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amt', MONEY),
    Column('TType', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwBank = Table(
    'vwBank', Base.metadata,
    Column('TDate', DateTime),
    Column('TType', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Mode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amt', MONEY)
)


t_vwCCustPay = Table(
    'vwCCustPay', Base.metadata,
    Column('name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('address', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('phone', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Route', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PNo', Numeric(18, 0), nullable=False),
    Column('AccNo', Numeric(18, 0)),
    Column('PDate', DateTime),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InvNo', Numeric(18, 0)),
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amount', MONEY),
    Column('PMode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PById', Numeric(18, 0)),
    Column('PByName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RefNo', Numeric(18, 0))
)


t_vwCDBAL = Table(
    'vwCDBAL', Base.metadata,
    Column('DT', DateTime),
    Column('ACC', Numeric(18, 0)),
    Column('SupplierName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BAL', MONEY),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwCDBALDT = Table(
    'vwCDBALDT', Base.metadata,
    Column('dt', DateTime)
)


t_vwCDBALRPT = Table(
    'vwCDBALRPT', Base.metadata,
    Column('DT', DateTime),
    Column('ACC', Numeric(18, 0)),
    Column('SupplierName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BAL', MONEY),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwCDest = Table(
    'vwCDest', Base.metadata,
    Column('RecId', Numeric(18, 0), nullable=False),
    Column('TCode', Numeric(18, 0)),
    Column('toName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CDate', DateTime)
)


t_vwCFrom = Table(
    'vwCFrom', Base.metadata,
    Column('RecId', Numeric(18, 0), nullable=False),
    Column('FCode', Numeric(18, 0)),
    Column('name', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CQty', Float(53)),
    Column('BQty', Float(53)),
    Column('NQty', Float(53)),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CDate', DateTime)
)


t_vwCQ = Table(
    'vwCQ', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('Debtor', Numeric(18, 0)),
    Column('CqNo', Numeric(18, 0)),
    Column('CAmount', MONEY),
    Column('CDate', DateTime),
    Column('Banked', CHAR(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BDate', DateTime),
    Column('BTime', DateTime),
    Column('BBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cleared', CHAR(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Bounced', CHAR(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CON', DateTime),
    Column('PD', CHAR(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Charge', MONEY),
    Column('EDate', DateTime),
    Column('Cat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('cn', Numeric(18, 0))
)


t_vwCSource = Table(
    'vwCSource', Base.metadata,
    Column('RecId', Numeric(18, 0), nullable=False),
    Column('FCode', Numeric(18, 0)),
    Column('CQty', Float(53)),
    Column('BQty', Float(53)),
    Column('NQty', Float(53)),
    Column('sourceName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwCTO = Table(
    'vwCTO', Base.metadata,
    Column('TCode', Numeric(18, 0)),
    Column('toName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RecId', Numeric(18, 0), nullable=False)
)


t_vwCV = Table(
    'vwCV', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('Dt', DateTime),
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EDesc', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('aIn', MONEY),
    Column('aOut', MONEY),
    Column('aTime', DateTime),
    Column('aDBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwCVOut = Table(
    'vwCVOut', Base.metadata,
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('aOut', MONEY, nullable=False)
)


t_vwCallInvItem = Table(
    'vwCallInvItem', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('CallId', Numeric(18, 0)),
    Column('Code', Numeric(18, 0)),
    Column('Name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ReqQty', Float(53)),
    Column('RQty', Float(53)),
    Column('Qty', Float(53)),
    Column('Price', Float(53)),
    Column('SubT', Float(53)),
    Column('Source', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDate', DateTime),
    Column('RTime', DateTime),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwCashV = Table(
    'vwCashV', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('Dt', DateTime),
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EDesc', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('aIn', MONEY),
    Column('aOut', MONEY),
    Column('aTime', DateTime),
    Column('aDBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDDBAL = Table(
    'vwDDBAL', Base.metadata,
    Column('DT', DateTime),
    Column('ACC', Numeric(18, 0)),
    Column('CustName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BAL', MONEY),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDDBALDT = Table(
    'vwDDBALDT', Base.metadata,
    Column('DT', DateTime)
)


t_vwDDBALRPT = Table(
    'vwDDBALRPT', Base.metadata,
    Column('DT', DateTime),
    Column('ACC', Numeric(18, 0)),
    Column('CustName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('BAL', MONEY),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDF = Table(
    'vwDF', Base.metadata,
    Column('MyFid', Numeric(18, 0)),
    Column('FTEXT', Unicode(4000, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDI = Table(
    'vwDI', Base.metadata,
    Column('Dno', Numeric(18, 0), nullable=False),
    Column('DDate', DateTime),
    Column('Amount', MONEY),
    Column('Shop', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Transactedby', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VAT', MONEY),
    Column('Pcode', Numeric(18, 0)),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('ItemPrice', MONEY),
    Column('ItemVat', MONEY),
    Column('ItemCost', MONEY),
    Column('h', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ShopNo', Numeric(18, 0)),
    Column('ProjId', Numeric(18, 0)),
    Column('ProjName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ITO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RefNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CAT', CHAR(10, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDISSUE = Table(
    'vwDISSUE', Base.metadata,
    Column('IP', Numeric(18, 0)),
    Column('SID', Numeric(18, 0)),
    Column('IDate', DateTime),
    Column('PCode', Numeric(18, 0)),
    Column('name', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IQty', Float(53)),
    Column('Tinqty', Float(53)),
    Column('SQty', Float(53)),
    Column('RQty', Float(53)),
    Column('tqty', Float(53)),
    Column('Diff', Float(53)),
    Column('PARTNO', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDLog3 = Table(
    'vwDLog3', Base.metadata,
    Column('MDate', DateTime),
    Column('AccNo', Numeric(18, 0)),
    Column('Narration', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DR', MONEY),
    Column('CR', MONEY),
    Column('Bal', MONEY),
    Column('RecId', Numeric(18, 0), nullable=False),
    Column('CustName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDSI = Table(
    'vwDSI', Base.metadata,
    Column('tradate', DateTime),
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('ItemCode', Numeric(10, 0)),
    Column('qty', Float(53)),
    Column('idno', Numeric(10, 0))
)


t_vwDSIR = Table(
    'vwDSIR', Base.metadata,
    Column('tradate', DateTime),
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('ItemCode', Numeric(10, 0)),
    Column('qty', Float(53)),
    Column('idno', Numeric(10, 0))
)


t_vwDSale = Table(
    'vwDSale', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('tratype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('total', MONEY),
    Column('cash', MONEY),
    Column('change', MONEY),
    Column('vat', MONEY),
    Column('SaleTime', DateTime),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InvNo', Numeric(18, 0)),
    Column('PostedOn', DateTime),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SPId', Numeric(18, 0)),
    Column('Da', MONEY),
    Column('Dis', Numeric(18, 0)),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OrderNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SH', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('phy', MONEY),
    Column('yvat', MONEY),
    Column('nvat', MONEY),
    Column('c1', MONEY),
    Column('mp', MONEY),
    Column('mpc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDSaleItemR = Table(
    'vwDSaleItemR', Base.metadata,
    Column('SaleItemNo', Numeric(18, 0), Identity(), nullable=False),
    Column('trano', Numeric(18, 0)),
    Column('TraDate', DateTime),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('total', MONEY),
    Column('itemcost', MONEY),
    Column('vat', MONEY),
    Column('ItemBP', MONEY),
    Column('EDate', DateTime),
    Column('EId', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LP', MONEY),
    Column('H', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vrc', NCHAR(5, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vr', Float(53))
)


t_vwDSaleR = Table(
    'vwDSaleR', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('tratype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('total', MONEY),
    Column('cash', MONEY),
    Column('change', MONEY),
    Column('vat', MONEY),
    Column('SaleTime', DateTime),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InvNo', Numeric(18, 0)),
    Column('PostedOn', DateTime),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SPId', Numeric(18, 0)),
    Column('Da', MONEY),
    Column('Dis', Numeric(18, 0)),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OrderNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SH', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('phy', MONEY),
    Column('yvat', MONEY),
    Column('nvat', MONEY),
    Column('c1', MONEY),
    Column('mp', MONEY),
    Column('mpc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDSaleitem = Table(
    'vwDSaleitem', Base.metadata,
    Column('SaleItemNo', Numeric(18, 0), Identity(), nullable=False),
    Column('trano', Numeric(5, 0)),
    Column('TraDate', DateTime),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('total', MONEY),
    Column('itemcost', MONEY),
    Column('vat', MONEY),
    Column('ItemBP', MONEY),
    Column('EDate', DateTime),
    Column('EId', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LP', MONEY),
    Column('H', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vrc', NCHAR(5, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vr', Float(53))
)


t_vwDel = Table(
    'vwDel', Base.metadata,
    Column('DelId', Numeric(18, 0), nullable=False),
    Column('ReqNo', Numeric(18, 0)),
    Column('DelDate', DateTime),
    Column('DelTime', DateTime),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemCode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CNo', Numeric(18, 0), nullable=False),
    Column('CYear', Numeric(18, 0), nullable=False),
    Column('DelBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwDelCost1 = Table(
    'vwDelCost1', Base.metadata,
    Column('DDate', DateTime),
    Column('Pcode', Numeric(18, 0)),
    Column('Cost', Float(53))
)


t_vwDelCost2 = Table(
    'vwDelCost2', Base.metadata,
    Column('theCost', Float(53), nullable=False)
)


t_vwDelProf = Table(
    'vwDelProf', Base.metadata,
    Column('DDate', DateTime),
    Column('DNo', Numeric(18, 0)),
    Column('Pcode', Numeric(18, 0)),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('RTQTY', Float(53)),
    Column('Bp', MONEY),
    Column('ItemPrice', MONEY)
)


t_vwDeliveryItem = Table(
    'vwDeliveryItem', Base.metadata,
    Column('DDate', DateTime),
    Column('Pcode', Numeric(18, 0)),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53))
)


t_vwDeliveryItem2 = Table(
    'vwDeliveryItem2', Base.metadata,
    Column('Pcode', Numeric(18, 0)),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53))
)


t_vwDisc = Table(
    'vwDisc', Base.metadata,
    Column('trano', Numeric(10, 0), nullable=False),
    Column('supplier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('sid', Numeric(18, 0)),
    Column('DiscAmt', MONEY, nullable=False),
    Column('PCode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('replenishdate', DateTime)
)


t_vwDisc2 = Table(
    'vwDisc2', Base.metadata,
    Column('PName', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SId', Numeric(18, 0)),
    Column('RefNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amount', MONEY),
    Column('IDate', DateTime),
    Column('DDate', DateTime),
    Column('disc', Numeric(18, 0))
)


t_vwEGnEV = Table(
    'vwEGnEV', Base.metadata,
    Column('egid', Numeric(18, 0)),
    Column('VName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('eg', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('exp', Numeric(18, 0))
)


t_vwExpenseItemTotal = Table(
    'vwExpenseItemTotal', Base.metadata,
    Column('EitemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Petty', MONEY, nullable=False),
    Column('Other', MONEY, nullable=False),
    Column('ItemTotal', MONEY)
)


t_vwExpenseVoteTotal = Table(
    'vwExpenseVoteTotal', Base.metadata,
    Column('VName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Petty', MONEY, nullable=False),
    Column('OAmt', MONEY, nullable=False),
    Column('VoteTotal', MONEY)
)


t_vwGDELI = Table(
    'vwGDELI', Base.metadata,
    Column('DELNO', Numeric(18, 0)),
    Column('APPINO', Numeric(18, 0)),
    Column('GRP', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemCode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('PR', MONEY),
    Column('RECID', Numeric(18, 0), nullable=False),
    Column('RT', Float(53)),
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwGDelItemDetail = Table(
    'vwGDelItemDetail', Base.metadata,
    Column('DELNO', Numeric(18, 0)),
    Column('APPINO', Numeric(18, 0)),
    Column('GRP', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemCode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('PR', MONEY),
    Column('SubTotal', Float(53)),
    Column('ReqNo', Numeric(18, 0)),
    Column('QUOTENo', Numeric(18, 0), nullable=False),
    Column('CID', Numeric(18, 0)),
    Column('CName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CYEAR', Numeric(18, 0)),
    Column('RBY', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDATE', DateTime),
    Column('RECID', Numeric(18, 0), nullable=False)
)


t_vwGP = Table(
    'vwGP', Base.metadata,
    Column('trano', Numeric(5, 0)),
    Column('TraDate', DateTime),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('itemcost', MONEY),
    Column('total', MONEY),
    Column('ItemBP', MONEY),
    Column('ProfMarg', MONEY),
    Column('GrossP', Float(53)),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cat', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwGPR = Table(
    'vwGPR', Base.metadata,
    Column('trano', Numeric(18, 0)),
    Column('TraDate', DateTime),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('itemcost', MONEY),
    Column('total', MONEY),
    Column('ItemBP', MONEY),
    Column('ProfMarg', MONEY),
    Column('GrossP', Float(53)),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cat', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwGREQ = Table(
    'vwGREQ', Base.metadata,
    Column('ReqNo', Numeric(18, 0), nullable=False),
    Column('BQNo', Numeric(18, 0)),
    Column('RDATE', DateTime),
    Column('RTIME', DateTime),
    Column('RUSER', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('GRP', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('CID', Numeric(18, 0)),
    Column('CName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CYEAR', Numeric(18, 0)),
    Column('RBY', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwGREQNew = Table(
    'vwGREQNew', Base.metadata,
    Column('ReqNo', Numeric(18, 0), nullable=False),
    Column('BQNo', Numeric(18, 0)),
    Column('CID', Numeric(18, 0)),
    Column('CYEAR', Numeric(18, 0)),
    Column('CCLIENT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDATE', DateTime),
    Column('RTIME', DateTime),
    Column('RBY', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RUSER', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwGREQS = Table(
    'vwGREQS', Base.metadata,
    Column('ReqNo', Numeric(18, 0), nullable=False),
    Column('BQNo', Numeric(18, 0)),
    Column('CID', Numeric(18, 0)),
    Column('CYEAR', Numeric(18, 0)),
    Column('CCLIENT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDATE', DateTime),
    Column('RTIME', DateTime),
    Column('RBY', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RUSER', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwGSR = Table(
    'vwGSR', Base.metadata,
    Column('ReqNo', Numeric(18, 0), nullable=False),
    Column('GenId', Numeric(18, 0)),
    Column('RDate', DateTime),
    Column('RTime', DateTime),
    Column('RBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RTotal', MONEY),
    Column('SDate', DateTime),
    Column('SNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('CID', Numeric(18, 0)),
    Column('OD', Unicode(200, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LSD', DateTime),
    Column('ItemCode', Numeric(18, 0)),
    Column('Itemname', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('UQTY', Float(53)),
    Column('BP', MONEY),
    Column('ST', MONEY),
    Column('SOURCE', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RQTY', Float(53)),
    Column('SBY', Numeric(18, 0))
)


t_vwGen = Table(
    'vwGen', Base.metadata,
    Column('GID', Numeric(18, 0), nullable=False),
    Column('SNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('CID', Numeric(18, 0)),
    Column('name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OD', Unicode(200, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LSD', DateTime)
)


t_vwGenSR = Table(
    'vwGenSR', Base.metadata,
    Column('ReqNo', Numeric(18, 0), nullable=False),
    Column('GenId', Numeric(18, 0)),
    Column('SNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('CID', Numeric(18, 0)),
    Column('name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDate', DateTime)
)


t_vwHS = Table(
    'vwHS', Base.metadata,
    Column('HSNO', Numeric(18, 0), nullable=False),
    Column('DT', DateTime),
    Column('HBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('HT', DateTime),
    Column('HRE', Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cust', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RefNo', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SType', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('stat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('rd', DateTime),
    Column('rby', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('sno', Numeric(18, 0)),
    Column('CODE', Numeric(18, 0)),
    Column('INAME', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('PRICE', MONEY),
    Column('ST', MONEY),
    Column('VAT', MONEY),
    Column('TOT', MONEY),
    Column('BP', MONEY),
    Column('VTR', Float(53)),
    Column('hty', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ssno', Numeric(18, 0))
)


t_vwHSMX = Table(
    'vwHSMX', Base.metadata,
    Column('dt', DateTime)
)


t_vwHSR = Table(
    'vwHSR', Base.metadata,
    Column('HSNO', Numeric(18, 0), nullable=False),
    Column('DT', DateTime),
    Column('HBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('HT', DateTime),
    Column('HRE', Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cust', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RefNo', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SType', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('stat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('rd', DateTime),
    Column('rby', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('sno', Numeric(18, 0)),
    Column('CODE', Numeric(18, 0)),
    Column('INAME', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('PRICE', MONEY),
    Column('ST', MONEY),
    Column('VAT', MONEY),
    Column('TOT', MONEY),
    Column('BP', MONEY),
    Column('VTR', Float(53)),
    Column('hty', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ssno', Numeric(18, 0))
)


t_vwHSS = Table(
    'vwHSS', Base.metadata,
    Column('stat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CODE', Numeric(18, 0)),
    Column('INAME', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('qtystock', Float(53)),
    Column('AvailQty', Float(53))
)


t_vwHist120 = Table(
    'vwHist120', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwHist120M = Table(
    'vwHist120M', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwHist30 = Table(
    'vwHist30', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwHist60 = Table(
    'vwHist60', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwHist90 = Table(
    'vwHist90', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwIssueTransfer = Table(
    'vwIssueTransfer', Base.metadata,
    Column('tno', Numeric(18, 0)),
    Column('TDATE', DateTime),
    Column('IP', Numeric(18, 0)),
    Column('SD', DateTime),
    Column('ED', DateTime),
    Column('F', Numeric(18, 0)),
    Column('FromName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('T', Numeric(18, 0)),
    Column('ToName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('PCODE', Numeric(18, 0)),
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('bpw', MONEY),
    Column('SubTotal', Float(53))
)


t_vwItemGP = Table(
    'vwItemGP', Base.metadata,
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('ItemCost', Float(53)),
    Column('Total', MONEY),
    Column('Cost', Float(53)),
    Column('Margin', Float(53)),
    Column('ItemGross', Float(53))
)


t_vwItemSummary = Table(
    'vwItemSummary', Base.metadata,
    Column('Itemname', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SalePerson', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IDate', DateTime),
    Column('SID', Numeric(18, 0)),
    Column('PCode', Numeric(18, 0)),
    Column('IQty', Float(53)),
    Column('SQty', Float(53)),
    Column('RQty', Float(53)),
    Column('Diff', Float(53)),
    Column('spw', MONEY),
    Column('WValue', Float(53)),
    Column('IP', Numeric(18, 0))
)


t_vwItemTotal = Table(
    'vwItemTotal', Base.metadata,
    Column('EitemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Petty', MONEY, nullable=False),
    Column('Other', MONEY, nullable=False),
    Column('ItemTotal', MONEY)
)


t_vwLNI = Table(
    'vwLNI', Base.metadata,
    Column('LDate', DateTime),
    Column('LBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EmpNo', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InitAmt', MONEY),
    Column('InitInstall', MONEY),
    Column('Amt', MONEY),
    Column('NewInstall', MONEY)
)


t_vwLNIA = Table(
    'vwLNIA', Base.metadata,
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EmpNo', Numeric(18, 0)),
    Column('InitAmt', MONEY),
    Column('InitInstall', MONEY),
    Column('NewInstall', MONEY),
    Column('Amt', MONEY),
    Column('LDate', DateTime),
    Column('LBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwLNMI = Table(
    'vwLNMI', Base.metadata,
    Column('EmpNo', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InitAmt', MONEY),
    Column('InitInstall', MONEY),
    Column('Amt', MONEY),
    Column('NewInstall', MONEY),
    Column('LDate', DateTime),
    Column('LBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwLPDiff = Table(
    'vwLPDiff', Base.metadata,
    Column('LpoNo', Numeric(18, 0)),
    Column('ICode', Numeric(18, 0)),
    Column('Qty', Float(53)),
    Column('DQty', Float(53)),
    Column('MyDiff', Float(53))
)


t_vwLPO = Table(
    'vwLPO', Base.metadata,
    Column('LpoNo', Numeric(18, 0), nullable=False),
    Column('supplierid', Numeric(10, 0), nullable=False),
    Column('SupplierName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('telno', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('fax', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('town', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Notes', Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LDate', DateTime),
    Column('LUser', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ICode', Numeric(18, 0)),
    Column('Qty', Float(53)),
    Column('Price', MONEY),
    Column('ST', MONEY),
    Column('GT', MONEY),
    Column('Nar', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VAT', MONEY),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LPOSubTotal', MONEY),
    Column('PARTNO', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('postal', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemTotal', MONEY),
    Column('IVAT', MONEY),
    Column('INCEXC', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwMSale = Table(
    'vwMSale', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('tratype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('total', MONEY),
    Column('cash', MONEY),
    Column('change', MONEY),
    Column('vat', MONEY),
    Column('SaleTime', DateTime),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InvNo', Numeric(18, 0)),
    Column('PostedOn', DateTime),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SPId', Numeric(18, 0)),
    Column('Da', MONEY),
    Column('Dis', Numeric(18, 0)),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OrderNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SH', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('phy', MONEY),
    Column('yvat', MONEY),
    Column('nvat', MONEY),
    Column('c1', MONEY),
    Column('mp', MONEY),
    Column('mpc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwMSaleD = Table(
    'vwMSaleD', Base.metadata,
    Column('SaleItemNo', Numeric(18, 0), Identity(), nullable=False),
    Column('trano', Numeric(5, 0)),
    Column('TraDate', DateTime),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('total', MONEY),
    Column('itemcost', MONEY),
    Column('vat', MONEY),
    Column('ItemBP', MONEY),
    Column('EDate', DateTime),
    Column('EId', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LP', MONEY),
    Column('H', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vrc', NCHAR(5, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vr', Float(53))
)


t_vwMinChr = Table(
    'vwMinChr', Base.metadata,
    Column('MinChr', Integer)
)


t_vwMonthGP = Table(
    'vwMonthGP', Base.metadata,
    Column('MyYear', Integer),
    Column('MonId', Integer),
    Column('Total', MONEY),
    Column('Gross', Float(53))
)


t_vwNewReq = Table(
    'vwNewReq', Base.metadata,
    Column('ReqNo', Numeric(18, 0), nullable=False),
    Column('RDate', DateTime),
    Column('RTime', DateTime),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CNo', Numeric(18, 0), nullable=False),
    Column('CYear', Numeric(18, 0), nullable=False),
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwOEItem = Table(
    'vwOEItem', Base.metadata,
    Column('EItem', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OAmt', MONEY)
)


t_vwOESub = Table(
    'vwOESub', Base.metadata,
    Column('subv', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OtherTotal', MONEY)
)


t_vwOEVote = Table(
    'vwOEVote', Base.metadata,
    Column('VName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('OAmt', MONEY)
)


t_vwOEntry = Table(
    'vwOEntry', Base.metadata,
    Column('VName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SDate', DateTime),
    Column('EDate', DateTime),
    Column('OtherAmt', MONEY, nullable=False),
    Column('EItem', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('subv', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwOEntryR = Table(
    'vwOEntryR', Base.metadata,
    Column('VName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SDate', DateTime),
    Column('EDate', DateTime),
    Column('OtherAmt', MONEY, nullable=False),
    Column('EItem', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('subv', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwOPSRDate = Table(
    'vwOPSRDate', Base.metadata,
    Column('Acc', Numeric(18, 0)),
    Column('SoldTo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cash', MONEY),
    Column('Inv', MONEY),
    Column('VAT', MONEY),
    Column('Total', MONEY),
    Column('MyCnt', Integer)
)


t_vwOPSRUser = Table(
    'vwOPSRUser', Base.metadata,
    Column('Dt', DateTime),
    Column('Acc', Numeric(18, 0)),
    Column('SoldTo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cash', MONEY),
    Column('Inv', MONEY),
    Column('VAT', MONEY),
    Column('Total', MONEY),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('MyCnt', Integer)
)


t_vwOpenVal = Table(
    'vwOpenVal', Base.metadata,
    Column('openval', Float(53)),
    Column('SDate', DateTime)
)


t_vwPAPP = Table(
    'vwPAPP', Base.metadata,
    Column('AppId', Numeric(18, 0), nullable=False),
    Column('CustId', Numeric(18, 0)),
    Column('name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AppDate', DateTime),
    Column('RefNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwPCEntry = Table(
    'vwPCEntry', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('SDate', DateTime),
    Column('EDate', DateTime),
    Column('Votehead', Unicode(200, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Narration', Unicode(300, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amount', MONEY),
    Column('Pmode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ABy', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RBy', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SubAcc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Item', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CB', Numeric(18, 0))
)


t_vwPCEntryR = Table(
    'vwPCEntryR', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('SDate', DateTime),
    Column('EDate', DateTime),
    Column('Votehead', Unicode(200, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Narration', Unicode(300, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amount', MONEY),
    Column('Pmode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ABy', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RBy', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SubAcc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Item', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CB', Numeric(18, 0))
)


t_vwPCS = Table(
    'vwPCS', Base.metadata,
    Column('Votehead', Unicode(200, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amount', MONEY)
)


t_vwPLI = Table(
    'vwPLI', Base.metadata,
    Column('pcode', Numeric(18, 0), nullable=False),
    Column('name', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('bpw', MONEY),
    Column('spw', MONEY),
    Column('Marg1', MONEY),
    Column('Ind1', MONEY),
    Column('spr', MONEY),
    Column('Marg2', MONEY),
    Column('Ind2', MONEY)
)


t_vwPPA = Table(
    'vwPPA', Base.metadata,
    Column('ADATE', DateTime),
    Column('CNO', Numeric(18, 0)),
    Column('CYEAR', Numeric(18, 0)),
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NARR', Unicode(2000, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CIN', MONEY),
    Column('COUT', MONEY),
    Column('BAL', MONEY),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RECID', Numeric(18, 0), nullable=False)
)


t_vwPetty = Table(
    'vwPetty', Base.metadata,
    Column('VName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SDate', DateTime),
    Column('EDate', DateTime),
    Column('PettyAmt', MONEY, nullable=False),
    Column('Item', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('subacc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwPettyItem = Table(
    'vwPettyItem', Base.metadata,
    Column('ITEM', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Petty', MONEY)
)


t_vwPettyR = Table(
    'vwPettyR', Base.metadata,
    Column('VName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SDate', DateTime),
    Column('EDate', DateTime),
    Column('PettyAmt', MONEY, nullable=False),
    Column('Item', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('subacc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwPettySub = Table(
    'vwPettySub', Base.metadata,
    Column('subacc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PettyTotal', MONEY)
)


t_vwPettyVote = Table(
    'vwPettyVote', Base.metadata,
    Column('VName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Petty', MONEY)
)


t_vwProjDel = Table(
    'vwProjDel', Base.metadata,
    Column('CNo', Numeric(18, 0)),
    Column('CName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CYEAR', Numeric(18, 0)),
    Column('BQNo', Numeric(18, 0)),
    Column('DELDATE', DateTime),
    Column('GRP', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemCode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DelQty', Float(53)),
    Column('ReturnQty', Float(53)),
    Column('MyQty', Float(53)),
    Column('BP', MONEY),
    Column('MyTotal', Float(53)),
    Column('Cat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AppId', Numeric(18, 0)),
    Column('DELNO', Numeric(18, 0), nullable=False),
    Column('ReqNo', Numeric(18, 0), nullable=False)
)


t_vwProjDelItem = Table(
    'vwProjDelItem', Base.metadata,
    Column('CNo', Numeric(18, 0)),
    Column('CName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CYEAR', Numeric(18, 0)),
    Column('BQNo', Numeric(18, 0)),
    Column('DELDATE', DateTime),
    Column('GRP', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ItemCode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DelQty', Float(53)),
    Column('ReturnQty', Float(53)),
    Column('MyQty', Float(53)),
    Column('BP', MONEY),
    Column('MyCost', Float(53)),
    Column('MyTotal', Float(53)),
    Column('CAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CID', Numeric(18, 0)),
    Column('DELNO', Numeric(18, 0)),
    Column('BUYP', MONEY),
    Column('Margin', MONEY),
    Column('DelProf', Float(53))
)


t_vwProjDeli = Table(
    'vwProjDeli', Base.metadata,
    Column('ProjId', Numeric(18, 0)),
    Column('ProjName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DDate', DateTime),
    Column('REFNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('RTQTY', Float(53)),
    Column('ItemPrice', MONEY),
    Column('ItemVat', MONEY),
    Column('ItemCost', MONEY),
    Column('BP', MONEY),
    Column('Dno', Numeric(18, 0), nullable=False)
)


t_vwPurchase = Table(
    'vwPurchase', Base.metadata,
    Column('replenishdate', DateTime),
    Column('PCode', Numeric(18, 0)),
    Column('Qty', Float(53))
)


t_vwQuote = Table(
    'vwQuote', Base.metadata,
    Column('QUOTENo', Numeric(18, 0), nullable=False),
    Column('CID', Numeric(18, 0)),
    Column('CName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Notes', Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('GT', MONEY),
    Column('LDate', DateTime),
    Column('LUser', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ICode', Numeric(18, 0)),
    Column('Qty', Float(53)),
    Column('Price', MONEY),
    Column('ST', MONEY),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NAr', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SId', Numeric(18, 0)),
    Column('name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VAT', MONEY),
    Column('QST', MONEY),
    Column('PARTNO', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VATRate', Float(53)),
    Column('VATAmt', MONEY),
    Column('VATSTAT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ct', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwREQ = Table(
    'vwREQ', Base.metadata,
    Column('ReqNo', Numeric(18, 0), nullable=False),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDate', DateTime),
    Column('RTime', DateTime),
    Column('BOQ', Numeric(18, 0)),
    Column('CODE', Numeric(18, 0)),
    Column('NAME', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('PRICE', MONEY),
    Column('SUBTOTAL', MONEY),
    Column('RBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwREQITEM = Table(
    'vwREQITEM', Base.metadata,
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CODE', Numeric(18, 0)),
    Column('NAME', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Request', Float(53)),
    Column('Authorised', Float(53)),
    Column('RQ', Float(53)),
    Column('ATH', Float(53)),
    Column('DL', Float(53))
)


t_vwRORD = Table(
    'vwRORD', Base.metadata,
    Column('QUOTENo', Numeric(18, 0), nullable=False),
    Column('CID', Numeric(18, 0)),
    Column('CName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Notes', Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('GT', MONEY),
    Column('LDate', DateTime),
    Column('LUser', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VAT', MONEY),
    Column('ST', MONEY),
    Column('CYEAR', Numeric(18, 0)),
    Column('CCLIENT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ICode', Numeric(18, 0)),
    Column('ItemName', Unicode(1000, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('Price', MONEY),
    Column('ItemSubtotal', MONEY),
    Column('NAr', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwReb = Table(
    'vwReb', Base.metadata,
    Column('PName', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SId', Numeric(18, 0)),
    Column('RefNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amount', MONEY),
    Column('IDate', DateTime),
    Column('DDate', DateTime),
    Column('rbt', Numeric(18, 0))
)


t_vwReqItemSum = Table(
    'vwReqItemSum', Base.metadata,
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('REQNO', Numeric(18, 0)),
    Column('CODE', Numeric(18, 0)),
    Column('NAME', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53)),
    Column('PRICE', MONEY),
    Column('SUBTOTAL', MONEY),
    Column('ATH', Float(53)),
    Column('DL', Float(53)),
    Column('RDate', DateTime),
    Column('RTime', DateTime),
    Column('RBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwReqSum = Table(
    'vwReqSum', Base.metadata,
    Column('ReqNo', Numeric(18, 0), nullable=False),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDate', DateTime),
    Column('RTime', DateTime),
    Column('RBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('ReqTotal', Float(53))
)


t_vwRout = Table(
    'vwRout', Base.metadata,
    Column('ReturnNo', Numeric(10, 0), nullable=False),
    Column('Trano', Numeric(18, 0)),
    Column('TotalAmt', MONEY),
    Column('ReturnDate', DateTime),
    Column('supplier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('supplierid', Numeric(10, 0), nullable=False),
    Column('dmode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('docno', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSCON = Table(
    'vwSCON', Base.metadata,
    Column('RecId', Numeric(18, 0), nullable=False),
    Column('CDate', DateTime),
    Column('FCode', Numeric(18, 0)),
    Column('fromName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CQty', Float(53)),
    Column('BQty', Float(53)),
    Column('NQty', Float(53)),
    Column('TCode', Numeric(18, 0)),
    Column('toName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSCard = Table(
    'vwSCard', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('PCode', Numeric(18, 0)),
    Column('MDate', DateTime),
    Column('Narration', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Category', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QIn', Float(53)),
    Column('QOut', Float(53)),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NewQty', Float(53)),
    Column('AllQty', Float(53)),
    Column('GRP', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSConvert = Table(
    'vwSConvert', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('FCode', Numeric(18, 0)),
    Column('CQty', Float(53)),
    Column('BQty', Float(53)),
    Column('NQty', Float(53)),
    Column('TCode', Numeric(18, 0)),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CDate', DateTime)
)


t_vwSDEL = Table(
    'vwSDEL', Base.metadata,
    Column('Dno', Numeric(18, 0), nullable=False),
    Column('DDate', DateTime),
    Column('Amount', MONEY),
    Column('VAT', MONEY),
    Column('Transactedby', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Shop', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('ItemPrice', MONEY),
    Column('ItemVat', MONEY),
    Column('ItemCost', MONEY),
    Column('CAT', CHAR(10, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RefNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RecId', Numeric(18, 0), nullable=False)
)


t_vwSDP = Table(
    'vwSDP', Base.metadata,
    Column('Dno', Numeric(18, 0), nullable=False),
    Column('DDate', DateTime),
    Column('ShopNo', Numeric(18, 0)),
    Column('ShopName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Pcode', Numeric(18, 0)),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('RTQTY', Float(53)),
    Column('MyNewQty', Float(53)),
    Column('BP', MONEY),
    Column('MyCost', Float(53)),
    Column('ItemPrice', MONEY),
    Column('MySale', Float(53)),
    Column('MyProfit', Float(53))
)


t_vwSHIST120 = Table(
    'vwSHIST120', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwSHIST120M = Table(
    'vwSHIST120M', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwSHIST30 = Table(
    'vwSHIST30', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwSHIST60 = Table(
    'vwSHIST60', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwSHIST90 = Table(
    'vwSHIST90', Base.metadata,
    Column('Idno', Numeric(18, 0)),
    Column('Balance', MONEY)
)


t_vwSIP = Table(
    'vwSIP', Base.metadata,
    Column('RECID', Numeric(18, 0), nullable=False),
    Column('SHOPID', Numeric(18, 0), nullable=False),
    Column('ITEMCODE', Numeric(18, 0), nullable=False),
    Column('PRICE', MONEY),
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ShopName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSISS = Table(
    'vwSISS', Base.metadata,
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('Total', MONEY)
)


t_vwSM = Table(
    'vwSM', Base.metadata,
    Column('RECNO', Numeric(18, 0), Identity(), nullable=False),
    Column('SDate', DateTime),
    Column('PCode', Numeric(18, 0)),
    Column('OTime', DateTime),
    Column('OQty', Float(53)),
    Column('OPrice', MONEY),
    Column('OUser', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CTime', DateTime),
    Column('CQty', Float(53)),
    Column('CPrice', MONEY),
    Column('CUser', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSMD = Table(
    'vwSMD', Base.metadata,
    Column('SDate', DateTime)
)


t_vwSMDT = Table(
    'vwSMDT', Base.metadata,
    Column('SDate', DateTime)
)


t_vwSMV = Table(
    'vwSMV', Base.metadata,
    Column('SDate', DateTime),
    Column('PCode', Numeric(18, 0)),
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OQty', Float(53)),
    Column('OPrice', MONEY),
    Column('OValue', Float(53)),
    Column('CQty', Float(53)),
    Column('CPrice', MONEY),
    Column('CValue', Float(53)),
    Column('CVal', Float(53)),
    Column('OUser', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CUser', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSPSales = Table(
    'vwSPSales', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('total', MONEY),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SPId', Numeric(18, 0)),
    Column('Name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSP_S_D = Table(
    'vwSP_S_D', Base.metadata,
    Column('recid', Numeric(18, 0), Identity(), nullable=False),
    Column('tdate', DateTime),
    Column('spid', Numeric(18, 0)),
    Column('spname', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('itemname', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('cos', MONEY),
    Column('total', MONEY),
    Column('prof', MONEY),
    Column('cat', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TraNo', Numeric(18, 0)),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('STO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSTAR = Table(
    'vwSTAR', Base.metadata,
    Column('STNO', Numeric(18, 0), nullable=False),
    Column('PCODE', Numeric(18, 0), nullable=False),
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('F_Shop', Float(53)),
    Column('F_Feeds', Float(53)),
    Column('F_Buffer', Float(53)),
    Column('F_Total', Float(53)),
    Column('C_Shop', Float(53)),
    Column('C_Feeds', Float(53)),
    Column('C_Buffer', Float(53)),
    Column('C_Total', Float(53)),
    Column('ShDef', Float(53)),
    Column('FsDef', Float(53)),
    Column('BufferDef', Float(53)),
    Column('TotalDef', Float(53))
)


t_vwSTAnalysis = Table(
    'vwSTAnalysis', Base.metadata,
    Column('STNO', Numeric(18, 0), nullable=False),
    Column('PCODE', Numeric(18, 0), nullable=False),
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('F_Shop', Float(53)),
    Column('F_Feeds', Float(53)),
    Column('F_Buffer', Float(53)),
    Column('F_Total', Float(53)),
    Column('C_Shop', Float(53)),
    Column('C_Feeds', Float(53)),
    Column('C_Buffer', Float(53)),
    Column('C_Total', Float(53)),
    Column('ShDef', Float(53)),
    Column('FsDef', Float(53)),
    Column('BufferDef', Float(53)),
    Column('TotalDef', Float(53))
)


t_vwSTE = Table(
    'vwSTE', Base.metadata,
    Column('EntNo', Numeric(18, 0), nullable=False),
    Column('EDate', DateTime),
    Column('EBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('StNo', Numeric(18, 0)),
    Column('StArea', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Narr', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PCODE', Numeric(18, 0)),
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53))
)


t_vwSTER = Table(
    'vwSTER', Base.metadata,
    Column('EntNo', Numeric(18, 0), nullable=False),
    Column('EDate', DateTime),
    Column('EBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('StNo', Numeric(18, 0)),
    Column('StArea', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Narr', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PCODE', Numeric(18, 0)),
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QTY', Float(53))
)


t_vwSale = Table(
    'vwSale', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('tratype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('total', MONEY),
    Column('cash', MONEY),
    Column('change', MONEY),
    Column('vat', MONEY),
    Column('SaleTime', DateTime),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InvNo', Numeric(18, 0)),
    Column('PostedOn', DateTime),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SPId', Numeric(18, 0)),
    Column('Da', MONEY),
    Column('Dis', Numeric(18, 0)),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OrderNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SH', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('phy', MONEY),
    Column('yvat', MONEY),
    Column('nvat', MONEY),
    Column('c1', MONEY),
    Column('mp', MONEY),
    Column('mpc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSaleD1 = Table(
    'vwSaleD1', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('tratype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('total', MONEY),
    Column('cash', MONEY),
    Column('change', MONEY),
    Column('vat', MONEY),
    Column('SaleTime', DateTime),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InvNo', Numeric(18, 0)),
    Column('PostedOn', DateTime),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SPId', Numeric(18, 0)),
    Column('Da', MONEY),
    Column('Dis', Numeric(18, 0)),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OrderNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SH', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('phy', MONEY),
    Column('yvat', MONEY),
    Column('nvat', MONEY),
    Column('c1', MONEY),
    Column('mp', MONEY),
    Column('mpc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSaleD1D = Table(
    'vwSaleD1D', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('total', MONEY),
    Column('vat', MONEY),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSaleD1R = Table(
    'vwSaleD1R', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('total', MONEY),
    Column('vat', MONEY),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSaleItem = Table(
    'vwSaleItem', Base.metadata,
    Column('SaleItemNo', Numeric(18, 0), Identity(), nullable=False),
    Column('trano', Numeric(5, 0)),
    Column('TraDate', DateTime),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('total', MONEY),
    Column('itemcost', MONEY),
    Column('vat', MONEY),
    Column('ItemBP', MONEY),
    Column('EDate', DateTime),
    Column('EId', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LP', MONEY),
    Column('H', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vrc', NCHAR(5, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vr', Float(53))
)


t_vwSaleItemPrint = Table(
    'vwSaleItemPrint', Base.metadata,
    Column('SaleItemNo', Numeric(18, 0), Identity(), nullable=False),
    Column('trano', Numeric(18, 0)),
    Column('TraDate', DateTime),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('total', MONEY),
    Column('itemcost', MONEY),
    Column('vat', MONEY),
    Column('ItemBP', MONEY),
    Column('EDate', DateTime),
    Column('EId', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LP', MONEY),
    Column('H', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vrc', NCHAR(5, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('vr', Float(53))
)


t_vwSalePrint = Table(
    'vwSalePrint', Base.metadata,
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('tradate', DateTime),
    Column('tratype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('saletype', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idno', Numeric(10, 0)),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('total', MONEY),
    Column('cash', MONEY),
    Column('change', MONEY),
    Column('vat', MONEY),
    Column('SaleTime', DateTime),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('InvNo', Numeric(18, 0)),
    Column('PostedOn', DateTime),
    Column('PBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NBal', MONEY),
    Column('OBal', MONEY),
    Column('SPId', Numeric(18, 0)),
    Column('Da', MONEY),
    Column('Dis', Numeric(18, 0)),
    Column('RegNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('OrderNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DNO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SH', Numeric(18, 0)),
    Column('PartNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('phy', MONEY),
    Column('yvat', MONEY),
    Column('nvat', MONEY),
    Column('c1', MONEY),
    Column('mp', MONEY),
    Column('mpc', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSaleSummary = Table(
    'vwSaleSummary', Base.metadata,
    Column('PCODE', Numeric(18, 0)),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SaleQty', Float(53), nullable=False),
    Column('DelQty', Float(53), nullable=False),
    Column('QEdit2', Float(53)),
    Column('QOff', Float(53)),
    Column('Total', Float(53), nullable=False),
    Column('Cat', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qtystock', Float(53)),
    Column('Ostock', Float(53)),
    Column('Cstock', Float(53)),
    Column('Pstock', Float(53)),
    Column('QEdit1', Float(53)),
    Column('Expr1', Float(53)),
    Column('Expr2', Float(53))
)


t_vwSale_Item = Table(
    'vwSale_Item', Base.metadata,
    Column('TraDate', DateTime),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('total', MONEY)
)


t_vwSale_Item2 = Table(
    'vwSale_Item2', Base.metadata,
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('Total', MONEY)
)


t_vwSalesPersonDelivery = Table(
    'vwSalesPersonDelivery', Base.metadata,
    Column('DDate', DateTime),
    Column('sid', Numeric(18, 0)),
    Column('sname', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('RTQTY', Float(53)),
    Column('ItemPrice', MONEY),
    Column('ItemVat', MONEY),
    Column('ItemCost', MONEY),
    Column('BP', MONEY),
    Column('Prof', Float(53)),
    Column('Dno', Numeric(18, 0), nullable=False),
    Column('Transactedby', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Shop', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwSalesPersonSale = Table(
    'vwSalesPersonSale', Base.metadata,
    Column('tradate', DateTime),
    Column('SPId', Numeric(18, 0)),
    Column('Name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ItemCode', Numeric(10, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('qty', Float(53)),
    Column('itemcost', MONEY),
    Column('total', MONEY),
    Column('ItemBP', MONEY),
    Column('Prof', Float(53)),
    Column('TraNo', Numeric(18, 0), nullable=False),
    Column('cashier', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SoldTo', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwShopLPO = Table(
    'vwShopLPO', Base.metadata,
    Column('LpoNo', Numeric(18, 0), nullable=False),
    Column('LDate', DateTime),
    Column('SID', Numeric(18, 0)),
    Column('SupplierName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ICode', Numeric(18, 0)),
    Column('ItemName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('DQTY', Float(53)),
    Column('BalQty', Float(53)),
    Column('Price', MONEY),
    Column('ST', MONEY),
    Column('ItemRef', Numeric(18, 0), nullable=False),
    Column('IVAT', MONEY),
    Column('INCEXC', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwStockConvert = Table(
    'vwStockConvert', Base.metadata,
    Column('RecId', Numeric(18, 0), nullable=False),
    Column('FCode', Numeric(18, 0)),
    Column('sourceName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CQty', Float(53)),
    Column('BQty', Float(53)),
    Column('NQty', Float(53)),
    Column('TCode', Numeric(18, 0)),
    Column('toName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CDate', DateTime)
)


t_vwStoreItem = Table(
    'vwStoreItem', Base.metadata,
    Column('SID', Numeric(18, 0), nullable=False),
    Column('SName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('PCode', Numeric(18, 0), nullable=False),
    Column('ItemName', Unicode(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53))
)


t_vwStoreItemTotal = Table(
    'vwStoreItemTotal', Base.metadata,
    Column('PCode', Numeric(18, 0), nullable=False),
    Column('Qty', Float(53))
)


t_vwSubAccExp = Table(
    'vwSubAccExp', Base.metadata,
    Column('EVS', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('PettyTotal', MONEY, nullable=False),
    Column('OtherTotal', MONEY, nullable=False),
    Column('Total', MONEY)
)


t_vwTCall = Table(
    'vwTCall', Base.metadata,
    Column('CallId', Numeric(18, 0), Identity(), nullable=False),
    Column('CDate', DateTime),
    Column('CBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Narr', Unicode(500, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PR', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CustId', Numeric(18, 0)),
    Column('ASS', CHAR(1, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ASSBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EDate', DateTime),
    Column('Name', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwTI = Table(
    'vwTI', Base.metadata,
    Column('IID', Numeric(18, 0), nullable=False),
    Column('IDate', DateTime),
    Column('TID', Numeric(18, 0)),
    Column('TName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ITO', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PROJ', Numeric(18, 0)),
    Column('PROJYR', Numeric(18, 0)),
    Column('DDATE', DateTime),
    Column('DBY', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RT', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RTBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RDate', DateTime),
    Column('Company', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('URTBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwUGR = Table(
    'vwUGR', Base.metadata,
    Column('GCODE', Numeric(18, 0), nullable=False),
    Column('GNAME', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ACODE', Unicode(5, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('AName', String(255, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ACC', Numeric(18, 0))
)


t_vwVAttLog = Table(
    'vwVAttLog', Base.metadata,
    Column('Company', Unicode(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('RecId', Numeric(18, 0), nullable=False),
    Column('LDate', DateTime),
    Column('EmpNo', Numeric(18, 0)),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('WK', Numeric(18, 0)),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwVCWage = Table(
    'vwVCWage', Base.metadata,
    Column('WDate', DateTime),
    Column('EmpNo', Numeric(18, 0)),
    Column('CNo', Numeric(18, 0)),
    Column('CYear', Numeric(18, 0)),
    Column('Amount', MONEY),
    Column('EmpName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwWK = Table(
    'vwWK', Base.metadata,
    Column('WeekID', Numeric(18, 0), Identity(), nullable=False),
    Column('SDate', DateTime),
    Column('WYr', Integer),
    Column('EDate', DateTime)
)


t_vwdobal = Table(
    'vwdobal', Base.metadata,
    Column('RecId', Numeric(18, 0), Identity(), nullable=False),
    Column('CId', Numeric(18, 0)),
    Column('RefNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Amount', MONEY),
    Column('IDate', DateTime),
    Column('DBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DDate', DateTime),
    Column('DTime', DateTime)
)


t_vwrc = Table(
    'vwrc', Base.metadata,
    Column('trano', Numeric(10, 0), Identity(), nullable=False),
    Column('RefNo', Numeric(18, 0)),
    Column('id', Numeric(10, 0)),
    Column('pmode', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('amount', MONEY),
    Column('DAllowed', MONEY),
    Column('tradate', DateTime),
    Column('chequeno', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('dbank', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('DoneBy', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PId', Numeric(18, 0)),
    Column('PN', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('VatWith', MONEY),
    Column('VatWithRefNo', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vwsp = Table(
    'vwsp', Base.metadata,
    Column('Dno', Numeric(18, 0), nullable=False),
    Column('DDate', DateTime),
    Column('ShopNo', Numeric(18, 0)),
    Column('ShopName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Pcode', Numeric(18, 0)),
    Column('PName', Unicode(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Qty', Float(53)),
    Column('RTQTY', Float(53)),
    Column('MyNewQty', Float(53)),
    Column('BP', MONEY),
    Column('MyCost', Float(53)),
    Column('ItemPrice', MONEY),
    Column('MySale', Float(53)),
    Column('MyProfit', Float(53))
)
