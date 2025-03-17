from flask_restx import Namespace, Resource
from .models import db, Department
from .docs.models import dept_ns, department_model, create_department_model, department_successfully_fetched_model, departments_successfully_fetched_model, department_successfully_create_modal, department_validation_error_model
from modules.auth.utils.auth import require_auth, get_current_user
from ..common.utils import format_error_response, format_success_response
from .validation import validate_department_data
from ..auth.docs.models import user_unauthorized_model , user_forbidden_model

@dept_ns.route("/")
class DepartmentList(Resource):
    @dept_ns.expect(create_department_model)
    @dept_ns.response(201, "Department Created", department_successfully_create_modal)
    @dept_ns.response(400, "Validation Error", department_validation_error_model)
    @dept_ns.response(401, "Unauthorized", user_unauthorized_model)
    @dept_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth(roles=["admin", "owner"])  # Only admins or owners can create departments
    def post(self):
        """Create a new department"""
        data = dept_ns.payload
        current_user = get_current_user()

        # Validate the department data
        is_valid, field_errors, missing_fields = validate_department_data(data)

        if not is_valid:
            return format_error_response(
                message={
                    "error": "Validation Error",
                    "details": field_errors,
                    "missing_fields": missing_fields,
                },
                status_code=400
            )

        new_dept = Department(
            name=data["name"],
            organisation_id=data["organisation_id"],
            description=data.get("description"),
            parent_department_id=data.get("parent_department_id"),
            head_id=data.get("head_id"),
            office_location=data.get("office_location")
        )
        db.session.add(new_dept)
        db.session.commit()

        return format_success_response(new_dept.to_dict(), "Department Created")

    @dept_ns.response(200, "Success", departments_successfully_fetched_model)
    @dept_ns.response(401, "Unauthorized", user_unauthorized_model)
    @dept_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth()
    def get(self):
        """Get all departments"""
        departments = Department.query.all()
        return format_success_response([dept.to_dict() for dept in departments])

@dept_ns.route("/<string:dept_id>")
class DepartmentResource(Resource):
    @dept_ns.response(200, "Success", department_successfully_fetched_model)
    @dept_ns.response(401, "Unauthorized", user_unauthorized_model)
    @dept_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth()
    def get(self, dept_id):
        """Retrieve a department by ID"""
        dept = Department.query.get_or_404(dept_id)
        return format_success_response(dept.to_dict())

    @dept_ns.expect(create_department_model)
    @dept_ns.response(200, "Department Updated", department_successfully_create_modal)
    @dept_ns.response(400, "Validation Error", department_validation_error_model)
    @dept_ns.response(401, "Unauthorized", user_unauthorized_model)
    @dept_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth(roles=["admin", "owner"])
    def put(self, dept_id):
        """Update a department"""
        dept = Department.query.get_or_404(dept_id)
        data = dept_ns.payload

        # Validate the department data
        is_valid, field_errors, missing_fields = validate_department_data(data, is_update=True)

        if not is_valid:
            return format_error_response(
                message={
                    "error": "Validation Error",
                    "details": field_errors,
                    "missing_fields": missing_fields,
                },
                status_code=400
            )

        for key, value in data.items():
            setattr(dept, key, value)
        db.session.commit()

        return format_success_response(dept.to_dict(), "Department Updated")

    @dept_ns.response(200, "Department Deleted")
    @dept_ns.response(401, "Unauthorized", user_unauthorized_model)
    @dept_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth(roles=["admin", "owner"])
    def delete(self, dept_id):
        """Delete a department"""
        dept = Department.query.get_or_404(dept_id)
        db.session.delete(dept)
        db.session.commit()
        return {"message": "Department deleted successfully"}, 200
