#StateManager with init, load_state, save_state and check_reset functions
import json
from datetime import datetime
from pathlib import Path

class StateManager:
    #Setting the default script directory and default state file path
    default_script_dir = Path(__file__).parent
    default_state_file = default_script_dir / 'state.json'

    def __init__(self, default_state_file=None):
        #If a custom state file path is provided, use it, else use the default state file path
        #Default state file is located in the same directory as the script and named 'state.json'
        if default_state_file: self.file_path = Path(default_state_file)
        else: self.file_path = self.default_state_file
        
        self.state = {
            "last_reset": datetime.now().strftime("%Y-%m-%d"),  #Today's date string via strftime
            "blocker_enabled": False, #Whether the blocker is enabled or not, default is False
            "apps": {} #Dictionary of all tracked apps and their info
        }
        self.load_state()
        

    def save_state(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.state, file)

    def load_state(self):
        try:
            with open(self.file_path, 'r') as file:
                self.state = json.load(file)
        except FileNotFoundError:
            self.save_state()  #Create the file if it doesn't exist
    
    def check_reset(self):
        #Checks today's date, matches with the last reset date in state
        today_date = datetime.now().strftime("%Y-%m-%d")

        #If last reset date differs from today's date, update last_reset and reset daily_opens counter and hold_minutes for each app in state
        if self.state["last_reset"] != today_date:
            self.state["last_reset"] = today_date
            for app in self.state["apps"]:
                self.state["apps"][app]["daily_opens"] = 0
                self.state["apps"][app]["hold_minutes"] = 1
            #Then save the updated state to the file
            self.save_state()
