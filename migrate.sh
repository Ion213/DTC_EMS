#!/bin/bash

# Stamp the database to the latest revision
flask db stamp head

# Generate a migration script with the description of the changes
flask db migrate -m "Description of the changes"

# Apply the migration to update the database schema
flask db upgrade

