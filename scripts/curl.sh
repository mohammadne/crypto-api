#!/bin/bash

address="http://127.0.0.1:1995"

# ----------------------------------------------------------------> Service

# Create Service
curl -X POST "$address/commands/service" \
-H "Content-Type: application/json" \
-d '{"service_name": "service1"}'

# Get Service
curl -X GET $address/commands/service/call.automation

# Update Service
curl -X PUT "$address/commands/service/service1" \
-H "Content-Type: application/json" \
-d '{"field_key": "field_value"}'

# Delete Service
curl -X DELETE "$address/commands/service/service1"

# ----------------------------------------------------------------> Template

# Create Template
curl -X POST "$address/commands/template/service1" \
-H "Content-Type: application/json" \
-d '{"name": "template1"}'

# Get Template
curl -X GET $address/commands/template/call.automation/user-not-installed-application.automation

# Update Template
curl -X PUT "$address/commands/template/service1/template1" \
-H "Content-Type: application/json" \
-d '{"field_key": "field_value"}'

# Delete Template
curl -X DELETE "$address/commands/template/service1/template1"
