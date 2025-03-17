from flask_restx import fields, Namespace

# Namespace for Organization
org_ns = Namespace("organization", description="Organization management operations")

# Organization Model (Response)
organization_model = org_ns.model(
    "Organization",
    {
        "id": fields.String(
            required=True, 
            description="Unique identifier for the organization", 
            example="org_12345"
        ),
        "name": fields.String(
            required=True, 
            description="Organization Name", 
            example="Acme Corp"
        ),
        "email": fields.String(
            required=True, 
            description="Primary email associated with the organization", 
            example="info@acmecorp.com",
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        ),
        "phone": fields.String(
            required=False, 
            description="Primary contact number of the organization", 
            example="+1-800-123-4567",
            pattern=r"^\+?[1-9]\d{1,14}$"
        ),
        "address": fields.String(
            required=False, 
            description="Physical address of the organization", 
            example="1234 Elm Street, Springfield, USA"
        ),
        "website": fields.String(
            required=False, 
            description="Official website URL", 
            example="https://www.acmecorp.com"
        ),
        "industry": fields.String(
            required=False, 
            description="Type of industry", 
            example="Technology"
        ),
        "size": fields.Integer(
            required=False, 
            description="Number of employees in the organization", 
            example=500
        ),
        "owner_id": fields.String(
            required=True, 
            description="User ID of the organization owner", 
            example="user_67890"
        ),
        "created_at": fields.DateTime(
            description="Timestamp when the organization was created", 
            example="2024-03-17T12:34:56Z"
        ),
        "updated_at": fields.DateTime(
            description="Timestamp when the organization was last updated", 
            example="2024-06-21T08:22:11Z"
        ),
        "is_active": fields.Boolean(
            description="Indicates whether the organization is active", 
            example=True
        ),
    },
)

# Create Organization Model (Request)
create_organization_model = org_ns.model(
    "CreateOrganization",
    {
        "name": fields.String(
            required=True, 
            description="Organization Name", 
            example="Acme Corp"
        ),
        "email": fields.String(
            required=True, 
            description="Organization Email", 
            example="info@acmecorp.com",
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        ),
        "phone": fields.String(
            required=False, 
            description="Phone Number", 
            example="+1-800-123-4567",
            pattern=r"^\+?[1-9]\d{1,14}$"
        ),
        "address": fields.String(
            required=False, 
            description="Organization Address", 
            example="1234 Elm Street, Springfield, USA"
        ),
        "website": fields.String(
            required=False, 
            description="Organization Website", 
            example="https://www.acmecorp.com"
        ),
        "industry": fields.String(
            required=False, 
            description="Industry Type", 
            example="Technology"
        ),
        "size": fields.Integer(
            required=False, 
            description="Organization Size", 
            example=500
        ),
    },
)

organization_successfully_create_modal = org_ns.model("OrganizationSuccessfullyCreated", {
    "message": fields.String(default="Organization successfully created"),
    "data": fields.Nested(organization_model),
})

organization_successfully_fetched_model = org_ns.model("OrganizationSuccessfullyFetched", {
    "message": fields.String(default="Organization successfully fetched"),
    "data": fields.Nested(organization_model),  # Ensure 'data' is a nested object
})

organizations_successfully_fetched_model = org_ns.model("OrganizationsSuccessfullyFetched", {
    "message": fields.String(default="Organizations successfully fetched"),
    "data": fields.List(fields.Nested(organization_model)),  # Use List for multiple orgs
})

organization_validation_error_model = org_ns.model("OrganizationValidationError", {
    "error": fields.String(
        required=True,
        description="Error message indicating validation failure",
        example="Missing required fields"
    ),
    "details": fields.Raw(
        required=True,
        description="Detailed field-specific validation errors (if applicable)",
        example={}
    ),
    "missing_fields": fields.List(
        fields.String,
        description="List of missing required fields",
        example=["name", "email"]
    )
})

# Update Organization Model (Request)
update_organization_model = org_ns.model(
    "UpdateOrganization",
    {
        "name": fields.String(
            required=False, 
            description="Updated organization name", 
            example="Acme Corporation"
        ),
        "email": fields.String(
            required=False, 
            description="Updated organization email", 
            example="support@acmecorp.com",
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        ),
        "phone": fields.String(
            required=False, 
            description="Updated phone number", 
            example="+1-800-987-6543",
            pattern=r"^\+?[1-9]\d{1,14}$"
        ),
        "address": fields.String(
            required=False, 
            description="Updated organization address", 
            example="5678 Oak Avenue, Metropolis, USA"
        ),
        "website": fields.String(
            required=False, 
            description="Updated website URL", 
            example="https://www.new-acme.com"
        ),
        "industry": fields.String(
            required=False, 
            description="Updated industry type", 
            example="E-commerce"
        ),
        "size": fields.Integer(
            required=False, 
            description="Updated organization size", 
            example=1000
        ),
        "is_active": fields.Boolean(
            required=False, 
            description="Update organization status (true=active, false=inactive)", 
            example=False
        ),
    },
)

# Delete Organization Response Model
delete_organization_response_model = org_ns.model(
    "DeleteOrganizationResponse",
    {
        "message": fields.String(
            description="Success message", 
            example="Organization deleted successfully"
        ),
        "organization_id": fields.String(
            description="ID of the deleted organization", 
            example="org_12345"
        ),
    },
)

# Organization Activation Model (Enable/Disable Organization)
activate_organization_model = org_ns.model(
    "ActivateOrganization",
    {
        "is_active": fields.Boolean(
            required=True, 
            description="Set organization status (true=active, false=inactive)", 
            example=True
        ),
    },
)

# Organization Search Filter Model
search_organization_model = org_ns.model(
    "SearchOrganization",
    {
        "name": fields.String(
            required=False, 
            description="Filter by organization name", 
            example="Acme"
        ),
        "industry": fields.String(
            required=False, 
            description="Filter by industry type", 
            example="Technology"
        ),
        "size_min": fields.Integer(
            required=False, 
            description="Minimum organization size", 
            example=50
        ),
        "size_max": fields.Integer(
            required=False, 
            description="Maximum organization size", 
            example=5000
        ),
        "is_active": fields.Boolean(
            required=False, 
            description="Filter by active/inactive status", 
            example=True
        ),
    },
)
