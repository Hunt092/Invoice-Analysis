from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import boto3
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import psycopg2
import os
from dbfunctions.create_tables import createTables
from dbfunctions.extract import parser as textractpraser
from dbfunctions.store import store
load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
AWS_REGION= os.getenv('AWS_REGION')
AWS_S3_BUCKET= os.getenv('AWS_S3_BUCKET')

# DB_HOST= os.getenv('AWS_REGION')
DB_NAME= os.getenv('DB_NAME')
DB_USER= os.getenv('DB_USER')
DB_PASSWORD= os.getenv('DB_PASSWORD')

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
async def upload_files(files: list[UploadFile] = File(...)):
    # Iterate over the uploaded files
    S3_CLIENT=boto3.client('s3')
    for file in files:
        # Upload the file to S3
        s3_object_key = file.filename
        S3_CLIENT.upload_fileobj(file.file, AWS_S3_BUCKET, s3_object_key)

        # Call Textract OCR on the file
        textract_client = boto3.client("textract", region_name=AWS_REGION)
        textract_response = textract_client.analyze_expense(
            Document={"S3Object": {"Bucket": AWS_S3_BUCKET, "Name": s3_object_key}}
        )

        # Extract data from Textract response
        extracted_data = textractpraser(textract_response)
        # Store extracted data in PostgreSQL database
        conn = get_db_conn()
        # createTables(conn)
        store(extracted_data,conn)
        conn.close()

    return RedirectResponse(url='/', status_code=303)

@app.get("/analysis")
def analysis():
    # Get analysis over the data stored in the database
    # ...

    return {"analysis": analysis_results}

# Database Connection
def get_db_conn():

    conn = psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn



@app.get("/vendor_total")
def get_vendor_total():
    conn = get_db_conn()
    cur = conn.cursor()

    query = """
    SELECT
      v.name AS vendor_name,
      SUM(total) AS total_amount
    FROM
      public.invoice_details i
      INNER JOIN public.vendor_details v ON i.vendor_id = v.vendor_id
    GROUP BY
      v.name
    ORDER BY
      total_amount DESC;
    """

    cur.execute(query)
    result = cur.fetchall()

    # Convert the result into a list of dictionaries
    vendor_totals = {
            "vendor_name": [],
            "total_amount": []
        }
    for row in result:
        vendor_totals["vendor_name"].append( row[0])
        vendor_totals["total_amount"].append( row[1])

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Return the result as a list of dictionaries
    return vendor_totals

@app.get("/month_wise_total")
def get_month_wise_total():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                EXTRACT(MONTH FROM to_date(order_date, 'DD/MM/YYYY')) AS month,
                SUM(total) AS total_amount
            FROM
                public.invoice_details
            GROUP BY
                EXTRACT(MONTH FROM to_date(order_date, 'DD/MM/YYYY'))
            ORDER BY
                month;
        """)
        results = []
        for row in cur.fetchall():
            results.append(row[1])
        return {"data": results}
    except Exception as e:
        print(e)
        return {"error": "An error occurred while fetching data"}
    

@app.get("/total/yearly")
async def yearly_total(year: int=2021) -> dict:
    conn= get_db_conn()
    cursor = conn.cursor()
    query = f"""
    SELECT
        SUM(total) AS total_amount
    FROM
        public.invoice_details
    WHERE
        EXTRACT(YEAR FROM to_date(order_date, 'DD/MM/YYYY')) = {year};
    """
    cursor.execute(query)
    total = cursor.fetchone()[0]
    if total==None:
        total= 0
    cursor.close()
    return {"total": total}

@app.get("/total/monthly")
async def monthly_total(month: int =6, year: int =2022) -> dict:
    conn= get_db_conn()
    cursor = conn.cursor()
    query = f"""
    SELECT
        SUM(total) AS total_amount
    FROM
        public.invoice_details
    WHERE
        EXTRACT(MONTH FROM to_date(order_date, 'DD/MM/YYYY')) = {month}
        AND EXTRACT(YEAR FROM to_date(order_date, 'DD/MM/YYYY')) = {year};
    """
    cursor.execute(query)
    total = cursor.fetchone()[0]
    cursor.close()
    if total == None:
        total=0
    return {"total": total}



@app.get("/invoices/count")
def get_invoice_count():
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM public.invoice_details")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {"count": count}
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL", error)


@app.get("/highest_product_prices")
def get_product_prices():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
  EXTRACT(MONTH FROM to_date(order_date, 'DD/MM/YYYY')) AS month,
  COALESCE(MAX(total), 0) AS highest_total
FROM
  public.invoice_details
GROUP BY
  EXTRACT(MONTH FROM to_date(order_date, 'DD/MM/YYYY'))
ORDER BY
  month;

    """)
    rows = cur.fetchall()
    cur.close()
    return {"data": rows}





