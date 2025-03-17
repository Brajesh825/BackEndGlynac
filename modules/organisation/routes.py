from flask_restx import Namespace, Resource, fields
from modules.common.docs.base import api  # Import the API instance

# Create namespace
org_ns = Namespace("organization", description="Organization management operations")

# Define request & response models
organization_model = org_ns.model(
    "Organization",
    {
        "id": fields.Integer(required=True, description="Organization ID"),
        "name": fields.String(required=True, description="Organization Name"),
        "address": fields.String(required=False, description="Organization Address"),
    },
)

create_organization_model = org_ns.model(
    "CreateOrganization",
    {
        "name": fields.String(required=True, description="Organization Name"),
        "address": fields.String(required=False, description="Organization Address"),
    },
)

@org_ns.route("/")
class OrganizationList(Resource):
    @org_ns.expect(create_organization_model)  # ✅ Attach model here
    @org_ns.response(201, "Organization Created", organization_model)  # ✅ Response Model
    @org_ns.response(400, "Validation Error")
    def post(self):
        """Create a new organization"""
        data = org_ns.payload  # Get request payload
        return {"id": 1, "name": data["name"], "address": data.get("address")}, 201

