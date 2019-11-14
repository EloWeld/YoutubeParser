import csv
import json
import re
import sys
import os


import requests

from pytube import YouTube

api_key = "AIzaSyCBocQMtmMDcZQNcGq6YjD0cE5dV8YLwCQ"


class Channel:
    def __init__(self):
        self.query = ''
        self.name = ''
        self.id = ''
        self.url = ''
        self.subs = 0
        self.views = 0
        self.videoCount = 0

        self.foundInQueries = []

    def __str__(self):
        s = '{:^20} | {:^15} | {:^25} | {} | {:^65} | {:>7} | {:^10} | {:^4}'.format(', '.join(self.foundInQueries), self.query, self.name[:25], self.id, self.url, self.subs,
                                                                   self.views, self.videoCount)
        return s


def SortChansBy(channels, option):
    if option == 'name':
        channels.sort(key=lambda x: x.name)
        return
    if option == 'subs':
        channels.sort(key=lambda x: x.subs)
        return
    elif option == 'views':
        channels.sort(key=lambda x: x.views)
        return
    elif option == 'videosCount':
        channels.sort(key=lambda x: x.videosCount)
        return
    elif option == 'query':
        channels.sort(key=lambda x: x.query)
        return
    elif option == 'queryInclude':
        channels.sort(key=lambda x: len(x.foundInQueries))
        return
    print("###ERROR IN SORTING CHANNELS BY " + str(option) + "!");


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


def ReadFilesInFolderToData(folder=None, delimiter=';'):
    data = []
    files = os.listdir(folder)
    print(files)
    for file in files:
        if file.split('.')[len(file.split('.')) - 1] == 'txt':
            with open(file, 'r', encoding='utf-8') as curr_file:
                for line in curr_file.readlines():
                    data.append(Channel())
                    file_data = line.split(delimiter)
                    data[len(data) - 1].query = str(file.split('.')[0])

                    data[len(data) - 1].name = str(file_data[0])
                    data[len(data) - 1].id = str(file_data[1])
                    data[len(data) - 1].url = str(file_data[2])
                    data[len(data) - 1].subs = int(file_data[3])
                    data[len(data) - 1].views = int(file_data[4])
                    data[len(data) - 1].videoCount = int(file_data[5])
    return data


def EditorMode(channels, keyword="File"):
    stop = False
    while not stop:
        print("\n\n\n\n\n\n\n\n\nOptions:")
        print("    0. Exit")
        print("    1. Out to table")
        print("    2. Sort")
        print("    3. Reverse")
        cmd = int(input())

        if cmd == '0':
            stop = True
        elif cmd == 1:
            OutToFile(str(keyword) + ".csv", channels, delimiter=';')
        elif cmd == 2:
            print("\nSort:")
            print("    0. Query")
            print("    1. Subscribes")
            print("    2. Views")
            print("    3. VideoCount")
            print("    4. QueryInclude")
            print("    5. Name")
            cmd_s = int(input())

            if cmd_s == 0:
                SortChansBy(channels, "query")
            elif cmd_s == 1:
                SortChansBy(channels, "subs")
            elif cmd_s == 2:
                SortChansBy(channels, "views")
            elif cmd_s == 3:
                SortChansBy(channels, "videosCount")
            elif cmd_s == 4:
                SortChansBy(channels, "queryInclude")
            elif cmd_s == 5:
                SortChansBy(channels, "name")
        elif cmd == 3:
            channels.reverse()

        for chan in channels:
            print(chan)


def AddChannelStatistics(data):
    for channel in data:
        for channel2 in data:
            if channel.id == channel2.id and (not channel == channel2):
                channel.foundInQueries.append(channel2.query)
                print(channel2.query)


def main():
    data = ReadFilesInFolderToData()
    AddChannelStatistics(data)
    SortChansBy(data, 'subs')
    data.reverse()

    if len(data) == 0:
        print('#ERROR: Folder is empty!')
    else:
        for channel in data:
            print(channel)

        # Run Editor
        EditorMode(data)


if __name__ == '__main__':
    main()
