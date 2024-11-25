import tempfile
import shutil
from enums import DataTypes
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from reader_validator import ReaderValidator
import boto3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = boto3.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    aws_session_token="",
    region_name="us-east-1"
)

class InputModel(BaseModel):
    data_type: int = Field(..., description="An integer representing the data type")
    s3_bucket_uri: str = Field(..., description="The URI of the S3 bucket")

@app.post("/process-data/")
async def process_data(input_data: InputModel):
    if not input_data.s3_bucket_uri.startswith("s3://"):
        raise HTTPException(status_code=400, detail="Invalid S3 bucket URI")
    path = (
        input_data.s3_bucket_uri.split('/')[-1] if input_data.s3_bucket_uri[-1] != '/' else input_data.s3_bucket_uri.split('/')[-2]
    )
    temp_dir = tempfile.mkdtemp(suffix=path)
    try:
        rv = ReaderValidator(
            DataTypes(input_data.data_type),
            input_data.s3_bucket_uri,
            temp_dir,
            session
        )
    except Exception as err:
        shutil.rmtree(temp_dir)
        raise HTTPException(status_code=400, detail=str(err))

    result = rv.validate()
    shutil.rmtree(temp_dir)

    return result
