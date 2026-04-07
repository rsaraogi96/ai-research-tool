from fastapi import APIRouter

from backend.api.instances import router as instances_router
from backend.api.search import router as search_router
from backend.api.analytics import router as analytics_router
from backend.api.people import router as people_router
from backend.api.companies import router as companies_router
from backend.api.tags import router as tags_router
from backend.api.collectors import router as collectors_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(instances_router)
api_router.include_router(search_router)
api_router.include_router(analytics_router)
api_router.include_router(people_router)
api_router.include_router(companies_router)
api_router.include_router(tags_router)
api_router.include_router(collectors_router)
