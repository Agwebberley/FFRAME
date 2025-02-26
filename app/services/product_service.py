from flask import current_app
from app.models.product import Product
from app.extensions import db
from app.auth.permissions import check_permission


class ProductService:
    @staticmethod
    def create(product_data, current_user):
        current_app.logger.debug("User %s attempting to create Product with data: %s", current_user, product_data)
        # Authorization: Check if current_user can create a product
        check_permission(current_user, action="create", resource="Product")

        new_product = Product(**product_data)
        db.session.add(new_product)
        db.session.commit()

        current_app.logger.info("Product created successfully with id: %s", new_product.id)
        return new_product

    @staticmethod
    def update(product_id, product_data, current_user):
        current_app.logger.debug("User %s attempting to update Product id %s with data: %s", current_user, product_id, product_data)
        check_permission(current_user, action="update", resource="Product")

        product = Product.query.get(product_id)
        if not product:
            current_app.logger.error("Product update failed: Product with id %s not found", product_id)
            raise Exception("Product not found")

        for key, value in product_data.items():
            setattr(product, key, value)
        db.session.commit()

        current_app.logger.info("Product updated successfully with id: %s", product_id)
        return product

    @staticmethod
    def delete(product_id, current_user):
        current_app.logger.debug("User %s attempting to delete Product with id: %s", current_user, product_id)
        check_permission(current_user, action="delete", resource="Product")

        product = Product.query.get(product_id)
        if not product:
            current_app.logger.error("Product deletion failed: Product with id %s not found", product_id)
            raise Exception("Product not found")

        db.session.delete(product)
        db.session.commit()

        current_app.logger.info("Product deleted successfully with id: %s", product_id)
        return True
