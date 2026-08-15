from app.repositories.employee_repository import (
    create_employee,
    get_all_employee,
    get_employee_by_id,
    update_employee,
    deactivate_employee
) 

def create_new_employee(
    employee_code,
    user_id,
    first_name,
    last_name,
    email,
    phone,
    date_of_birth,
    gender,
    address,
    city,
    state,
    country,
    postal_code,
    joining_date,
    employment_type,
    department_id,
    designation_id,
    manager_id,
    salary,
    emergency_contact_name,
    emergency_contact_phone
):

    return create_employee(
        employee_code=employee_code,
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        date_of_birth=date_of_birth,
        gender=gender,
        address=address,
        city=city,
        state=state,
        country=country,
        postal_code=postal_code,
        joining_date=joining_date,
        employment_type=employment_type,
        department_id=department_id,
        designation_id=designation_id,
        manager_id=manager_id,
        salary=salary,
        emergency_contact_name=emergency_contact_name,
        emergency_contact_phone=emergency_contact_phone
    ) 