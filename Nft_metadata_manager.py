import json
import os
import re # For basic input validation

# --- Configuration ---
METADATA_DIR = "metadata_files"

# Ensure the metadata directory exists
if not os.path.exists(METADATA_DIR):
    os.makedirs(METADATA_DIR)
    print(f"Created metadata directory: {METADATA_DIR}")

# --- Helper Functions ---

def get_file_path(token_id):
    """Constructs the full file path for a given token ID."""
    return os.path.join(METADATA_DIR, f"{token_id}.json")

def load_metadata(token_id):
    """Loads and returns metadata from a JSON file."""
    file_path = get_file_path(token_id)
    if not os.path.exists(file_path):
        print(f"Error: Metadata file for Token ID {token_id} not found.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            print(f"Metadata for Token ID {token_id} loaded successfully.")
            return metadata
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file {file_path}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading: {e}")
        return None

def save_metadata(token_id, metadata):
    """Saves metadata to a JSON file."""
    file_path = get_file_path(token_id)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)
        print(f"Metadata for Token ID {token_id} saved successfully to {file_path}.")
        return True
    except Exception as e:
        print(f"Error saving metadata to {file_path}: {e}")
        return False

def display_metadata(metadata):
    """Prints metadata in a readable format."""
    if not metadata:
        print("No metadata to display.")
        return

    print("\n--- NFT Metadata Details ---")
    print(f"Name: {metadata.get('name', 'N/A')}")
    print(f"Description: {metadata.get('description', 'N/A')}")
    print(f"Image URI: {metadata.get('image', 'N/A')}")
    if 'external_url' in metadata:
        print(f"External URL: {metadata['external_url']}")
    if 'background_color' in metadata:
        print(f"Background Color: {metadata['background_color']}")

    attributes = metadata.get('attributes', [])
    if attributes:
        print("\nAttributes:")
        for attr in attributes:
            print(f"  - {attr.get('trait_type', 'N/A')}: {attr.get('value', 'N/A')}")
    else:
        print("\nNo attributes defined.")
    print("---------------------------\n")

# --- Core Manager Functions ---

def create_new_metadata():
    """Prompts user for details to create a new metadata file."""
    print("\n--- Create New NFT Metadata ---")
    
    while True:
        token_id_str = input("Enter Token ID (e.g., 1, 2, 100): ").strip()
        if token_id_str.isdigit():
            token_id = int(token_id_str)
            if os.path.exists(get_file_path(token_id)):
                print(f"Error: Metadata file for Token ID {token_id} already exists. Please choose a different ID or edit the existing file.")
            else:
                break
        else:
            print("Invalid Token ID. Please enter a positive integer.")

    name = input("Enter NFT Name: ").strip()
    description = input("Enter NFT Description: ").strip()
    image_uri = input("Enter Image URI (e.g., ipfs://Qm...): ").strip()
    external_url = input("Enter External URL (optional): ").strip() or None
    background_color = input("Enter Background Color (optional, e.g., FFC0CB): ").strip() or None

    metadata = {
        "name": name,
        "description": description,
        "image": image_uri,
        "attributes": []
    }
    if external_url:
        metadata["external_url"] = external_url
    if background_color:
        metadata["background_color"] = background_color

    print("\nNow, let's add some attributes. Type 'done' when finished.")
    while True:
        trait_type = input("Enter Trait Type (e.g., 'Hat', 'Eyes') or 'done': ").strip()
        if trait_type.lower() == 'done':
            break
        value = input(f"Enter Value for '{trait_type}': ").strip()
        metadata["attributes"].append({"trait_type": trait_type, "value": value})
        print(f"Attribute '{trait_type}: {value}' added.")

    if save_metadata(token_id, metadata):
        print(f"NFT metadata for Token ID {token_id} created successfully.")
    else:
        print(f"Failed to create metadata for Token ID {token_id}.")

