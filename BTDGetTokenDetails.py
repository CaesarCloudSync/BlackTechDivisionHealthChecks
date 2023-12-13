import json
import requests
class BTDGetTokenDetails:
    def __init__(self):
        with open("lead_event_req.json") as f:
            self.lead_event_req = json.load(f)
    def get_token_details(self):
        resp = requests.get("https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app/v1/getscoreboard")
        users = {}
        for user in resp.json().get("scoreboard"):
            if "test.token@gmail.com" == user["email"]:
                users.update(user)
                break
        if len(users) == 0:
            users = {'email': 'test.token@gmail.com', 'reward': 0}
        return users