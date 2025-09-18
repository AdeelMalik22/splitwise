from fastapi import FastAPI
from app.api.users.routes import router as users_router
from app.api.groups.routes import router as groups_router
from app.api.expenses.routes import router as expenses_router
app = FastAPI()
app.include_router(users_router)
app.include_router(groups_router)
app.include_router(expenses_router)
