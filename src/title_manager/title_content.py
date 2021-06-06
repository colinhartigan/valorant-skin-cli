import requests

class Title_Content:

    @staticmethod
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod 
    def fetch_title_by_name(name):
        titles = Title_Content.fetch(endpoint="/playertitles")["data"]

        for title in titles:
            if name in title['displayName'].lower():
                return title
        return None

    @staticmethod 
    def fetch_all_titles():
        titles = Title_Content.fetch(endpoint="/playertitles")["data"]
        return titles