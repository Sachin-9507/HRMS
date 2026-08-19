from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.schemas.designation import (
    DesignationCreateRequest,
    DesignationUpdateRequest
)

from app.repositories.designation_repository import (
    get_designations as repository_get_designations,
)

from app.services.designation_service import (
    create_designation as create_designation_service,
    get_designations as get_designations_service,
    get_designation as get_designation_service,
    update_designation as update_designation_service,
    deactivate_designation
)

from app.auth.rbac import (
    require_permission
)


router = APIRouter(
    prefix="/designations",
    tags=["Designations"]
)


@router.post("")
def create_designation(
    name: str,
    code: str,
    department_id: int,
    description: str | None = None
):
    return create_designation_service(
        name=name,
        code=code,
        description=description,
        department_id=department_id
    )


@router.get(
    "",
    dependencies=[
        Depends(
            require_permission(
                "designation.read"
            )
        )
    ]
)
def get_designations(
    department_id: int | None = None,
    include_inactive: bool = False
):
    return repository_get_designations(
        department_id = department_id,
        include_inactive = include_inactive
    )

    designations = get_designations(
        department_id = department_id,
        include_inactive = include_inactive
    )

    return {
        "designations": designations
    }


@router.get(
    "/{designation_id}",
    dependencies=[
        Depends(
            require_permission(
                "designation.read"
            )
        )
    ]
)
def get_designation(
    designation_id: int
):

    try:

        designation = get_designation_service(
            designation_id
        )

        return {
            "designation": designation
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put(
    "/{designation_id}",
    dependencies=[
        Depends(
            require_permission(
                "designation.update"
            )
        )
    ]
)
def update_designation(
    designation_id: int,
    data: DesignationUpdateRequest
):

    try:

        designation = update_designation_service(
            designation_id,
            data
        )

        return {
            "message": "Designation updated successfully",
            "designation": designation
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.delete(
    "/{designation_id}",
    dependencies=[
        Depends(
            require_permission(
                "designation.delete"
            )
        )
    ]
)
def delete_designation(
    designation_id: int
):

    try:

        designation = deactivate_designation(
            designation_id
        )

        return {
            "message": "Designation deactivated successfully",
            "designation": designation
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )