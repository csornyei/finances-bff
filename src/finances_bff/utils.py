import httpx
from fastapi import Request


async def get_tag_service_client(request: Request) -> httpx.AsyncClient:
    """
    Get the tag service client from the request's app state.
    """
    if not hasattr(request.app.state, "tag_service_client"):
        raise ValueError("Tag service client is not initialized")
    return request.app.state.tag_service_client


async def get_statement_service_client(request: Request) -> httpx.AsyncClient:
    """
    Get the statement service client from the request's app state.
    """
    if not hasattr(request.app.state, "statement_service_client"):
        raise ValueError("Statement service client is not initialized")
    return request.app.state.statement_service_client


async def get_account_service_client(request: Request) -> httpx.AsyncClient:
    """
    Get the account service client from the request's app state.
    """
    if not hasattr(request.app.state, "account_service_client"):
        raise ValueError("Account service client is not initialized")
    return request.app.state.account_service_client


async def get_file_service_client(request: Request) -> httpx.AsyncClient:
    """
    Get the file service client from the request's app state.
    """
    if not hasattr(request.app.state, "file_service_client"):
        raise ValueError("File service client is not initialized")
    return request.app.state.file_service_client
