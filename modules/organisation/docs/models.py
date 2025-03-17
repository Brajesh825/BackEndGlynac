"""
API Documentation Models for Organization Endpoints.
Defines request and response models using Flask-RESTx.
"""

from flask_restx import fields
from ...common.docs.base import api

# Organization Model
organization_model = api.model("Organization", {
    "id": fields.String(description="Unique identifier of the organization"),
    "name": fields.String(required=True, description="Organization name"),
    "description": fields.String(description="Organization description"),
    "created_at": fields.String(description="Organization creation timestamp"),
    "updated_at": fields.String(description="Last updated timestamp"),
})

# Organization Creation Model
organization_create_model = api.model("CreateOrganization", {
    "name": fields.String(required=True, description="Organization name"),
    "description": fields.String(description="Organization description"),
})

# Organization Update Model
organization_update_model = api.model("UpdateOrganization", {
    "name": fields.String(description="Updated organization name"),
    "description": fields.String(description="Updated organization description"),
})

# Organization Response Model
organization_response_model = api.model("OrganizationResponse", {
    "organization": fields.Nested(organization_model),
})

# Success Response Model
org_success_model = api.model("OrganizationSuccess", {
    "message": fields.String(description="Success message"),
    "data": fields.Nested(organization_model),
})

# Error Responses
org_not_found_model = api.model("OrganizationNotFound", {
    "error": fields.String(description="Organization not found"),
})

org_validation_error_model = api.model("OrganizationValidationError", {
    "error": fields.String(description="Validation error"),
})
