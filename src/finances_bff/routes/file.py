import httpx
from fastapi import APIRouter, HTTPException, Depends, UploadFile

from finances_bff.utils import get_file_service_client
from finances_bff.schemas import file as file_schemas

router = APIRouter()


@router.get("/file/health", tags=["health"])
async def health_check(
    file_service_client: httpx.AsyncClient = Depends(get_file_service_client),
):
    """
    Health check endpoint.
    """
    try:
        response = await file_service_client.get("/health")
        response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"File service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    return {"status": "ok", "file_service": response.json()}


@router.post("/upload/zip", tags=["file"])
async def upload_zip(
    zip_file: UploadFile,
    file_service_client: httpx.AsyncClient = Depends(get_file_service_client),
):
    """
    Endpoint to upload zip data.
    """
    if not zip_file or zip_file.content_type != "application/zip":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only zip files are allowed."
        )

    file_name = zip_file.filename

    if not file_name.endswith(".zip"):
        raise HTTPException(status_code=400, detail="File is not a zip file")

    file_content = await zip_file.read()

    try:
        response = await file_service_client.post(
            "/api/v1/upload/zip", files={"file": (file_name, file_content)}
        )
        response.raise_for_status()
        return {"message": "Zip file uploaded successfully"}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/upload/csv", tags=["file"])
async def upload_csv(
    csv_file: UploadFile,
    file_service_client: httpx.AsyncClient = Depends(get_file_service_client),
):
    """
    Endpoint to upload CSV data.
    """
    if not csv_file or csv_file.content_type != "text/csv":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only CSV files are allowed."
        )

    file_name = csv_file.filename

    if not file_name.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File is not a CSV file")

    file_content = await csv_file.read()

    try:
        response = await file_service_client.post(
            "/api/v1/upload/csv", files={"file": (file_name, file_content)}
        )
        response.raise_for_status()
        return {"message": "CSV file uploaded successfully"}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/process")
async def process_file(
    body: file_schemas.ProcessDataRequest,
    file_service_client: httpx.AsyncClient = Depends(get_file_service_client),
):
    """
    Endpoint to process a file by its ID.
    """
    try:
        response = await file_service_client.post(
            "/api/v1/process",
            json={
                "file_name": body.file_name,
                "delimiter": body.delimiter,
            },
        )
        response.raise_for_status()
        return {"message": "File processed successfully", "data": response.json()}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/files/raw")
async def get_csv_files(
    file_service_client: httpx.AsyncClient = Depends(get_file_service_client),
):
    """
    Endpoint to get all raw CSV files.
    """
    try:
        response = await file_service_client.get("/api/v1/files/raw")
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
