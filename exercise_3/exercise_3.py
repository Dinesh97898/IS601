import json
class Exercise3:
    def __init__(self,json_file):
        self.json_data = json.load(open(json_file,'r'))

    def get_username(self):
        return self.json_data['username']
    
    def get_time_remaining(self):
        return self.json_data['time_remaining']
    
    def add_hour(self):
        self.json_data['time_remaining'] += 60
