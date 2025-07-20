from pydantic import BaseModel


class ProcessDataRequest(BaseModel):
    """
    Request model for processing data.
    """

    file_name: str
    delimiter: str = ";"
