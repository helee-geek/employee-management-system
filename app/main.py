from fastapi import FastAPI
from app.routes import auth_routes, department_routes, employee_routes, task_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Employee Management System")

app.include_router(auth_routes.router)
app.include_router(department_routes.router)
app.include_router(employee_routes.router)
app.include_router(task_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Employee Management System API running"}