def edit_existing_metadata():
    """Allows editing of an existing metadata file."""
    print("\n--- Edit NFT Metadata ---")
    while True:
        token_id_str = input("Enter Token ID of the file to edit: ").strip()
        if token_id_str.isdigit():
            token_id = int(token_id_str)
            break
        else:
            print("Invalid Token ID. Please enter a positive integer.")

    metadata = load_metadata(token_id)
    if not metadata:
        return

    display_metadata(metadata)

    while True:
        print("\nWhat do you want to edit?")
        print("1. Name")
        print("2. Description")
        print("3. Image URI")
        print("4. External URL")
        print("5. Background Color")
        print("6. Manage Attributes")
        print("7. Done Editing (Save Changes)")
        
        edit_choice = input("Enter your choice: ").strip()

        if edit_choice == '1':
            new_name = input(f"Enter new Name (current: {metadata.get('name')}): ").strip()
            if new_name:
                metadata['name'] = new_name
                print("Name updated.")
        elif edit_choice == '2':
            new_desc = input(f"Enter new Description (current: {metadata.get('description')}): ").strip()
            if new_desc:
                metadata['description'] = new_desc
                print("Description updated.")
        elif edit_choice == '3':
            new_image = input(f"Enter new Image URI (current: {metadata.get('image')}): ").strip()
            if new_image:
                metadata['image'] = new_image
                print("Image URI updated.")
        elif edit_choice == '4':
            new_external_url = input(f"Enter new External URL (current: {metadata.get('external_url')}): ").strip()
            metadata['external_url'] = new_external_url if new_external_url else None
            print("External URL updated.")
        elif edit_choice == '5':
            new_bg_color = input(f"Enter new Background Color (current: {metadata.get('background_color')}): ").strip()
            metadata['background_color'] = new_bg_color if new_bg_color else None
            print("Background Color updated.")
        elif edit_choice == '6':
            manage_attributes_menu(metadata)
        elif edit_choice == '7':
            if save_metadata(token_id, metadata):
                print("Changes saved.")
            else:
                print("Failed to save changes.")
            break
        else:
            print("Invalid choice. Please try again.")
        
        display_metadata(metadata) # Show current state after each edit

def manage_attributes_menu(metadata):
    """Sub-menu for managing NFT attributes."""
    if 'attributes' not in metadata or not isinstance(metadata['attributes'], list):
        metadata['attributes'] = [] # Initialize if missing or wrong type

    while True:
        print("\n--- Manage Attributes ---")
        display_metadata(metadata) # Show current attributes
        print("1. Add New Attribute")
        print("2. Edit Existing Attribute")
        print("3. Remove Attribute")
        print("4. Back to Main Edit Menu")
        
        attr_choice = input("Enter your choice: ").strip()

        if attr_choice == '1':
            trait_type = input("Enter new Trait Type: ").strip()
            value = input(f"Enter Value for '{trait_type}': ").strip()
            found = False
            for attr in metadata['attributes']:
                if attr.get('trait_type', '').lower() == trait_type.lower():
                    attr['value'] = value
                    print(f"Attribute '{trait_type}' updated to '{value}'.")
                    found = True
                    break
            if not found:
                metadata['attributes'].append({"trait_type": trait_type, "value": value})
                print(f"Attribute '{trait_type}: {value}' added.")

        elif attr_choice == '2':
            trait_type_to_edit = input("Enter Trait Type to edit: ").strip()
            found = False
            for attr in metadata['attributes']:
                if attr.get('trait_type', '').lower() == trait_type_to_edit.lower():
                    new_value = input(f"Enter new Value for '{attr['trait_type']}' (current: {attr['value']}): ").strip()
                    if new_value:
                        attr['value'] = new_value
                        print(f"Attribute '{attr['trait_type']}' updated to '{new_value}'.")
                    found = True
                    break
            if not found:
                print(f"Attribute '{trait_type_to_edit}' not found.")
        
        elif attr_choice == '3':
            trait_type_to_remove = input("Enter Trait Type to remove: ").strip()
            initial_len = len(metadata['attributes'])
            metadata['attributes'] = [
                attr for attr in metadata['attributes']
                if attr.get('trait_type', '').lower() != trait_type_to_remove.lower()
            ]
            if len(metadata['attributes']) < initial_len:
                print(f"Attribute '{trait_type_to_remove}' removed.")
            else:
                print(f"Attribute '{trait_type_to_remove}' not found.")
        
        elif attr_choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def view_metadata():
    """Loads and displays metadata for a given Token ID."""
    print("\n--- View NFT Metadata ---")
    while True:
        token_id_str = input("Enter Token ID to view: ").strip()
        if token_id_str.isdigit():
            token_id = int(token_id_str)
            break
        else:
            print("Invalid Token ID. Please enter a positive integer.")

    metadata = load_metadata(token_id)
    if metadata:
        display_metadata(metadata)

