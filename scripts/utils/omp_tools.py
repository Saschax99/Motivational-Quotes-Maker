import os
import json
import secrets
import string

encoding = 'utf-8'

class OsTools:
    @staticmethod
    def get_folder_count(path: str, extensions: str = None) -> int:
        """Get the number of files in a folder with optional extensions."""
        list_dir = os.listdir(path)
        if extensions:
            count = sum(1 for file in list_dir if file.endswith(extensions))
        else:
            count = len(list_dir)
        return count

    @staticmethod
    def select_specific_object_from_folder(path: str, index: int) -> str:
        """Select a specific file from a folder by its index."""
        return os.listdir(path)[index]
    
    @staticmethod
    def write_file(data, path):
        """Write data into a file e. g. json object to a file"""
        with open(path, "a", encoding=encoding) as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
            outfile.write(",\n")
            
    @staticmethod
    def read_file(file_path):
        """read file in path and return data"""
        print(file_path)
        print(os.path.abspath(file_path))
        with open(os.path.abspath(file_path), "r", encoding=encoding) as infile:
            data = json.load(infile)
            return data
        
    @staticmethod
    def generate_id(id_length):
        # Define the pool of characters to choose from
        characters = string.ascii_letters + string.digits
        # Generate the secure random ID
        random_id = ''.join(secrets.choice(characters) for i in range(id_length))
        return random_id
    
    @staticmethod
    def delete_unreadable_characters(string, chars):
        """
        Removes all characters in the string 'chars' from the string 's'
        """
        for char in chars:
            if char in string:
                if char == ";":
                    string = string.replace(char, ",")
                else:
                    string = string.replace(char, "")
        return string
    
    @staticmethod
    def delete_files(*files_path):
        for file_path in files_path:
            try:
                os.remove(file_path)
            except PermissionError:
                print(f"cant delete {file_path}, going to skip this one")

    @staticmethod
    def remove_first_element_in_file(file_path):
        with open(os.path.abspath(file_path), "r", encoding=encoding) as infile:
            data = json.load(infile)
            del data[0]
        
        with open(os.path.abspath(file_path), "r", encoding=encoding) as infile:
            json.dump(data, infile, ensure_ascii=False, indent=4)