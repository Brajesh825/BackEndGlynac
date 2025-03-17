from .models import Organization, Department, Employee, Meeting
from .routes import org_ns  # Import namespace

__all__ = ["Organization", "Department", "Employee", "Meeting"]

def init_app(app):
    """Initialize the organization module with the Flask app."""
    from modules.common.docs.base import api  # Ensure you import API instance

    api.add_namespace(org_ns)  # ✅ Ensure namespace is added