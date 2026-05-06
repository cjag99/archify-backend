from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from app.api.dependencies import get_project_service, get_current_user
from app.domain.projects.dtos import ProjectCreateModel, ProjectUpdateModel
from app.domain.projects.services import ProjectService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.post("/")
async def create_project(
    data: ProjectCreateModel,
    service: ProjectService = Depends(get_project_service),
    current_user: UserProfile = Depends(get_current_user)
):
    try:
        project = service.create_project(data, current_user.id)
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def get_projects(
    service: ProjectService = Depends(get_project_service),
    current_user: UserProfile = Depends(get_current_user)
):
    try:
        projects = service.get_projects_by_user_id(str(current_user.id))
        if not projects:
            return []
        return projects
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{project_id}")
async def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
    current_user: UserProfile = Depends(get_current_user)
):
    try:
        project = service.get_project_by_id(str(project_id))
        if not project or project.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
    current_user: UserProfile = Depends(get_current_user)
):
    try:
        project = service.get_project_by_id(str(project_id))
        if not project or project.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Project not found")
        
        service.delete_project(str(project_id))
        return {"message": "Project deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{project_id}")
async def update_project(
    project_id: UUID,
    data: ProjectUpdateModel,
    service: ProjectService = Depends(get_project_service),
    current_user: UserProfile = Depends(get_current_user)
):
    try:
        project = service.get_project_by_id(str(project_id))
        if not project or project.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Project not found")
        
        service.update_project(project, data.model_dump(exclude_unset=True))
        return {"message": "Project updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