def batch_generate_metadata():
    """Generates multiple metadata files for a collection."""
    print("\n--- Batch Generate NFT Metadata ---")
    while True:
        try:
            start_id = int(input("Enter starting Token ID (e.g., 1): ").strip())
            end_id = int(input("Enter ending Token ID (e.g., 100): ").strip())
            if start_id <= 0 or end_id <= 0 or start_id > end_id:
                print("Invalid ID range. Start ID must be positive and less than or equal to End ID.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter integers for Token IDs.")
    
    base_name = input("Enter base name (e.g., 'My Collection #'): ").strip()
    base_description = input("Enter base description: ").strip()
    base_image_uri = input("Enter base Image URI (e.g., 'ipfs://QmWxyz/'): ").strip()
    external_url = input("Enter External URL (optional, applied to all): ").strip() or None
    background_color = input("Enter Background Color (optional, applied to all, e.g., FFC0CB): ").strip() or None

    print("\nNow, let's add common attributes for all NFTs. Type 'done' when finished.")
    common_attributes = []
    while True:
        trait_type = input("Enter common Trait Type (e.g., 'Background', 'Rarity') or 'done': ").strip()
        if trait_type.lower() == 'done':
            break
        value = input(f"Enter common Value for '{trait_type}': ").strip()
        common_attributes.append({"trait_type": trait_type, "value": value})
        print(f"Common attribute '{trait_type}: {value}' added.")

    print(f"\nGenerating metadata for {end_id - start_id + 1} NFTs...")
    generated_count = 0
    for i in range(start_id, end_id + 1):
        # Create a copy of common attributes for each NFT
        current_attributes = list(common_attributes) 
        
        # You can add logic here to customize attributes per NFT if needed
        # For example, randomize some attributes or load from a CSV for unique traits
        # For simplicity, this example just uses common attributes + adds a numerical trait
        current_attributes.append({"trait_type": "Number", "value": str(i)})

        metadata = {
            "name": f"{base_name}{i}",
            "description": base_description,
            "image": f"{base_image_uri}{i}.png", # Assuming image names are sequential
            "attributes": current_attributes
        }
        if external_url:
            metadata["external_url"] = external_url
        if background_color:
            metadata["background_color"] = background_color

        if save_metadata(i, metadata):
            generated_count += 1
        else:
            print(f"Skipped Token ID {i} due to error.") # Error already printed by save_metadata

    print(f"\nBatch generation complete. Successfully generated {generated_count} files.")


# --- Main Application Loop ---

def display_main_menu():
    """Displays the main menu options."""
    print("\n--- NFT Metadata Manager ---")
    print("1. Create New NFT Metadata")
    print("2. Edit Existing NFT Metadata")
    print("3. View NFT Metadata")
    print("4. Batch Generate Metadata (for collections)")
    print("5. Exit")
    print("----------------------------")

def main():
    while True:
        display_main_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            create_new_metadata()
        elif choice == '2':
            edit_existing_metadata()
        elif choice == '3':
            view_metadata()
        elif choice == '4':
            batch_generate_metadata()
        elif choice == '5':
            print("Exiting NFT Metadata Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        time.sleep(0.5) # Short pause for readability in console

if __name__ == "__main__":
    import time # Import time here for sleep function
    main()