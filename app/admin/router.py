from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from db.session import get_session
from schemas.user import User
from schemas.config import Config  # 引入 Config 模型
from api.response_model import ResponseModel  # 引入 ResponseModel 以处理异常响应

admin_router = APIRouter()
templates = Jinja2Templates(directory="admin/templates")

@admin_router.get("/admin/")
async def index(request: Request, session: AsyncSession = Depends(get_session)):
    try:
        # 从数据库中读取管理员用户名
        statement = select(Config).where(Config.k == "admin_user")
        result = await session.execute(statement)
        config = result.scalar_one_or_none()

        if not config:
            return ResponseModel(code=1, msg="管理员用户未找到")

        admin_name = config.v  # 获取管理员用户名

    except Exception as e:
        # 处理可能出现的错误
        return {"code": 1, "msg": str(e), "data": None}

    # 渲染模板并传递管理员用户名
    return templates.TemplateResponse("index.html", {"request": request, "admin_name": admin_name})


@admin_router.get("/admin/console")
async def console(request: Request):
    return templates.TemplateResponse("console.html", {"request": request})

@admin_router.get("/admin/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 队伍
@admin_router.get("/admin/team")
async def team(request: Request):
    return templates.TemplateResponse("team.html", {"request": request})
@admin_router.get("/admin/team_form")
async def team_form(request: Request, session: AsyncSession = Depends(get_session)):
    # 使用 AsyncSession 进行异步查询
    try:
        statement = select(User)
        result = await session.execute(statement)  # 确保 await 用于异步调用
        users = result.scalars().all()  # 获取查询结果的所有数据
    except Exception as e:
        # 处理可能出现的错误
        return {"code": 1, "msg": str(e), "data": None}

    # 渲染模板并传递用户列表
    return templates.TemplateResponse("team_form.html", {"request": request, "users": users})
# 用户
@admin_router.get("/admin/user")
async def user(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})
@admin_router.get("/admin/user_form")
async def user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})

# 题目
@admin_router.get("/admin/problem")
async def problem(request: Request):
    return templates.TemplateResponse("problem.html", {"request": request})
@admin_router.get("/admin/problem_form")
async def problem_form(request: Request):
    return templates.TemplateResponse("problem_form.html", {"request": request})

# 比赛
@admin_router.get("/admin/competition")
async def competition(request: Request):
    return templates.TemplateResponse("competition.html", {"request": request})
@admin_router.get("/admin/competition_form")
async def competition_form(request: Request):
    return templates.TemplateResponse("competition_form.html", {"request": request})