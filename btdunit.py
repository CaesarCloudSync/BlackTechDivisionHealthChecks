import re
import json
import unittest
import requests
from CaesarAICronEmail.CaesarAIEmail import CaesarAIEmail
from BTDGetTokenDetails import BTDGetTokenDetails
btdtokendets = BTDGetTokenDetails()
class BTDTokensUnittest(unittest.TestCase):
    def test_kartra_events(self):
        user = btdtokendets.get_token_details()
        lead_event_req = btdtokendets.lead_event_req
        resp = requests.post("https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app/v1/rewardlead?leadaction=attendedonlineevent&reward=10&api_key=fPvimQSo&api_pass=xfdgUTCcYEqD",json=lead_event_req)
        print(resp.json())
        self.assertNotEqual(resp.json().get("message"),None)

        user_after = btdtokendets.get_token_details()
        greater_than  = user_after["reward"] > user["reward"]
        self.assertEqual(greater_than,True)
