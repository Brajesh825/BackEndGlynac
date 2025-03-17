import re
from urllib.parse import urlparse

def validate_email_format(email):
    """Validate email format.
    
    Args:
        email (str): Email address to validate.
    
    Returns:
        tuple: (bool, str) indicating validation success and error message (if any).
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return False, "Invalid email format"
    return True, ""

def validate_phone(phone):
    """Validate phone number format.
    
    Args:
        phone (str): Phone number to validate.
    
    Returns:
        tuple: (bool, str) indicating validation success and error message (if any).
    """
    phone_regex = r'^\+?[1-9]\d{1,14}$'  # Supports international formats (E.164)
    if not re.match(phone_regex, phone):
        return False, "Invalid phone number format"
    return True, ""

def validate_url_format(url):
    """Validate website URL format.
    
    Args:
        url (str): Website URL to validate.
    
    Returns:
        tuple: (bool, str) indicating validation success and error message (if any).
    """
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True, ""
        return False, "Invalid website URL format"
    except Exception:
        return False, "Invalid website URL format"

def validate_password(password):
    """Validate password strength.
    
    Args:
        password (str): Password to validate.
    
    Returns:
        tuple: (bool, str) indicating validation success and error message (if any).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?`~" for char in password):
        return False, "Password must contain at least one special character"
    return True, ""

def validate_organization_data(data):
    """Validate organization creation data.
    
    Args:
        data (dict): The input data containing organization details.
    
    Returns:
        tuple: (bool, dict, list) indicating validation success, field errors, and missing fields.
    """
    required_fields = ["name", "email"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    field_errors = {}

    if missing_fields:
        return False, {}, missing_fields

    # Validate email
    is_valid, error = validate_email_format(data["email"])
    if not is_valid:
        field_errors["email"] = error

    # Validate phone if provided
    if "phone" in data:
        is_valid, error = validate_phone(data["phone"])
        if not is_valid:
            field_errors["phone"] = error

    # Validate website if provided
    if "website" in data:
        is_valid, error = validate_url_format(data["website"])
        if not is_valid:
            field_errors["website"] = error

    return not bool(field_errors), field_errors, []

def validate_department_data(data, is_update=False):
    """Validate department creation data.
    
    Args:
        data (dict): The input data containing department details.
        is_update (bool): Flag to indicate if this is an update operation.
    
    Returns:
        tuple: (bool, dict, list) indicating validation success, field errors, and missing fields.
    """
    required_fields = ["name", "organisation_id"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    field_errors = {}

    if missing_fields and not is_update:
        return False, {}, missing_fields

    # Validate name
    if "name" in data and len(data["name"]) < 2:
        field_errors["name"] = "Department name must be at least 2 characters long"

    # Validate organisation_id
    if "organisation_id" in data and not re.match(r'^[a-fA-F0-9-]{36}$', data["organisation_id"]):
        field_errors["organisation_id"] = "Invalid organisation ID format"

    return not bool(field_errors), field_errors, missing_fields
