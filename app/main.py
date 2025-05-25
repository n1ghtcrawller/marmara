from fastapi import FastAPI, UploadFile, File
from app.api.endpoints import router
from app.database import engine
from app.models import db_models
from app.api import auth, endpoints
import time
from sqlalchemy.exc import OperationalError


app = FastAPI(title="Marmara Speech Analytics")

# FIXME:
def wait_for_db(aengine, timeout=60, interval=2):
    start = time.time()
    while True:
        try:
            with aengine.connect() as conn:
                print("Database is ready!")
                return
        except OperationalError:
            if time.time() - start > timeout:
                raise TimeoutError("Timed out waiting for the database to be ready.")
            print("Waiting for database to be ready...")
            time.sleep(interval)

wait_for_db(engine)
db_models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(endpoints.router)