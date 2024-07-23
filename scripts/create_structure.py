import os
import shutil

# Define the folder structure and files
structure = {
    "address": [
        "addr_city_dao.py",
        "addr_country_dao.py",
        "addr_region_dao.py",
        "address_dao.py"
    ],
    "entities": [
        "entity_address_dao.py",
        "entity_amenities_dao.py",
        "entity_billable_dao.py",
        "entity_media_dao.py"
    ],
    "properties": [
        "property_dao.py",
        "property_assignment_dao.py",
        "property_unit_dao.py",
        "property_unit_assoc_dao.py"
    ],
    "billing": [
        "invoice_dao.py",
        "invoice_item_dao.py",
        "transaction_dao.py",
        "transaction_type_dao.py",
        "payment_type_dao.py"
    ],
    "contracts": [
        "contract_dao.py",
        "contract_type_dao.py",
        "under_contract_dao.py"
    ],
    "auth": [
        "user_dao.py",
        "role_dao.py",
        "permission_dao.py",
        "auth_dao.py",
        "company_dao.py"
    ],
    "communication": [
        "calendar_event_dao.py",
        "message_dao.py",
        "maintenance_request_dao.py",
        "tour_booking_dao.py"
    ],
    "resources": [
        "amenities_dao.py",
        "media_dao.py",
        "utilities_dao.py",
        "base_dao.py"
    ]
}

# Create folders and copy files
for folder, files in structure.items():
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Create __init__.py file in the folder
    init_file_path = os.path.join(folder, '__init__.py')
    with open(init_file_path, 'w') as f:
        f.write(f"# {folder} package\n")
    
    for file in files:
        # Check if the file exists in the current directory
        if os.path.isfile(file):
            # Define source and destination paths
            src = os.path.join(os.getcwd(), file)
            dst = os.path.join(folder, file)
            
            # Copy the file
            shutil.copy(src, dst)
            print(f"Copied {file} to {folder}")
        else:
            print(f"File {file} not found in the current directory")

print("Folders and files copied successfully.")
