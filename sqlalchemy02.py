from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Sequence, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# 회원정보를 이용한 SQL CRUD
# mno,userid, passwd, name, email, regdate
sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url,
            connect_args={}, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False,bind=engine)
# 데이터베이스 모델 정의
Base =declarative_base()

class Member(Base):
    __tablename__ = 'member'

    mno = Column(Integer, Sequence('seq_member'),
                 primary_key=True, index=True, )
    userid =Column(String, index=True)
    passwd=Column(String)
    name = Column(String)
    email = Column(String)
    regdate =Column(DateTime(timezone=True),
                     server_default=func.now())

Base.metadata.create_all(bind=engine)

# 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class NewMemberModel(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str


class MemberModel(NewMemberModel):
    mno: int
    regdate: datetime


app = FastAPI()

@app.get('/')
def indext():
    return 'Hello, sqlalchemy!!, again'

#회원 조회
@app.get('/member', response_model=List[MemberModel])
def read_member(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

#회원 추가
#@app.post('/member', response_model=NewMemberModel)
@app.post('/member', response_model=str)
def add_member(m: NewMemberModel, db: Session = Depends(get_db)):
    m = Member(**dict(m))
    db.add(m)
    db.commit()
    db.refresh(m)
    #return m
    return '데이터 입력 성공!!'

# 회원 상세 조회
@app.get('/member,/{mno}',response_model=Optional[MemberModel])
def readone_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    return member

# 회원 데이터 삭제 - 회원번호로 조회
@app.delete('/member,/{mno}', response_model=Optional[MemberModel])
def delete_member(mno : int, db: Session= Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    if member:
        db.delete(member)
        db.commit()
    return member

# 회원 데이터 수정 - 회원번호로 조회
# 먼저, 삭제할 회원 데이터가 있는지 확인한 후 수정 실행
@app.put('/member/{mno}', response_model=Optional[MemberModel])
def update_member(m: MemberModel, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == m.mno).first()
    if member:
        for key, val in m.dict().items():
            setattr(member, key, val)
        db.commit()
        db.refresh(member)
    return member

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy02:app', reload=True)