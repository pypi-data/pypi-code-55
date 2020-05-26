from fastapi.routing import APIRouter
from circlepacker.domain.contracts import Health
import circlepacker


router = APIRouter()


@router.get("/")
async def get_health():
    version = circlepacker.__version__
    current_health = Health()
    current_health.status = "Healthy"
    current_health.version = version
    return current_health
