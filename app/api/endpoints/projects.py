import token
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
    user_auth: tuple[str, UserProfile] = Depends(get_current_user)
):
    user, token = user_auth
    try:
        project = service.create_project(data, user.id, token)
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def get_projects(
    service: ProjectService = Depends(get_project_service),
    user_auth: tuple[str, UserProfile] = Depends(get_current_user)
):
    user, token = user_auth
    try:
        if user and user.is_authorized:
            projects = service.get_all_projects(token)
        else:
            projects = service.get_projects_by_user_id(str(user.id), token)
        if not projects:
            return "No projects to show"
        return projects
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{project_id}")
async def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
    user_auth: tuple[str, UserProfile] = Depends(get_current_user)
):
    user, token = user_auth
    try:
        project = service.get_project_by_id(str(project_id), token)
        if not project or project.user_id != user.id:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{project_id}")
async def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
    user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    user, token = user_auth
    
    try:
        project = service.get_project_by_id(str(project_id), token)
        if not project or (project.user_id != user.id and not user.is_authorized):
            raise HTTPException(status_code=404, detail="Project not found")
        
        service.delete_project(project_id, token)
        return {"message": "Project deleted successfully"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{project_id}")
async def update_project(
    project_id: UUID,
    data: ProjectUpdateModel,
    service: ProjectService = Depends(get_project_service),
    user_auth: tuple[str, UserProfile] = Depends(get_current_user)
):
    user, token = user_auth
    try:
        project = service.get_project_by_id(str(project_id), token)
        if not project or project.user_id != user.id:
            raise HTTPException(status_code=404, detail="Project not found")
        
        service.save_project(project, data.model_dump(exclude_unset=True), token)
        return {"message": "Project updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

