import json
from schnitzel import messages

# Client login
login_response = messages.login()

# Begin hand


print(json.dumps(login_response, indent=4, sort_keys=True))
