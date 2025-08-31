# Shows all consoles

import myrient

API = myrient.MyrientAPI()
consoles = API.get_folders("/files/Redump")

for item in consoles.items():
    print(item[0] + " : " + item[1])