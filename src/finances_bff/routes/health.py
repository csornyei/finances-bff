import httpx
from fastapi import APIRouter, HTTPException, Depends

import finances_bff.utils as utils

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check(
    account_service_client: httpx.AsyncClient = Depends(
        utils.get_account_service_client
    ),
    file_service_client: httpx.AsyncClient = Depends(utils.get_file_service_client),
    statement_service_client: httpx.AsyncClient = Depends(
        utils.get_statement_service_client
    ),
    tag_service_client: httpx.AsyncClient = Depends(utils.get_tag_service_client),
):
    """
    Health check endpoint for the BFF.
    """
    try:
        account_response = await account_service_client.get("/health")
        file_response = await file_service_client.get("/health")
        statement_response = await statement_service_client.get("/health")
        tag_response = await tag_service_client.get("/health")
        account_response.raise_for_status()
        file_response.raise_for_status()
        statement_response.raise_for_status()
        tag_response.raise_for_status()

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Service is unavailable: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    return {
        "status": "ok",
        "services": {
            "account_service": account_response.json(),
            "file_service": file_response.json(),
            "statement_service": statement_response.json(),
            "tag_service": tag_response.json(),
        },
    }


@router.get("/account/health", tags=["health"])
async def account_health_check(
    account_service_client: httpx.AsyncClient = Depends(
        utils.get_account_service_client
    ),
):
    """
    Health check endpoint.
    """
    try:
        response = await account_service_client.get("/health")
        response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Account service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    return {"status": "ok", "account_service": response.json()}


@router.get("/file/health", tags=["health"])
async def file_health_check(
    file_service_client: httpx.AsyncClient = Depends(utils.get_file_service_client),
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


@router.get("/statements/health", tags=["health"])
async def statements_health_check(
    statement_service_client: httpx.AsyncClient = Depends(
        utils.get_statement_service_client
    ),
):
    """
    Health check endpoint.
    """
    try:
        response = await statement_service_client.get("/health")
        response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Statement service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    return {"status": "ok", "statement_service": response.json()}


@router.get("/tags/health", tags=["health"])
async def tags_health_check(
    tag_service_client: httpx.AsyncClient = Depends(utils.get_tag_service_client),
):
    """
    Health check endpoint.
    """
    try:
        response = await tag_service_client.get("/health")
        response.raise_for_status()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Tag service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    return {"status": "ok", "tag_service": response.json()}
