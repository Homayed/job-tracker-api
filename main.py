from fastapi import FastAPI
from database import Base, engine
from routers import auth_routes, users, companies,applications,interviews,notes

app = FastAPI()
app.include_router(auth_routes.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(interviews.router)
app.include_router(notes.router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Job Tracker API is running"
    }









