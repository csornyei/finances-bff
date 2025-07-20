import httpx
from fastapi import APIRouter, HTTPException, Depends

from finances_bff.utils import get_account_service_client
from finances_bff.schemas import account as account_schemas

router = APIRouter()


@router.get("/accounts/", response_model=list[account_schemas.AccountOut])
async def read_accounts(
    params: account_schemas.AccountsFilter = Depends(),
    account_service_client: httpx.AsyncClient = Depends(get_account_service_client),
):
    """
    Get all accounts.
    """
    try:
        params_dict = params.model_dump(exclude_unset=True)

        params_dict = {k: v for k, v in params_dict.items() if v is not None}

        response = await account_service_client.get(
            "/api/v1/accounts/", params=params_dict
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Account service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/accounts/", response_model=account_schemas.AccountOut)
async def create_account(
    account: account_schemas.AccountCreate,
    account_service_client: httpx.AsyncClient = Depends(get_account_service_client),
):
    """
    Create a new account.
    """
    try:
        response = await account_service_client.post(
            "/api/v1/accounts/",
            json=account.model_dump(mode="json", exclude_unset=True),
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Account service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/accounts/{account_id}", response_model=account_schemas.AccountWithAliases)
async def read_account(
    account_id: str,
    account_service_client: httpx.AsyncClient = Depends(get_account_service_client),
):
    """
    Get a specific account by ID.
    """
    try:
        response = await account_service_client.get(f"/api/v1/accounts/{account_id}")
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Account service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.post("/accounts/alias")
async def create_alias(
    body: account_schemas.AccountAlias,
    account_service_client: httpx.AsyncClient = Depends(get_account_service_client),
):
    """
    Add an alias to the account.
    """
    try:
        response = await account_service_client.post(
            "/api/v1/accounts/alias",
            json=body.model_dump(mode="json", exclude_unset=True),
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Account service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.put("/accounts/{account_id}", response_model=account_schemas.AccountOut)
async def update_account(
    account: account_schemas.AccountUpdate,
    account_id: str,
    account_service_client: httpx.AsyncClient = Depends(get_account_service_client),
):
    """
    Update a specific account by ID.
    """
    try:
        response = await account_service_client.put(
            f"/api/v1/accounts/{account_id}",
            json=account.model_dump(mode="json", exclude_unset=True),
        )
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Account service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.delete("/accounts/{account_id}")
async def delete_account(
    account_id: str,
    account_service_client: httpx.AsyncClient = Depends(get_account_service_client),
):
    """
    Delete a specific account by ID.
    """
    try:
        response = await account_service_client.delete(f"/api/v1/accounts/{account_id}")
        response.raise_for_status()
        return {"message": "Account deleted successfully"}
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Account service is unavailable: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
