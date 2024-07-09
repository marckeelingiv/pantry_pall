import os

def gather_models(django_project_path, output_file_path):
    models_content = []

    # Traverse the Django project directory
    for root, dirs, files in os.walk(django_project_path):
        # Skip .venv directory
        if '.venv' in root:
            continue
        
        if 'models.py' in files:
            models_file_path = os.path.join(root, 'models.py')
            with open(models_file_path, 'r', encoding='utf-8') as file:
                # Add the name of the models.py file to the content list
                models_content.append(f"# {models_file_path}")
                # Add the content of the models.py file to the content list
                models_content.append(file.read())

    # Write the gathered content to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for content in models_content:
            output_file.write(content)
            output_file.write('\n\n')  # Separate each models.py content with a blank line

if __name__ == "__main__":
    # set django_project_path to the current directory
    django_project_path = os.getcwd()
    output_file_path = 'all_models.txt'  # The output file where all models.py content will be written
    gather_models(django_project_path, output_file_path)
    print(f"All models.py content has been gathered into {output_file_path}")
