from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status

from app.repositories import leave_repository


def calculate_total_days(
    start_date: date,
    end_date: date
) -> Decimal:

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be after end date"
        )

    days = (end_date - start_date).days + 1

    return Decimal(days)


def apply_leave(
    employee_id: int,
    leave_type_id: int,
    start_date: date,
    end_date: date,
    reason: str
):
    leave_type = leave_repository.get_leave_type(
        leave_type_id
    )

    if not leave_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave type not found"
        )

    if not leave_type[5]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Leave type is inactive"
        )

    total_days = calculate_total_days(
        start_date,
        end_date
    )

    overlapping = leave_repository.has_overlapping_leave(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date
    )

    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Leave request overlaps with an existing pending or approved leave"
        )

    leave_id = leave_repository.create_leave_request(
        employee_id=employee_id,
        leave_type_id=leave_type_id,
        start_date=start_date,
        end_date=end_date,
        total_days=total_days,
        reason=reason
    )

    return leave_id


def get_my_leave(
    employee_id: int,
    leave_id: int
):
    leave = leave_repository.get_leave_request(
        leave_id,
        employee_id
    )

    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )

    return leave


def get_my_leaves(
    employee_id: int,
    status_filter: str | None = None
):
    allowed_statuses = {
        "PENDING",
        "APPROVED",
        "REJECTED",
        "CANCELLED"
    }

    if status_filter and status_filter.upper() not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid leave status"
        )

    return leave_repository.list_my_leave_requests(
        employee_id=employee_id,
        status=status_filter.upper()
        if status_filter
        else None
    )


def cancel_leave(
    employee_id: int,
    leave_id: int
):
    cancelled = leave_repository.cancel_leave_request(
        leave_id=leave_id,
        employee_id=employee_id
    )

    if not cancelled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Leave cannot be cancelled. "
                "It may not exist or may no longer be pending."
            )
        )

    return True


def get_my_balances(
    employee_id: int,
    leave_year: int
):
    return leave_repository.list_leave_balances(
        employee_id=employee_id,
        leave_year=leave_year
    )

def get_all_leaves(
    status_filter: str | None = None,
    employee_id: int | None = None,
    leave_type_id: int | None = None
):
    allowed_statuses = {
        "PENDING",
        "APPROVED",
        "REJECTED",
        "CANCELLED"
    }

    if (
        status_filter
        and status_filter.upper()
        not in allowed_statuses
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid leave status"
        )

    return leave_repository.list_all_leave_requests(
        status_filter=(
            status_filter.upper()
            if status_filter
            else None
        ),
        employee_id=employee_id,
        leave_type_id=leave_type_id
    )

def get_admin_leave(
    leave_id: int
):
    leave = leave_repository.get_admin_leave_request(
        leave_id
    )

    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )

    return leave

def approve_leave(
    leave_id: int,
    reviewer_id: int
):
    try:

        leave_repository.approve_leave_request(
            leave_id=leave_id,
            reviewer_id=reviewer_id
        )

    except ValueError as exc:

        message = str(exc)

        if message == "Leave request not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    return get_admin_leave(leave_id)

def reject_leave(
    leave_id: int,
    reviewer_id: int,
    admin_remarks: str
):
    try:

        leave_repository.reject_leave_request(
            leave_id=leave_id,
            reviewer_id=reviewer_id,
            admin_remarks=admin_remarks
        )

    except ValueError as exc:

        message = str(exc)

        if message == "Leave request not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    return get_admin_leave(leave_id)