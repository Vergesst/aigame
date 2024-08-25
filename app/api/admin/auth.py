from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.response_model import ResponseModel
from app.core.security import create_access_token, verify_password, get_current_admin
from app.core.utils import load_config_from_db
from app.db.session import get_session

auth_router = APIRouter()

@auth_router.post("/login", response_model=ResponseModel, tags=["Admin"])
async def login(username: str, password: str, session: AsyncSession = Depends(get_session)):
    try:
        config_dict = await load_config_from_db(session)

        admin_user = config_dict.get("admin_user")
        admin_pwd = config_dict.get("admin_pwd")

        if not admin_user or not admin_pwd:
            return ResponseModel(code=1, msg="管理员用户或密码未设置")

        if username != admin_user or not verify_password(password, admin_pwd):
            return ResponseModel(code=1, msg="用户名或密码错误")

        access_token = create_access_token(data={"sub": username})
        return ResponseModel(code=0, msg="登录成功", data={"access_token": access_token, "token_type": "bearer"})
    except Exception as e:
        return ResponseModel(code=1, msg=str(e))