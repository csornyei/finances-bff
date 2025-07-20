import httpx
from fastapi import APIRouter, HTTPException, Depends

from finances_bff.utils import get_tag_service_client
from finances_bff.schemas import tag as tag_schemas

router = APIRouter()


@router.get("/tags/health", tags=["health"])
async def health_check(
    tag_service_client: httpx.AsyncClient = Depends(get_tag_service_client),
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


@router.get("/tags/", response_model=list[tag_schemas.TagOut])
async def read_tags(
    tag_service_client: httpx.AsyncClient = Depends(get_tag_service_client),
):
    """
    Get all tags.
    """
    try:
        response = await tag_service_client.get("/api/v1/tags/")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Tag service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/tags/{tag_id_or_name}", response_model=tag_schemas.TagOut)
async def read_tag(
    tag_id_or_name: str,
    tag_service_client: httpx.AsyncClient = Depends(get_tag_service_client),
):
    """
    Get a tag by ID or name.
    """
    try:
        response = await tag_service_client.get(f"/api/v1/tags/{tag_id_or_name}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Tag service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/tags/", response_model=tag_schemas.TagOut)
async def create_tag(
    tag: tag_schemas.TagCreate,
    tag_service_client: httpx.AsyncClient = Depends(get_tag_service_client),
):
    """
    Create a new tag.
    """
    try:
        print(f"Creating tag: {tag}")
        tag_json = tag.model_dump(exclude_unset=True)
        response = await tag_service_client.post("/api/v1/tags/", json=tag_json)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Tag service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.put("/tags/{tag_id}", response_model=tag_schemas.TagOut)
async def update_tag(
    tag_id: str,
    tag: tag_schemas.TagUpdate,
    tag_service_client: httpx.AsyncClient = Depends(get_tag_service_client),
):
    """
    Update an existing tag by ID.
    """
    try:
        tag_json = tag.model_dump(exclude_unset=True)
        response = await tag_service_client.put(f"/api/v1/tags/{tag_id}", json=tag_json)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Tag service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.delete("/tags/{tag_id}")
async def delete_tag(
    tag_id: str,
    tag_service_client: httpx.AsyncClient = Depends(get_tag_service_client),
):
    """
    Delete a tag by ID.
    """
    try:
        response = await tag_service_client.delete(f"/api/v1/tags/{tag_id}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Tag service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
