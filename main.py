from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os, pyodbc
from azure.storage.blob import BlobServiceClient

app = FastAPI(title="Zelvio API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQL_CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING")
BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING")

@app.get("/")
def home():
    return {"message": "Zelvio full backend is running ✅"}

@app.get("/test-sql")
def test_sql():
    try:
        conn = pyodbc.connect(SQL_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT GETDATE()")
        row = cursor.fetchone()
        return {"sql_connection": "ok", "server_time": str(row[0])}
    except Exception as e:
        return {"sql_connection": "failed", "error": str(e)}

@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        blob_service = BlobServiceClient.from_connection_string(BLOB_CONN_STRING)
        container_client = blob_service.get_container_client("uploads")
        try:
            container_client.create_container()
        except Exception:
            pass
        container_client.upload_blob(name=file.filename, data=file.file, overwrite=True)
        return {"filename": file.filename, "status": "uploaded"}
    except Exception as e:
        return {"error": str(e)}
