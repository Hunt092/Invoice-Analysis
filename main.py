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

@app.get('/upload')
def upload_page(request:Request):
    return templates.TemplateResponse("Upload.html", {"request": request})

@app.post("/upload")
async def upload_files(files= File(...)):
    # Iterate over the uploaded files
    S3_CLIENT=boto3.client('s3')
    for file in files:
        # Upload the file to S3
        s3_object_key = file.filename
        S3_CLIENT.upload_fileobj(file.file, app.config("AWS_S3_BUCKET"), s3_object_key)

        # Call Textract OCR on the file
        textract_client = boto3.client("textract", region_name=app.config('AWS_REGION'))
        textract_response = textract_client.detect_document_text(
            Document={"S3Object": {"Bucket": app.config("AWS_S3_BUCKET"), "Name": s3_object_key}}
        )

        # Extract data from Textract response
        extracted_data = extract_data_from_textract(textract_response)

        # Store extracted data in PostgreSQL database
        conn = get_db_conn()
        cur = conn.cursor()
        query = """
            INSERT INTO your_table_name (field1, field2, ...)
            VALUES (%s, %s, ...)
        """
        cur.execute(query, (extracted_data["field1"], extracted_data["field2"], ...))
        conn.commit()
        cur.close()
        conn.close()

    return {"message": "Files uploaded successfully"}

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

def extract_data_from_textract(textract_response):
    # Parse Textract response to get relevant data
    # ...

    # Return a dictionary with the extracted data
    extracted_data = {"field1": "value1", "field2": "value2"}
    return extracted_data