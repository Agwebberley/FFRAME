# app/services/user_service.py
import logging
from app.models.user import User
from app.extensions import db
from app.auth.permissions import check_permission

# Configure a module-level logger
logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def create(data, context):
        """
        Create a new User.
        :param data: dict containing user fields (e.g., username, email, etc.)
        :param context: dict containing request context (e.g., current user)
        :return: the newly created User instance
        """
        current_user = context.get("user")
        try:
            # Perform authorization check
            check_permission(current_user, action="create", resource="User")
        except Exception as e:
            logger.error("Permission error while creating user: %s", e)
            raise Exception("Unauthorized to create user.")

        try:
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
            logger.info("User created successfully: %s", new_user.username)
            return new_user
        except Exception as e:
            logger.exception("Error creating user: %s", e)
            db.session.rollback()
            raise Exception("User creation failed.")

    @staticmethod
    def update(user_id, data, context):
        """
        Update an existing User.
        :param user_id: ID of the user to update
        :param data: dict containing updated user fields
        :param context: dict containing request context (e.g., current user)
        :return: the updated User instance
        """
        current_user = context.get("user")
        try:
            check_permission(current_user, action="update", resource="User")
        except Exception as e:
            logger.error("Permission error while updating user: %s", e)
            raise Exception("Unauthorized to update user.")

        try:
            user = User.query.get(user_id)
            if not user:
                logger.warning("User not found with id: %s", user_id)
                raise Exception("User not found")
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            logger.info("User updated successfully: %s", user.username)
            return user
        except Exception as e:
            logger.exception("Error updating user: %s", e)
            db.session.rollback()
            raise Exception("User update failed.")

    @staticmethod
    def delete(user_id, context):
        """
        Delete an existing User.
        :param user_id: ID of the user to delete
        :param context: dict containing request context (e.g., current user)
        :return: True if deletion succeeded
        """
        current_user = context.get("user")
        try:
            check_permission(current_user, action="delete", resource="User")
        except Exception as e:
            logger.error("Permission error while deleting user: %s", e)
            raise Exception("Unauthorized to delete user.")

        try:
            user = User.query.get(user_id)
            if not user:
                logger.warning("User not found with id: %s", user_id)
                raise Exception("User not found")
            db.session.delete(user)
            db.session.commit()
            logger.info("User deleted successfully with id: %s", user_id)
            return True
        except Exception as e:
            logger.exception("Error deleting user: %s", e)
            db.session.rollback()
            raise Exception("User deletion failed.")
