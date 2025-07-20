import httpx
from fastapi import APIRouter, HTTPException, Depends

from finances_bff.utils import get_statement_service_client
from finances_bff.schemas import statement as statement_schemas

router = APIRouter()


@router.get("/statements/health", tags=["health"])
async def health_check(
    statement_service_client: httpx.AsyncClient = Depends(get_statement_service_client),
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


@router.post("/statements/", response_model=statement_schemas.StatementOut)
async def create_statement(
    statement: statement_schemas.StatementCreate,
    statement_service_client: httpx.AsyncClient = Depends(get_statement_service_client),
):
    """
    Create a new statement.
    """
    try:
        response = await statement_service_client.post(
            "/api/v1/statements/",
            json=statement.model_dump(mode="json", exclude_unset=True),
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Statement service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/statements/", response_model=list[statement_schemas.StatementExtended])
async def list_statements(
    params: statement_schemas.StatementFilters = Depends(),
    statement_service_client: httpx.AsyncClient = Depends(get_statement_service_client),
):
    """
    Get all statements with optional filters.
    """
    try:
        params_dict = params.model_dump(exclude_unset=True)

        params_dict = {k: v for k, v in params_dict.items() if v is not None}

        response = await statement_service_client.get(
            "/api/v1/statements/", params=params_dict
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Statement service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get(
    "/statements/{statement_id}", response_model=statement_schemas.StatementExtended
)
async def get_one_statement(
    statement_id: str,
    statement_service_client: httpx.AsyncClient = Depends(get_statement_service_client),
):
    """
    Get a statement by ID.
    """
    try:
        response = await statement_service_client.get(
            f"/api/v1/statements/{statement_id}"
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Statement service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.put("/statements/{statement_id}", response_model=statement_schemas.StatementOut)
async def update_statement(
    statement_id: str,
    statement: statement_schemas.StatementUpdate,
    statement_service_client: httpx.AsyncClient = Depends(get_statement_service_client),
):
    """
    Update an existing statement by ID.
    """
    try:
        response = await statement_service_client.put(
            f"/api/v1/statements/{statement_id}",
            json=statement.model_dump(mode="json", exclude_unset=True),
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Statement service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.delete("/statements/{statement_id}")
async def delete_statement(
    statement_id: str,
    statement_service_client: httpx.AsyncClient = Depends(get_statement_service_client),
):
    """
    Delete a statement by ID.
    """
    try:
        response = await statement_service_client.delete(
            f"/api/v1/statements/{statement_id}"
        )
        response.raise_for_status()
        return {"ok": True}
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Statement service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
