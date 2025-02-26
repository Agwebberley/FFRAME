from flask import current_app


def check_permission(current_user, action, resource):
    # Not Implimented
    current_app.logger.debug("DEBUG: Permission Granted")
    return True
