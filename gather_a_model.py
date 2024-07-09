import os
import argparse

def copy_django_files_to_txt(app_folder):
    """
    This function takes the name of a Django app folder and copies the contents
    of specific Django files into a single .txt file within the same folder.

    Args:
    app_folder (str): The directory path of the Django app.

    Returns:
    str: The path to the created .txt file or an error message if unsuccessful.
    """
    # Define the files to be copied
    files_to_copy = ['admin.py', 'models.py', 'serializers.py', 'tests.py', 'urls.py', 'views.py']
    folder_name = os.path.basename(os.path.normpath(app_folder))  # Extract the folder name
    output_file_name = f"{folder_name}.txt"  # Use the folder name to create the output file name
    output_path = os.path.join(app_folder, output_file_name)

    try:
        # Open the output file in write mode
        with open(output_path, 'w') as output_file:
            # Loop through the files and copy contents
            for file_name in files_to_copy:
                file_path = os.path.join(app_folder, file_name)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as file:
                        output_file.write(f"--- Contents of {file_name} ---\n")
                        output_file.write(file.read() + "\n\n")
                else:
                    output_file.write(f"--- {file_name} not found ---\n\n")
        return f"Contents copied to {output_path}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
if __name__ == "__main__":
    # Setup command line argument parsing
    parser = argparse.ArgumentParser(description="Copy Django app files to a single text file.")
    parser.add_argument("app_folder", type=str, help="Path to the Django app folder")
    
    args = parser.parse_args()
    
    # Call the function with the command line argument
    result = copy_django_files_to_txt(args.app_folder)

# Example usage:
# result = copy_django_files_to_txt('path_to_your_django_app')
# print(result)
