from fastapi import FastAPI

from Routes import user
# from connections import engine, Base

app = FastAPI()

# Base.metadata.create_all(bind=engine) ==> No need to use as already table is exist.

@app.get('/health')
def health_check():
    return {'message':'Healthy'}


app.include_router(user.router)


