import asyncio
import logging

from celery import Celery

from app.settings import Settings

settings = Settings() # type: ignore

# Initialize the Celery app
celery_app = Celery(__name__,
    broker=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
)
celery_app.conf.update(enable_utc=True, timezone="Europe/Prague")
celery_app.conf.update( # tasks can accept all python types arguments
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=["pickle"],
)

logger = logging.getLogger(__name__)

@celery_app.task(name="compute_route")
def compute_route_task(file_content: str, nr_cars: int) -> str:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(compute_route(file_content, nr_cars))
    loop.close()
    return result

async def compute_route(file_content: str, nr_cars: int) -> str: # noqa
    """Async function for computing the route"""
    logger.info("Starting to compute the route")
    await asyncio.sleep(2)
    logger.info("Finished computing the route")
    return """
        <div>
            <h3>Trasa byla úspěšně vytvořena</h3>
            <p>Odkazy na navigaci naleznete zde:</p>
            <ul style="list-style-type: none; padding: 0;">
                <li style="margin-bottom: 10px;">
                    <strong>(1/5)</strong>
                    <a href="https://mapy.cz/fnc/v1/route?start=14.721057172205304,50.631829779131046&end=14.558713,50.761887&waypoints=14.575324,50.71658;14.543725,50.771604;14.54303,50.777262;14.547429,50.768575;14.549955,50.766204;14.550304,50.76403;14.553751,50.761613;14.553721,50.763457;14.555701,50.765579&routeType=car_fast"
                    target="_blank"
                    style="text-decoration: none; color: #0073e6;">
                    Odkaz na trasu do Mapy.cz
                    </a>
                </li>
                <li style="margin-bottom: 10px;">
                    <strong>(2/5)</strong>
                    <a href="https://mapy.cz/fnc/v1/route?start=14.558713,50.761887&end=14.721057172205304,50.631829779131046&waypoints=14.55603,50.757245;14.556733,50.758154;14.560845,50.755749;14.55908,50.75594;14.560909,50.754522&routeType=car_fast"
                    target="_blank"
                    style="text-decoration: none; color: #0073e6;">
                    Odkaz na trasu do Mapy.cz
                    </a>
                </li>
            </ul>
        </div>
    """
