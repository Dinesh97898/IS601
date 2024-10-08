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

    def get_items(self):
        return list(self.json_data['shopping_cart'].keys())

    def get_total(self):
        return sum(self.json_data['shopping_cart'].values())
