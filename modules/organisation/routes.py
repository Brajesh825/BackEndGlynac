from flask_restx import Namespace, Resource
from .models import db, Organization
from .docs.models import org_ns, organization_model, create_organization_model ,organization_successfully_fetched_model, organizations_successfully_fetched_model, organization_successfully_create_modal, organization_validation_error_model
from modules.auth.utils.auth import require_auth, get_current_user
from ..common.utils import format_error_response, format_success_response
from .validation import validate_organization_data
from ..auth.docs.models import user_unauthorized_model , user_forbidden_model


@org_ns.route("/")
@org_ns.route("/")
class OrganizationList(Resource):
    @org_ns.expect(create_organization_model)
    @org_ns.response(201, "Organization Created", organization_successfully_create_modal)
    @org_ns.response(400, "Validation Error", organization_validation_error_model)
    @org_ns.response(401, "Unauthorized", user_unauthorized_model)
    @org_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth(roles=["admin", "owner"])  # Only admins or owners can create organizations
    def post(self):
        """Create a new organization"""
        data = org_ns.payload
        current_user = get_current_user()

        # Validate the organization data
        is_valid, field_errors, missing_fields = validate_organization_data(data)

        if not is_valid:
            return format_error_response(
                message={
                    "error": "Validation Error",
                    "details": field_errors,
                    "missing_fields": missing_fields,
                },
                status_code=400
            )

        new_org = Organization(
            name=data["name"],
            email=data["email"],
            phone=data.get("phone"),
            address=data.get("address"),
            website=data.get("website"),
            industry=data.get("industry"),
            size=data.get("size"),
            owner_id=current_user.id  # Assign the logged-in user as owner
        )
        db.session.add(new_org)
        db.session.commit()

        return format_success_response(new_org.to_dict(), "Organization Created")

    @org_ns.response(200, "Success", organizations_successfully_fetched_model)
    @org_ns.response(401, "Unauthorized", user_unauthorized_model)
    @org_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth()
    def get(self):
        """Get all organizations where the user is the owner (active only)"""
        current_user = get_current_user()
        organizations = Organization.query.filter_by(owner_id=current_user.id, is_active=True).all()
        
        return format_success_response([org.to_dict() for org in organizations])

@org_ns.route("/<string:org_id>")
class OrganizationResource(Resource):
    @org_ns.response(200, "Success", organization_successfully_fetched_model)
    @org_ns.response(401, "Unauthorized", user_unauthorized_model)
    @org_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth()
    def get(self, org_id):
        """Retrieve an organization by ID (Only if the user is the owner)"""
        current_user = get_current_user()
        org = Organization.query.filter_by(id=org_id, is_active=True, owner_id=current_user.id).first()
        
        if not org:
            return format_error_response({"error": "Organization not found", "errorType": "not_found"}, 404)

        return format_success_response(org.to_dict())

    @org_ns.expect(create_organization_model)
    @org_ns.response(401, "Unauthorized", user_unauthorized_model)
    @org_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth(roles=["admin", "owner"])
    def put(self, org_id):
        """Update an organization (Only owners or admins)"""
        org = Organization.query.get_or_404(org_id)
        current_user = get_current_user()

        if current_user.id != org.owner_id and current_user.role != "admin":
            return {"error": "You do not have permission to update this organization"}, 403

        data = org_ns.payload
        for key, value in data.items():
            setattr(org, key, value)
        db.session.commit()
        
        return org.to_dict()

    @org_ns.response(200, "Organization Deleted (Soft Delete)")
    @org_ns.response(401, "Unauthorized", user_unauthorized_model)
    @org_ns.response(403, "Forbidden", user_forbidden_model)
    @require_auth(roles=["admin", "owner"])
    def delete(self, org_id):
        """Soft delete an organization"""
        org = Organization.query.get_or_404(org_id)
        current_user = get_current_user()

        if current_user.id != org.owner_id and current_user.role != "admin":
            return {"error": "You do not have permission to delete this organization"}, 403

        org.is_active = False  # Soft delete
        db.session.commit()
        return {"message": "Organization deleted successfully"}, 200
