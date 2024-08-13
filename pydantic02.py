from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel


# 회원정보를 이용한 CRUD
# userid, passwd, name, email, regdate
class Member(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
    regdate: datetime

member_db: List[Member] = []

app = FastAPI()

@app.get('/')
def index ():
    return 'Hello,pydantic!! - Member'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('pydantic02:app', reload=True)
#회원 데이터 조회

@app.get('/member',response_model=list[Member])
def member():
    return member_db
# 회원 데이터 추가
@app.post('/manber',response_model=Member)
def manberok(m: Member):
    member_db.append(m)
    return m


# 회원데이터 상세 조회 - 아이디로 조회
@app.get('/member/{userid}',response_model=Member)
def manone(userid: str):
    memberone = Member(userid='none', passwd='none',name='none',email='none',
                       regdate='1970-010-01T00:00.000Z')
    for m in member_db:
        if m.userid == userid:
            memberone = m
    return memberone
# 회원데이터 삭제
@app.delete('/member/{userid}', response_model=Member)
def memberdel(userid: str):
    memberone = Member(userid='none', passwd='none',name='none',email='none',
                    regdate='1970-010-01T00:00.000Z')
    for idx,m in enumerate(member_db):
        if m.userid == userid:
            memberone = member_db.pop(idx)
    return memberone

# 회원 데이터 수정 -
@app.put('/member',response_model=Member)
def memberbod(one: Member):
    putone = Member(userid='none', passwd='none',name='none',email='none',
                    regdate='1970-010-01T00:00.000Z')
    for idx, m in enumerate(member_db):
        if m.userid == one.userid:
            member_db[idx] = one
            putone = one
    return putone


