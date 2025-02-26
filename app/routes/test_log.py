from flask import Blueprint, current_app

# Define Blueprint
test_log_bp = Blueprint('test_log', __name__)


@test_log_bp.route('/test-log')
def test_log():
    current_app.logger.debug('This is a DEBUG message')
    current_app.logger.info('This is an INFO message')
    current_app.logger.warning('This is a WARNING message')
    current_app.logger.error('This is an ERROR message')
    current_app.logger.critical('This is a CRITICAL message')
    return "Logs have been generated."
