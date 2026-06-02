import io
import zipfile
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_project_service, get_current_user, get_architecture_service
from app.domain.architectures.services import ArchitectureService
from app.domain.projects.dtos import ProjectCreateModel
from app.domain.projects.services import ProjectService
from app.domain.users.models import UserProfile

router = APIRouter()

@router.post("/")
async def create_project(
    data: ProjectCreateModel,
    service: ProjectService = Depends(get_project_service),
    user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    user, token = user_auth
    try:
        project = service.save_project(data, user.id, token)
        return project
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def get_projects(
    service: ProjectService = Depends(get_project_service),
    user_auth: tuple[UserProfile, str] = Depends(get_current_user)
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
    user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    user, token = user_auth
    try:
        project = service.get_project_by_id(str(project_id), token)
        if not project or project.user_id != user.id:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

  # Asegúrate de importar esto

@router.get("/download/{project_id}")
async def download_project(
        project_id: UUID,
        service: ProjectService = Depends(get_project_service),
        architecture_service: ArchitectureService = Depends(get_architecture_service),
        user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    user, token = user_auth
    try:
        project = service.get_project_by_id(str(project_id), token)
        if not project or (project.user_id != user.id and not user.is_authorized):
            raise HTTPException(status_code=404, detail="Project not found")

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            readme_content = f'# {project.name}\n\n'
            readme_content += f'## Description\n{project.description}\n\n'

            if project.architecture is not None:
                architecture_id = project.architecture.get("architecture_id", None)
                architecture = architecture_service.get_architecture_by_id(architecture_id, token)
                if architecture:
                    readme_content += f'## Architecture\n'
                    readme_content += f'**Name:** {architecture.name}\n\n'
                    readme_content += f'**Description:** {architecture.description}\n\n'

                    nodes = project.architecture.get("nodes", [])
                    readme_content += "### Components\n"
                    readme_content += "| Component Name (Label) | Type / Role |\n"
                    readme_content += "| :--- | :--- |\n"

                    for node in nodes:
                        if node.get("type") == "user":
                            continue

                        label = node.get("data", {}).get("label", "Unknown")
                        node_type = node.get("type", "generic-component")
                        readme_content += f"| {label} | `{node_type}` |\n"

                        folder_name = "".join(c for c in label if c.isalnum() or c in (" ", "_", "-")).strip()
                        if folder_name:
                            folder_name_slug = folder_name.replace(" ", "_").lower()
                            suffix = node_type.split("-")[-1]
                            file_path = f"src/{folder_name_slug}/{folder_name_slug}_{suffix}.py"
                            file_content = f"# Componente autogenerado para {label}\n"
                            zip_file.writestr(file_path, file_content)

                    readme_content += "\n"

            zip_file.writestr("README.md", readme_content)

        zip_buffer.seek(0)
        zip_bytes = zip_buffer.getvalue()

        safe_project_name = "".join(c for c in project.name if c.isalnum() or c in ("_", "-")).strip()
        filename = f"{safe_project_name or 'project'}.zip"

        return StreamingResponse(
            content=zip_bytes,
            status_code=200,
            media_type="application/octet-stream",
            headers={
                "Content-Type": "application/zip",
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Cache-Control": "no-store",
                "Content-Length": str(len(zip_bytes))
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
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
    data: ProjectCreateModel,
    service: ProjectService = Depends(get_project_service),
    user_auth: tuple[UserProfile, str] = Depends(get_current_user)
):
    user, token = user_auth
    try:
        project = service.get_project_by_id(str(project_id), token)
        if not project or project.user_id != user.id:
            raise HTTPException(status_code=404, detail="Project not found")

        update_data = data.model_dump(exclude_unset=True)
        updated_project = project.model_copy(update=update_data)
        service.save_project(
            project_data=updated_project,
            user_id=user.id,
            token=token
        )

        return {"message": "Project updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
