import requests
#sends http requests in python

API_key='AIzaSyDCyBRraltNgd93Ve22JYwGRG7wLlyD86A'
url = "https://www.googleapis.com/youtube/v3/search?key={API_key}&q=barbie trailer&type=video&part=snippet&videoId=pBk4NYhWNMM"

class Trailer:
    def __init__(self, MovieName: str = 'Barbie trailer'):
        self.TrailerData = {}
        self.fetch(MovieName)

    def getVidId(self):
        try:
                data = self.TrailerData["items"][0]["id"]["videoId"]
                return str(data)
        except (KeyError, IndexError):
            return None

    def getThumbnail(self):
          try:
                data = self.TrailerData["items"][0]["snippet"]["thumbnails"]["default"]["url"]
                return str(data)
          except (KeyError, IndexError):
                return None

    def fetch(self, MovieName):
            url = f"https://www.googleapis.com/youtube/v3/search" + \
            f"?key={API_key}&q={MovieName} trailer&aqi=no"
            response = requests.get(url)
            self.TrailerData = response.json()




# Create an instance of the Trailer class
'''moviet = Trailer("Finding nemo")

# Call the getVidId method
vid_id = moviet.getVidId()

print(vid_id)  # Print the video I'''