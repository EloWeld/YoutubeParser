import json
import sys

import requests

api_key = "AIzaSyDOD-2-tJ6e0XCSXOOAkzTnNaxsOCoxb2Y"

class YouTubeData:
    def __init__(self):
        self.data = None
        self.nextPageToken = None
        self.json_url = None

    def append_data(self, url):
        self.json_url = requests.get(url)

        try:
            aaa = json.loads(self.json_url.text)["items"]
        except KeyError:
            print("\n####ERROR: " + json.loads(self.json_url.text)["error"]["message"])
            sys.exit()

        if not self.data:
            self.data = json.loads(self.json_url.text)
        else:
            tmp = json.loads(self.json_url.text)
            self.data["items"] += tmp["items"]
            self.data["nextPageToken"] = tmp["nextPageToken"]

        self.nextPageToken = self.data["nextPageToken"]

        print("Next page token: " + self.nextPageToken)

    def print_data(self):
        print("Search data in json: " + str(self.data))


class YouTubeChannel:
    def __init__(self, item):

        self.data = item
        self.name = self.data["snippet"]["title"]
        self.id = self.data["snippet"]["channelId"]
        self.url = "https://www.youtube.com/channel/" + self.id

        """
        self.json_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.id}&key={api_key}"

        self.json_get = requests.get(self.json_url).text

        try:
            self.statistics = json.loads(self.json_get)["items"][0]["statistics"]
        except KeyError:
            print("\n####ERROR: " + json.loads(self.json_get)["error"]["message"])
            sys.exit()
        
        self.videosCount = int(self.statistics["videoCount"])
        self.subs = int(self.statistics["subscriberCount"])
        self.views = int(self.statistics["viewCount"])
        """
        self.videosCount = 0
        self.subs = 0
        self.views = 0

    def __str__(self):
        s = '{:^25} | {} | {:^65} | {:^4} | {:>7} | {:^10}'.format(self.name[:25], self.id, self.url, self.videosCount,
                                                                   self.subs, self.views)
        return s


def SortChansBy(channels, option):
    if option == 'subs':
        channels.sort(key=lambda x: x.subs)
        return
    elif option == 'views':
        channels.sort(key=lambda x: x.views)
        return
    elif option == 'videosCount':
        channels.sort(key=lambda x: x.videosCount)
        return
    print("###ERROR IN SORTING CHANNELS BY " + str(option) + "!");


def EditorMode(channels, keyword="File"):
    stop = False
    while not stop:
        print("Options:")
        print("    0. Exit")
        print("    1. Out to table")
        print("    2. Sort by VideoCount")
        print("    3. Sort by Subs")
        print("    4. Sort by Views")
        print("    5. Reverse")
        cmd = int(input())

        if cmd == '0':
            OutToFile(keyword + ".txt", channels, delimiter=';')
            stop = True
        elif cmd == 1:
            OutToFile(str(keyword) + ".csv", channels, delimiter=';')
        elif cmd == 2:
            SortChansBy(channels, "videosCount")
            print("SORTED")
        elif cmd == 3:
            SortChansBy(channels, "subs")
        elif cmd == 4:
            SortChansBy(channels, "views")
        elif cmd == 5:
            channels.reverse()

        for chan in channels:
            print(chan)


def OutToFile(file, channels, delimiter=';', end='\n'):
    with open(file, 'wb') as file:
        for channel in channels:
            file.write((channel.name + delimiter).encode('utf-8'))
            file.write((channel.id + delimiter).encode('utf-8'))
            file.write((channel.url + delimiter).encode('utf-8'))
            file.write((str(channel.subs) + delimiter).encode('utf-8'))
            file.write((str(channel.views) + delimiter).encode('utf-8'))
            file.write((str(channel.videosCount) + delimiter).encode('utf-8'))
            file.write(end.encode('utf-8'))


def main():
    # Init
    pass

    # Input
    keywords = []
    with open("keywords.ini", 'r', encoding='utf-8') as file:
        keywords = file.readlines()
        keywords = [x.strip() for x in keywords]
    print (keywords)
    maxResults = int(input('Enter MaxResults(EnterToSkip): '))
    if not maxResults:
        maxResults = 10
    regionCode = input('Enter RegionCode(EnterToSkip): ')

    # API
    for keyword in keywords:
        yData = YouTubeData()
        print("{:=^70}".format("CURRENT KEYWORD: " + keyword[:20]))
        for page in range(1 + (maxResults // 51)):
            pageToken = yData.nextPageToken
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&key={api_key}"
            url += f"&q={keyword}"
            url += f"&maxResults={maxResults % 51 if page == maxResults // 51 else 50}" if maxResults else ""
            url += f"&maxResults={regionCode}" if regionCode else ""
            url += f"&pageToken={pageToken}" if pageToken else ""
            yData.append_data(url)
        yData.print_data()

        channels = [YouTubeChannel(item) for item in yData.data["items"]]
        for chan in channels:
            print(chan)

        # After Searching do that▼
        SortChansBy(channels, "videosCount")
        OutToFile(keyword + ".txt", channels)

    # Run Editor if it needs
    EditorMode(channels, keyword)


if __name__ == '__main__':
    main()
