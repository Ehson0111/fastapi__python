from fastapi import FastAPI, HTTPException
# from database import *    # Если используется, раскомментируйте  uvicorn api:app --reload

from models import *
from response_models import *
from config import *
import uvicorn

app = FastAPI(
    title="Тут чета умное",
    description="Тут чета умное",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/users/select/{user_id}")
async def get_users(user_id: int):
    try:
        with DBSetting.get_session() as conn:
            user = conn.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/add", response_model=UserCreate)
async def add_get_users(user_name: str, user_role: str):
    user = UserCreate(name=user_name, role=user_role)
    with DBSetting.get_session() as conn:
        role_db = conn.query(Role).filter(Role.name == user.role).first()
        
        if role_db is None:
            raise HTTPException(status_code=404, detail="We haven't this role")
        else:
            new_user = User(name=user.name, role_id=role_db.id)
            conn.add(new_user)
            conn.commit()
            print("Успешно")
            return user
        
@app.put("/users/update/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, updated_data: UserUpdate):
    try:
        with DBSetting.get_session() as conn:
            user = conn.query(User).filter(User.id == user_id).first()
            
            if user is None: 
                raise HTTPException(status_code=404, detail="User not found")
                
            for key, value in updated_data.dict().items():
                setattr(user, key, value)
            
            conn.commit()
            return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/users/delete/{user_id}")
async def delete_user(user_id: int):
    try:
        with DBSetting.get_session() as conn:
            user = conn.query(User).filter(User.id == user_id).first()
            
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            
            conn.delete(user)
            conn.commit()
            return {"message": f"User with ID {user_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)