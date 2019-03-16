import json
from schnitzel import messages

login_response = messages.login()

print(json.dumps(login_response, indent=4, sort_keys=True))
