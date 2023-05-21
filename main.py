#sqlalchemy modules
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#fastapi modules
from fastapi import FastAPI ,Depends,HTTPException,Response
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
#my modules
from models import User as Usermodel
from models import Conference as Conferencemodel
from models import engine
from schemas import Settings,User,Conference

app=FastAPI()
dbengine = engine
Session = sessionmaker(bind=dbengine)
session = Session()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return Response(content="Invalid input", status_code=400)


@AuthJWT.load_config
def get_config():
    return Settings()

@app.post('/users/', response_model=User)
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


@app.post('/login/', description="Login successful", status_code=200)
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


# @app.get('/refresh')
# def refresh_token(Authorize:AuthJWT=Depends()):
#     try:
#         Authorize.jwt_refresh_token_required()
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Invalid Token")

#     current_user=Authorize.get_jwt_subject()
#     access_token=Authorize.create_access_token(subject=current_user)
#     response_obj={"access_token":access_token}

#     return JSONResponse(content=response_obj, status_code=200)
    

@app.post('/conferences/')
def create_conference(conference:Conference,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    new_conference = Conferencemodel(  title =conference.title,
                        description =conference.description,
                        start_time =conference.start_time,
                        end_time =conference.end_time,
                        Capacity =conference.Capacity,
                        items =conference.items,)
    session.add(new_conference)
    session.commit()

    return Response(content="Conference created", status_code=201)


@app.get('/conferences/', description="Successful operation", status_code=200)
def  Get_all_conferences(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        return Response(content="Unauthorized", status_code=401)
    
    conferences = session.query(Conferencemodel).all()
    serialized_objects=[]
    for conference in conferences: 
        data=Conference(
                id=conference.id,
                title =conference.title,
                description =conference.description,
                start_time =conference.start_time,
                end_time =conference.end_time,
                Capacity =conference.Capacity,
                items =conference.items,
         )
        serialized_objects.append(Conference.serialize(data))

    return serialized_objects
 

@app.put('/conferences/{conference_id}')
def   Update_an_existing_conference(conference:Conference,conference_id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    query = session.query(Conferencemodel).filter(Conferencemodel.id==conference_id)
    result = query.first()
    if (result):
        result.title =conference.title
        result.description =conference.description
        result.start_time =conference.start_time
        result.end_time =conference.end_time
        result.Capacity =conference.Capacity
        result.items =conference.items

        session.add(result)
        session.commit()
        return Response(content="Conference updated", status_code=200)
    else:
        return Response(content="Conference not found", status_code=404)


@app.delete('/conferences/{conference_id}',status_code=204)
def delete_an_existing_conference(conference_id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    query = session.query(Conferencemodel).filter(Conferencemodel.id==conference_id)
    result = query.first()
    if (result):
        session.delete(result)
        session.commit()
        return Response(content="Conference deleted", status_code=204)
        #background_tasks.add_task(send_notification, include_content())
    else:
        return Response(content="Conference not found", status_code=404)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



