import base64
import os

def save_base64_image(base64_string, filename):
    try:
        binary_data = base64.b64decode(base64_string)

        uploads_folder = 'uploads'
        file_path = os.path.join(uploads_folder, filename)

        with open(file_path, 'wb') as image_file:
            image_file.write(binary_data)
        
        return True

    except Exception as e:
        return e
    
def delete_image_from_uploads(filename):
    uploads_folder = 'uploads'
    file_path = os.path.join(uploads_folder, filename)

    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print('image deleted from uploads folder')
        return True
    else:
        print(f"File '{filename}' not found in the 'uploads' folder.")

def check_image_exist(filename):
    uploads_folder = 'uploads'
    file_path = os.path.join(uploads_folder, filename)

    if os.path.exists(file_path):
        print('image exists in folder')
    else:
        print('image not found in folder')