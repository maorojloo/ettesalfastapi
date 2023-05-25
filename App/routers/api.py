#sqlalchemy modules
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#fastApi
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import FastAPI ,Depends,HTTPException,Response
from fastapi_jwt_auth import AuthJWT
#my modules
from schemas import Settings
from schemas import User,Conference
from models import User as Usermodel
from models import Conference as Conferencemodel
from models import engine


api_router = APIRouter()

dbengine = engine
Session = sessionmaker(bind=dbengine)
session = Session()


@api_router.post('/conferences/')
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


@api_router.get('/conferences/', description="Successful operation", status_code=200)
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
 

@api_router.put('/conferences/{conference_id}')
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


@api_router.delete('/conferences/{conference_id}',status_code=204)
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
    else:
        return Response(content="Conference not found", status_code=404)
