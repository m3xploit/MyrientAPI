# Shows all psx roms

import myrient

API = myrient.MyrientAPI()
roms = API.get_files("/files/Redump/Sony - PlayStation/")

for item in roms.items():
    print(item[1]["size"] + " - " + item[0])

    # Download link is in item[1]["download_link"]