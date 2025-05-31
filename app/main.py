from fastapi import FastAPI, UploadFile, File
from app.database import engine
from app.models import db_models
from app.api import auth, endpoints
import time
from sqlalchemy.exc import OperationalError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Marmara Speech Analytics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
app.mount("/media", StaticFiles(directory="uploaded_files"), name="serve_audio_file")

app.include_router(auth.router)
app.include_router(endpoints.router)