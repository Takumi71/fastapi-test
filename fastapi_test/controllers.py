from fastapi import FastAPI, Depends, HTTPException, Security  # new

from fastapi.security import HTTPBasic, HTTPBasicCredentials  # new

from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED  # new

import db  # new
from models import User, Task  # new

import hashlib  # new


app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
    version='0.9 beta'
)
 
 # new テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用
security = HTTPBasic()

def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # Basic認証で受け取った情報
    username = credentials.username
    password = hashlib.md5(credentials.password.encode()).hexdigest()

    # データベースからユーザ名が一致するデータを取得
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all() if user is not None else []
    db.session.close()

    # 該当ユーザがいない場合
    if user is None or user.password != password:
        error = 'ユーザ名かパスワードが間違っています'
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Basic"},
        )

    # 特に問題がなければ管理者ページへ
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task})

def index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request
                                      })

# def admin(request: Request):
#     # ユーザとタスクを取得
#     # とりあえず今はadminユーザのみ取得
#     user = db.session.query(User).filter(User.username == 'admin').first()
#     task = db.session.query(Task).filter(Task.user_id == user.id).all()
#     db.session.close()
 
#     return templates.TemplateResponse('admin.html',
#                                       {'request': request,
#                                        'user': user,
#                                        'task': task})



