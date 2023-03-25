import os

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