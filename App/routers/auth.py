from fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter
from schemas import Settings
from schemas import User
from fastapi import Depends



auth_router = APIRouter()



@AuthJWT.load_config
def get_config():
    return Settings()

@auth_router.post('/users/', response_model=User)
def create_user(user:User):
    query = session.query(Usermodel).filter(Usermodel.username==user.username)
    result = query.first()

    if not result:
        user = Usermodel(username=user.username, password=user.password)
        session.add(user)
        session.commit()
    else:
        return Response(content="Invalid input", status_code=400)

    return Response(content="User registered", status_code=201)


@auth_router.post('/login/', description="Login successful", status_code=200)
def login(user:User,Authorize:AuthJWT=Depends()):
    query = session.query(Usermodel).filter(Usermodel.username==user.username, Usermodel.password==user.password)
    result = query.first()
    if result:
        access_token = Authorize.create_access_token(subject=user.username)
        refresh_token = Authorize.create_refresh_token(subject=user.username)
        response_obj= {"access_token":access_token,"refresh_token":refresh_token} 

        return JSONResponse(content=response_obj, status_code=200)
    else:
        return Response(content="Invalid username or password", status_code=401)

@auth_router.get('/refresh')
def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Token")

    current_user=Authorize.get_jwt_subject()
    access_token=Authorize.create_access_token(subject=current_user)
    response_obj={"access_token":access_token}

    return JSONResponse(content=response_obj, status_code=200)
    