"""
Organization routes module.
This module provides all the endpoints related to organization management, 
including creating, updating, retrieving, deleting organizations, and managing members.
"""

from flask import Blueprint, request, jsonify
from flask_restx import Resource
from datetime import datetime
from ..common.database import db
from ..common.utils import format_error_response, format_success_response
from ..common.docs.base import org_ns
from .docs.models import (
    organization_model, organization_create_model, organization_update_model, organization_response_model,
    org_not_found_model, org_validation_error_model, org_success_model
)
from .models import Organization
from modules.auth.utils.auth import require_auth, get_current_user

# Create Blueprint for organization routes
organization_bp = Blueprint('organization', __name__)

@org_ns.route('/')
class OrganizationList(Resource):
    @require_auth
    @org_ns.response(200, 'List of organizations', [organization_response_model])
    def get(self):
        """Retrieve all organizations"""
        organizations = Organization.query.all()
        return format_success_response({
            "organizations": [
                {
                    "id": str(org.id),
                    "name": org.name,
                    "description": org.description,
                    "created_at": org.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_at": org.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                for org in organizations
            ]
        }, "Organizations retrieved successfully")

    @require_auth
    @org_ns.expect(organization_create_model)
    @org_ns.response(201, 'Organization created successfully', org_success_model)
    @org_ns.response(400, 'Validation error', org_validation_error_model)
    def post(self):
        """Create a new organization"""
        data = request.get_json()
        
        if not data.get("name"):
            return format_error_response({
                "error": "Organization name is required"
            }, 400)
        
        new_org = Organization(
            name=data["name"],
            description=data.get("description"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        try:
            db.session.add(new_org)
            db.session.commit()
            return format_success_response({
                "id": str(new_org.id),
                "name": new_org.name,
                "description": new_org.description
            }, "Organization created successfully", 201)
        except Exception as e:
            db.session.rollback()
            return format_error_response({
                "error": f"Failed to create organization: {str(e)}"
            }, 500)

@org_ns.route('/<string:org_id>')
class OrganizationDetail(Resource):
    @require_auth
    @org_ns.response(200, 'Organization retrieved successfully', organization_response_model)
    @org_ns.response(404, 'Organization not found', org_not_found_model)
    def get(self, org_id):
        """Retrieve a specific organization"""
        organization = Organization.query.get(org_id)
        if not organization:
            return format_error_response({"error": "Organization not found"}, 404)
        
        return format_success_response({
            "id": str(organization.id),
            "name": organization.name,
            "description": organization.description,
            "created_at": organization.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": organization.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }, "Organization retrieved successfully")

    @require_auth
    @org_ns.expect(organization_update_model)
    @org_ns.response(200, 'Organization updated successfully', org_success_model)
    @org_ns.response(404, 'Organization not found', org_not_found_model)
    def put(self, org_id):
        """Update an existing organization"""
        data = request.get_json()
        organization = Organization.query.get(org_id)
        
        if not organization:
            return format_error_response({"error": "Organization not found"}, 404)

        organization.name = data.get("name", organization.name)
        organization.description = data.get("description", organization.description)
        organization.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            return format_success_response({
                "id": str(organization.id),
                "name": organization.name,
                "description": organization.description
            }, "Organization updated successfully")
        except Exception as e:
            db.session.rollback()
            return format_error_response({
                "error": f"Failed to update organization: {str(e)}"
            }, 500)

    @require_auth
    @org_ns.response(200, 'Organization deleted successfully', org_success_model)
    @org_ns.response(404, 'Organization not found', org_not_found_model)
    def delete(self, org_id):
        """Delete an organization"""
        organization = Organization.query.get(org_id)
        if not organization:
            return format_error_response({"error": "Organization not found"}, 404)
        
        try:
            db.session.delete(organization)
            db.session.commit()
            return format_success_response({}, "Organization deleted successfully")
        except Exception as e:
            db.session.rollback()
            return format_error_response({
                "error": f"Failed to delete organization: {str(e)}"
            }, 500)


