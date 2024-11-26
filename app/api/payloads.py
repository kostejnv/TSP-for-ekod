
from pydantic import BaseModel


class TestPayload(BaseModel):
    """Test payload for testing the API."""
    authorize_token: str

class ComputeRoutePayload(BaseModel):
    points_file: str
    nr_cars: int
