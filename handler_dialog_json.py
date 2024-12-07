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

    def get_dialog_step(self, input_step):
        """
        Get dialog data for a specific step
        Args:
            input_step (int): Step number to retrieve
        Returns:
            dict: Dictionary containing dialog data (speaker, d, sprite_bkg, sprite_left, sprite_right)
                  or None if step not found
        """
        if self.input_json_packet is None:
            print("No JSON file loaded")
            return None
            
        step_key = str(input_step)  # Convert step number to string for JSON lookup
        if step_key not in self.input_json_packet:
            print(f"Step {input_step} not found in dialog")
            return None
            
        step_data = self.input_json_packet[step_key]
        # Verify all required fields are present
        required_fields = ["speaker", "d", "sprite_bkg", "sprite_left", "sprite_right"]
        if not all(field in step_data for field in required_fields):
            print(f"Step {input_step} is missing required fields")
            return None
            
        return {
            "speaker": step_data["speaker"],
            "d": step_data["d"],
            "sprite_bkg": step_data["sprite_bkg"],
            "sprite_left": step_data["sprite_left"],
            "sprite_right": step_data["sprite_right"]
        }