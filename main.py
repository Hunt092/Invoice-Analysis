from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import boto3
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.config = {
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16 MB
    'UPLOAD_EXTENSIONS': ['.pdf', '.jpeg', '.jpg', '.png'],
    'UPLOAD_PATH': 'uploads/',
    'AWS_ACCESS_KEY_ID': 'your_access_key',
    'AWS_SECRET_ACCESS_KEY': 'your_secret_key',
    'AWS_REGION': os.getenv('AWS_REGION'),
    'AWS_S3_BUCKET': os.getenv('AWS_S3_BUCKET'),
    'DB_HOST': 'your_db_host',
    'DB_NAME': 'your_db_name',
    'DB_USER': 'your_db_user',
    'DB_PASSWORD': 'your_db_password'
}

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def upload_file(file: UploadFile):
    # Upload the file to S3
    s3 = boto3.client('s3')
    s3.upload_fileobj(file.file, 'my-bucket', file.filename)
    textract = boto3.client('textract')

    # Call the Textract OCR on the file
    response = textract.process(file.file)
    text = response.decode('utf-8')

    # Extract the necessary data and store it in the database
    # ...

    # Redirect to the homepage
    return {"message": "File uploaded successfully"}

@app.get("/analysis")
def analysis():
    # Get analysis over the data stored in the database
    # ...

    return {"analysis": analysis_results}

# Database Connection
def get_db_conn():
    conn = psycopg2.connect(
        host=app.config['DB_HOST'],
        database=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD']
    )
    return conn