from flask import Blueprint, request, jsonify
import uuid

handlers_blueprint = Blueprint('handlers', __name__)

# ---------------------------------------------------------------------> Health Endppoints

@handlers_blueprint.route('/healthz/liveness')
def liveness():
    return "It's live"

@handlers_blueprint.route('/healthz/readiness')
def readiness():
    return "It's ready"

# Dictionary to store services (name - api_key - id)
services = []

# ---------------------------------------------------------------------> Service Endppoints

@handlers_blueprint.route('/commands/service', methods=['POST'])
def create_service():
    data = request.json
    if 'service_name' not in data:
        return jsonify({'error': 'Missing service_name field in JSON request'}), 400

    service_name = data['service_name']
    for service in services:
        if 'name' in service and service['name'] == service_name:
            return jsonify({'error': f'Service name "{service_name}" already exists'}), 400

    api_key = str(uuid.uuid4())
    id = len(services) + 1

    services.append({'id': id, 'name': service_name, 'api_key': api_key})

    return jsonify({'id': id, 'api_key': api_key}), 200

@handlers_blueprint.route('/commands/service/<service_name>', methods=['GET'])
def read_service(service_name):
    for service in services:
        if 'name' in service and service['name'] == service_name:
            return jsonify(service), 200

    return jsonify({'error': f'Service "{service_name}" not found'}), 404

@handlers_blueprint.route('/commands/service/<service_name>', methods=['PUT'])
def update_service(service_name):
    for service in services:
        if 'name' in service and service['name'] == service_name:
            return jsonify({'id': service['id'], 'api_key': service['api_key']}), 200

    return jsonify({'error': f'Service "{service_name}" not found'}), 404

@handlers_blueprint.route('/commands/service/<service_name>', methods=['DELETE'])
def delete_service(service_name):
    for idx, template in enumerate(templates):
        if 'service_name' in template and template['service_name'] == service_name:
            del templates[idx]

    for idx, service in enumerate(services):
        if 'name' in service and service['name'] == service_name:
            del services[idx]
            return jsonify({'message': f'Service "{service_name}" deleted successfully'}), 200

    return jsonify({'error': f'Service "{service_name}" not found'}), 404

# ---------------------------------------------------------------------> Template Endpoints

# Dictionary to store templates (service_name - name - id)
templates = []

@handlers_blueprint.route('/commands/template/<service_name>', methods=['POST'])
def create_template(service_name):
    data = request.json
    if 'name' not in data:
        return jsonify({'error': 'Missing name field in JSON request'}), 400
    template_name = data['name']

    found_service=False
    for service in services:
        if 'name' in service and service['name'] == service_name:
            found_service=True
    if not found_service:
        return jsonify({'error': f'Service "{service_name}" doesn\'t exists'}), 400

    for template in templates:
        if ('service_name' in template and template['service_name'] == service_name) and ('name' in template and template['name'] == template_name):
            return jsonify({'error': f'Template "{template_name}" already exists for "{service_name}"'}), 400

    # Generate the ID for the new template
    template_id = len(templates) + 1
    new_template = {'id': template_id, 'name': template_name, 'service_name': service_name}
    templates.append(new_template)

    # Return the ID of the newly created template
    return jsonify({'id': template_id}), 200

@handlers_blueprint.route('/commands/template/<service_name>/<template_name>', methods=['GET'])
def read_template(service_name, template_name):
    found_service=False
    for service in services:
        if 'name' in service and service['name'] == service_name:
            found_service=True
    if not found_service:
        return jsonify({'error': f'Service "{service_name}" not found'}), 404

    for template in templates:
        if ('service_name' in template and template['service_name'] == service_name) and ('name' in template and template['name'] == template_name):
            return jsonify({'id': template['id']}), 200

    return jsonify({'error': f'Template "{template_name}" not found for "{service_name}"'}), 404

@handlers_blueprint.route('/commands/template/<service_name>/<template_name>', methods=['PUT'])
def update_template(service_name, template_name):
    data = request.json
    return read_template(service_name, template_name)

@handlers_blueprint.route('/commands/template/<service_name>/<template_name>', methods=['DELETE'])
def delete_template(service_name, template_name):
    found_service=False
    for service in services:
        if 'name' in service and service['name'] == service_name:
            found_service=True
    if not found_service:
        return jsonify({'error': f'Service "{service_name}" doesn\'t exists'}), 404

    for idx, template in enumerate(templates):
        if ('service_name' in template and template['service_name'] == service_name) and ('name' in template and template['name'] == template_name):
            del templates[idx]
            return jsonify({'message': f'Template "{template_name}" deleted successfully for service "{service_name}"'}), 200

    return jsonify({'error': f'Template "{template_name}" not found for service "{service_name}"'}), 404

