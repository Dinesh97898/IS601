import json
class Exercise3:
    def __init__(self,json_file):
        self.json_data = json.load(open(json_file,'r'))
