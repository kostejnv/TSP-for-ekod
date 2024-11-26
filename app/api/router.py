import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.api.payloads import ComputeRoutePayload
from app.settings import Settings
from app.worker import celery_app, compute_route_task

router = APIRouter(
    prefix="/api",
)
settings = Settings() # type: ignore

logger = logging.getLogger(__name__)


@router.get("/task/result/{task_id}")
async def task_result(task_id: str) -> JSONResponse:
    try:
        logger.info("Getting the result of the task with id: %s", task_id)
        task = celery_app.AsyncResult(task_id)
        return JSONResponse(content={"status": task.status, "result": task.result})
    except Exception as e:
        msg = f"Failed to get the result of the task: {e!s}"
        logger.error(msg)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": msg})

@router.post("/compute_route")
def compute_route(payload: ComputeRoutePayload) -> JSONResponse:
    try:
        logger.info("Starting to compute the route")
        # compute the route
        task = compute_route_task.delay(payload.points_file, payload.nr_cars)
        return JSONResponse(content={"task_id": task.id})
    except Exception as e:
        msg = f"Failed to compute the route: {e!s}"
        logger.error(msg)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": msg})
