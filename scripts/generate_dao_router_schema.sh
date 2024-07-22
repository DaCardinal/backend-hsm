#!/bin/bash

# Check if a model name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <model_name>"
  exit 1
fi

###############################
######## ADD DAO ##############
###############################

# Capitalize the first letter of the model name
MODEL_NAME=$(echo "$1" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')

# Convert the model name to lowercase for the filename
MODEL_NAME_LOWER=$(echo "$MODEL_NAME" | tr '[:upper:]' '[:lower:]')
# Create the directory if it does not exist
mkdir -p app/dao

# Define the routers directory
DAO_DIRECTORY="./app/dao"

# Define the output file path
OUTPUT_FILE="${DAO_DIRECTORY}/${MODEL_NAME_LOWER}_dao.py"

# Check if the router file already exists
if [ -f "$OUTPUT_FILE" ]; then
    echo "DAO file $OUTPUT_FILE already exists."
else
    # Create the routers directory if it does not exist
    mkdir -p $DAO_DIRECTORY

    # Generate the Python code and save it to the file
    cat << EOF > $OUTPUT_FILE
from typing import Type

from dao.base_dao import BaseDAO
from models import $MODEL_NAME

class ${MODEL_NAME}DAO(BaseDAO[$MODEL_NAME]):
    def __init__(self, model: Type[$MODEL_NAME], load_parent_relationships: bool = False, load_child_relationships: bool = False, excludes = []):
        super().__init__(model, load_parent_relationships, load_child_relationships, excludes=excludes)
        self.primary_key = "${MODEL_NAME_LOWER}_id"
EOF
    # Confirm that the file was created
    echo "DAO File created: $OUTPUT_FILE"
fi

###############################
######## ADD ROUTER ###########
###############################

# Define the routers directory
ROUTER_DIRECTORY="./app/router"

# Define the router output file path
ROUTER_OUTPUT_FILE="$ROUTER_DIRECTORY/${MODEL_NAME_LOWER}_router.py"

# Check if the router file already exists
if [ -f "$ROUTER_OUTPUT_FILE" ]; then
    echo "Router file $ROUTER_OUTPUT_FILE already exists."
else
    # Create the routers directory if it does not exist
    mkdir -p $ROUTER_DIRECTORY

    # Generate the Python code and save it to the file
    cat << EOF > $ROUTER_OUTPUT_FILE
from typing import List

from models import $MODEL_NAME
from dao.${MODEL_NAME_LOWER}_dao import ${MODEL_NAME}DAO
from schema import ${MODEL_NAME}Schema
from router.base_router import BaseCRUDRouter

class ${MODEL_NAME}Router(BaseCRUDRouter):

    def __init__(self, dao: ${MODEL_NAME}DAO = ${MODEL_NAME}DAO($MODEL_NAME, load_parent_relationships=False, load_child_relationships=False), prefix: str = "", tags: List[str] = []):
        super().__init__(dao=dao, schemas=${MODEL_NAME}Schema, prefix=prefix, tags=tags)
        self.dao = dao
        self.register_routes()

    def register_routes(self):
        pass
EOF

    # Confirm that the file was created
    echo "Router File created: $ROUTER_OUTPUT_FILE"
fi

###############################
######## ADD SCHEMA ###########
###############################

# Define the schema file path
SCHEMA_FILE="app/schema/schemas.py"

# Check if the schema line is already imported
if grep -q "${MODEL_NAME}Schema = generate_schemas_for_sqlalchemy_model($MODEL_NAME, excludes=" "$SCHEMA_FILE"; then
  echo "Schema line for $MODEL_NAME already imported in: $SCHEMA_FILE"
else
  # Append the schema generation line to the schema file without trailing newline
  printf "\n${MODEL_NAME}Schema = generate_schemas_for_sqlalchemy_model($MODEL_NAME, excludes=['${MODEL_NAME_LOWER}_id'])" >> $SCHEMA_FILE
  # Confirm that the schema line was added
  echo "Schema line added to: $SCHEMA_FILE"
fi

# Update the import line in the schema file
IMPORT_LINE=$(grep -E '^from models import ' $SCHEMA_FILE)

if [[ $IMPORT_LINE == *"$MODEL_NAME"* ]]; then
  echo "$MODEL_NAME is already imported in $SCHEMA_FILE"
else
  NEW_IMPORT_LINE="${IMPORT_LINE%,}"
  
  sed -i '' "s|$IMPORT_LINE|$NEW_IMPORT_LINE, $MODEL_NAME|" $SCHEMA_FILE
  echo "Model added to import line in: $SCHEMA_FILE"
fi

SCHEMA_FILE="app/schema/__init__.py"
# Update the import line in the schema file
IMPORT_LINE=$(grep -E '^from schema.schemas import ' $SCHEMA_FILE)

if [[ $IMPORT_LINE == *"$MODEL_NAME"* ]]; then
  echo "$MODEL_NAME is already imported in $SCHEMA_FILE"
else
  NEW_IMPORT_LINE="${IMPORT_LINE%,}"
  
  sed -i '' "s|$IMPORT_LINE|$NEW_IMPORT_LINE, ${MODEL_NAME}Schema|" $SCHEMA_FILE
  echo "Model added to import line in: $SCHEMA_FILE"
fi

###############################
######## ADD ROUTERS ##########
###############################

ROUTER_IMPORTS="app/utils/__init__.py"
# Update the import line in the schema file
IMPORT_LINE=$(grep -E '^from schema.schemas import ' $SCHEMA_FILE)

if [[ $IMPORT_LINE == *"$MODEL_NAME"* ]]; then
  echo "$MODEL_NAME is already imported in $SCHEMA_FILE"
else
  NEW_IMPORT_LINE="${IMPORT_LINE%,}"
  
  sed -i '' "s|$IMPORT_LINE|$NEW_IMPORT_LINE, ${MODEL_NAME}Schema|" $SCHEMA_FILE
  echo "Model added to import line in: $SCHEMA_FILE"
fi


ROUTES_FILE="app/utils/routes.py"

# Check if the file exists
if [ ! -f "$ROUTES_FILE" ]; then
    echo "Error: $ROUTES_FILE not found."
    exit 1
fi

# Check if the line already exists in the file
if grep -q "app\.include_router(${MODEL_NAME}Router" "$ROUTES_FILE"; then
  echo "Line already exists in $ROUTES_FILE. Skipping addition."
else
  # # # Use sed to add the line after the specified pattern
  # sed -i '' '/app\.include_router(router)/a \
  #   \
  #   # Create an instance of '${MODEL_NAME}'Router\
  #   app.include_router('${MODEL_NAME}'Router(prefix="/'${MODEL_NAME_LOWER}'", tags=["'${MODEL_NAME}'"]).router) \
  #     ' "$ROUTES_FILE"

  NEW_LINE="    \n    # Create an instance of ${MODEL_NAME}Router\n    app.include_router(${MODEL_NAME}Router(prefix=\"/${MODEL_NAME_LOWER}\", tags=[\"${MODEL_NAME}\"]).router)"

  awk -v new_line="$NEW_LINE" '
      /def configure_routes\(app: FastAPI\)/ { inside_function = 1 }
      inside_function && /^    / { buffer = buffer $0 "\n"; next }
      { print }
      END { if (inside_function) print buffer new_line }
  ' "$ROUTES_FILE" > temp_file && mv temp_file "$ROUTES_FILE"

  echo "New route added to configure_routes function in $ROUTES_FILE"
fi

# Define the import file path
IMPORT_FILE="app/router/__init__.py"

# Define the line to be added
NEW_LINE="from router.${MODEL_NAME_LOWER}_router import ${MODEL_NAME}Router"

# Check if the file exists
if [ ! -f "$IMPORT_FILE" ]; then
    echo "Error: $IMPORT_FILE not found."
    exit 1
fi

# Check if the line already exists in the file
if grep -q "$NEW_LINE" "$IMPORT_FILE"; then
    echo "Line already exists in $IMPORT_FILE. Skipping addition."
else
    # Add the new line to the end of the file
    printf "\n$NEW_LINE" >> "$IMPORT_FILE"
    echo "Line added to $IMPORT_FILE."
fi