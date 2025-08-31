import requests
from bs4 import BeautifulSoup

class MyrientAPI:
    def __init__(self):
        self.myrient_root = "https://myrient.erista.me/"

    def _fetch_table(self, uri: str): # Do not use this
        if uri.startswith("/"):
            uri = uri[1:]
        if not uri.endswith("/"):
            uri += "/"

        response = requests.get(self.myrient_root + uri, allow_redirects=False)
        soup = BeautifulSoup(response.text, features="lxml")
        table = soup.find("table")
        return table, uri

    # e.g. get_folders("/files/Redump/")
    def get_folders(self, myrient_uri: str, debug_log=False) -> dict:
        table, myrient_uri = self._fetch_table(myrient_uri)
        if not table:
            if debug_log:
                print("(DEBUG) get_folders() : No table found.")
            return {}

        folders = {}
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue

            td_link, td_size = tds[0], tds[1]
            a = td_link.find("a")
            if not a or a.get("href") == "../":
                continue

            if td_size.get_text().strip() == "-":
                folder_name = a.get_text().strip()
                folder_href = a.get("href")
                if folder_href.startswith("/"):
                    folder_href = folder_href[1:]
                folder_href = self.myrient_root + myrient_uri + folder_href

                folders[folder_name] = folder_href
                if debug_log:
                    print(f"(DEBUG) get_folders() : {folder_name} -> {folder_href}")

        return folders

    # e.g. get_files("/files/Redump/Sony%20-%20PlayStation/")
    def get_files(self, myrient_uri: str, debug_log=False) -> dict:
        table, myrient_uri = self._fetch_table(myrient_uri)
        if not table:
            if debug_log:
                print("(DEBUG) get_files() : No table found.")
            return {}

        files = {}
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue

            td_link, td_size = tds[0], tds[1]
            a = td_link.find("a")
            if not a or a.get("href") == "../":
                continue

            if td_size.get_text().strip() != "-":
                file_name = a.get_text().strip()
                file_href = a.get("href")
                if file_href.startswith("/"):
                    file_href = file_href[1:]
                file_href = self.myrient_root + myrient_uri + file_href

                files[file_name] = {
                    "download_link": file_href, # This download link wont change
                    "size": td_size.get_text().strip()
                }
                if debug_log:
                    print(f"(DEBUG) get_files() : {file_name} -> {file_href}")

        return files


if __name__ == '__main__':
    import sys
    print(sys.argv[0] + " cant run standalone.")