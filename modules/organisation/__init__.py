# organisation/__init__.py
from .models import Organization,Department,Employee,Meeting

__all__ = [
    'Organization',
    'Department',
    'Employee',
    'Meeting',
]


def init_app(app):
    """Initialize the organization module with the Flask app."""
    # Import routes to register them with the namespaces
    # Routes must be imported here to avoid circular imports
    from . import routes  
