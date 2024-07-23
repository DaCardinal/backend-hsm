import os
import re

# Mapping structure
structure = {
    "address": [
        "addr_city_dao.py",
        "addr_country_dao.py",
        "addr_region_dao.py",
        "address_dao.py",
    ],
    "entities": [
        "entity_address_dao.py",
        "entity_amenities_dao.py",
        "entity_billable_dao.py",
        "entity_media_dao.py",
    ],
    "properties": [
        "property_dao.py",
        "property_assignment_dao.py",
        "property_unit_dao.py",
        "property_unit_assoc_dao.py",
    ],
    "billing": [
        "invoice_dao.py",
        "invoice_item_dao.py",
        "transaction_dao.py",
        "transaction_type_dao.py",
        "payment_type_dao.py",
    ],
    "contracts": ["contract_dao.py", "contract_type_dao.py", "under_contract_dao.py"],
    "auth": [
        "user_dao.py",
        "role_dao.py",
        "permission_dao.py",
        "auth_dao.py",
        "company_dao.py",
    ],
    "communication": [
        "calendar_event_dao.py",
        "message_dao.py",
        "maintenance_request_dao.py",
        "tour_booking_dao.py",
    ],
    "resources": [
        "amenities_dao.py",
        "media_dao.py",
        "utilities_dao.py",
        "base_dao.py",
    ],
}


def reverse_file_references(root_folder):
    # Create a reverse mapping of folder names to filenames
    folder_to_file = {}
    for folder, files in structure.items():
        for file in files:
            folder_to_file[file] = folder

    # Iterate through each folder and file in the root directory
    for foldername, subfolders, filenames in os.walk(root_folder):
        # Process each file in the current folder
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(foldername, filename)
                file_name_without_ext = filename[:-3]  # Remove the .py extension
                print(f"{file_name_without_ext}")

                # Determine the original folder name based on the current filename
                for file, folder in folder_to_file.items():
                    sub_file_name = file[:-3]
                    print(f"\t{sub_file_name}, {folder}")
                    # if filename.startswith(f'{folder}.'):
                    #     original_folder_name = folder
                    #     original_filename = file
                    #     break

                    # print(original_folder_name)
                    if sub_file_name:
                        try:
                            # Read the file content with error handling for encoding
                            with open(
                                file_path, "r", encoding="utf-8", errors="replace"
                            ) as file:
                                file_content = file.read()

                            # Prepare the regex pattern and replacement string
                            pattern = re.compile(
                                rf"app\.dao\.{sub_file_name}", re.IGNORECASE
                            )
                            replacement = f"app.dao.{folder}.{sub_file_name}"

                            # Replace occurrences using regex
                            updated_content = pattern.sub(replacement, file_content)
                            print(updated_content)

                            # Write the updated content back to the file
                            if updated_content != file_content:
                                with open(file_path, "w", encoding="utf-8") as file:
                                    file.write(updated_content)

                                print(f"Reversed references in {file_path}")

                        except Exception as e:
                            print(f"Failed to update {file_path}: {e}")


if __name__ == "__main__":
    # Set the root folder where the folders are created
    root_folder = os.getcwd()  # Current directory where the script is located
    reverse_file_references(root_folder)
    print("File references reversed successfully.")
