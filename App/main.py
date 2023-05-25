
#fastapi modules
from fastapi import FastAPI ,Response
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import RequestValidationError

#my modules
from routers.auth import auth_router
from routers.api import api_router


app=FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(api_router, prefix="/api")

# To customize validation error response
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return Response(content="Invalid input", status_code=400)

#UVICORN configuration
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



