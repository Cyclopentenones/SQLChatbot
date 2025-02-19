from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, Numeric, SmallInteger, DateTime, ForeignKey
from datetime import datetime

class KHOA(SQLModel, table=True):
    MAKHOA: str = Field(sa_column=Column(String(4), primary_key=True))
    TENKHOA: str = Field(sa_column=Column(String(40)))
    NGTLAP: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True))
    TRGKHOA: Optional[str] = Field(sa_column=Column(String(4), nullable=True))
    class Config:
     from_attributes = True

class MONHOC(SQLModel, table=True):
    MAMH: str = Field(sa_column=Column(String(10), primary_key=True))
    TENMH: str = Field(sa_column=Column(String(40)))
    TCLT: int = Field(sa_column=Column(SmallInteger))
    TCTH: int = Field(sa_column=Column(SmallInteger))
    MAKHOA: str = Field(sa_column=Column(String(4), ForeignKey("khoa.MAKHOA"))) 
    class Config:
        from_attributes = True

class DIEUKIEN(SQLModel, table=True):
    MAMH: str = Field(sa_column=Column(String(10), ForeignKey("monhoc.MAMH"), primary_key=True))
    MAMH_TRUOC: str = Field(sa_column=Column(String(10), ForeignKey("monhoc.MAMH"), primary_key=True))
    class Config:
        from_attributes = True
class GIAOVIEN(SQLModel, table=True):
    MAGV: str = Field(sa_column=Column(String(4), primary_key=True))
    HOTEN: str = Field(sa_column=Column(String(40)))
    HOCVI: str = Field(sa_column=Column(String(10)))
    HOCHAM: str = Field(sa_column=Column(String(10)))
    GIOITINH: str = Field(sa_column=Column(String(3)))
    NGSINH: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True)) 
    NGVL: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True))
    HESO: Optional[float] = Field(sa_column=Column(Numeric(4,2), nullable=True))
    MUCLUONG: Optional[float] = Field(sa_column=Column(Numeric, nullable=True))
    MAKHOA: str = Field(sa_column=Column(String(4), ForeignKey("khoa.MAKHOA"), nullable=True))  
    class Config:
        from_attributes = True

class LOP(SQLModel, table=True):
    MALOP: str = Field(sa_column=Column(String(3), primary_key=True))
    TENLOP: str = Field(sa_column=Column(String(40)))
    TRGLOP: str = Field(sa_column=Column(String(5)))
    SISO: int = Field(sa_column=Column(SmallInteger))
    MAGVCN: Optional[str] = Field(sa_column=Column(String(4), ForeignKey("giaovien.MAGV"), nullable=True)) 
    class Config:
        from_attributes = True

class HOCVIEN(SQLModel, table=True):
    MAHV: str = Field(sa_column=Column(String(5), primary_key=True))
    HO: str = Field(sa_column=Column(String(40)))
    TEN: str = Field(sa_column=Column(String(10)))
    NGSINH: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True)) 
    GIOITINH: str = Field(sa_column=Column(String(3)))
    NOISINH: str = Field(sa_column=Column(String(40)))
    MALOP: str = Field(sa_column=Column(String(3), ForeignKey("lop.MALOP")))
    class Config:
        from_attributes = True

class GIANGDAY(SQLModel, table=True):
    MALOP: str = Field(sa_column=Column(String(3), ForeignKey("lop.MALOP"), primary_key=True))
    MAMH: str = Field(sa_column=Column(String(10), ForeignKey("monhoc.MAMH"), primary_key=True))
    MAGV: str = Field(sa_column=Column(String(4), ForeignKey("giaovien.MAGV")))
    HOCKY: int = Field(sa_column=Column(SmallInteger))
    NAM: int = Field(sa_column=Column(SmallInteger))
    TUNGAY: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True)) 
    DENNGAY: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True))
    class Config:
        from_attributes = True

class KETQUATHI(SQLModel, table=True):
    MAHV: str = Field(sa_column=Column(String(5), ForeignKey("hocvien.MAHV"), primary_key=True))
    MAMH: str = Field(sa_column=Column(String(10), ForeignKey("monhoc.MAMH"), primary_key=True))
    LANTHI: int = Field(sa_column=Column(SmallInteger, primary_key=True, default=1)) 
    NGTHI: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True))  
    DIEM: Optional[float] = Field(sa_column=Column(Numeric(4,2), nullable=True))
    KQUA: Optional[str] = Field(sa_column=Column(String(10), nullable=True))
    class Config:
        from_attributes = True