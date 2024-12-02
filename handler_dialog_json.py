import json
import os

class DialogJsonHandler:
    def __init__(self):
        self.input_json_packet = None
        self.json_directory = "root/defaults/json/"
        
    def load_json_file(self, filename):
        """
        Load a JSON file from the specified directory
        Args:
            filename (str): Name of the JSON file to load
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_path = os.path.join(self.json_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                self.input_json_packet = json.load(file)
            return True
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return False