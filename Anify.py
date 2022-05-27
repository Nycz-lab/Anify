import requests
import os
import time
import json

class wallhavenapi:

    wapiJson = {}


    #search for images based on criteria defined in parameters
    def search(self, sorting="toplist", categories=None, tags=None, purity=None, apikey=None, resolution='1920x1080'):
        baseUrl = 'https://wallhaven.cc/api/v1/search/?sorting=toplist'

        if categories:
            baseUrl += f"&categories={categories}"

        if tags:
            baseUrl += f"&q={tags}"

        if purity:
            baseUrl += f"&purity={purity}"

        if apikey:
            baseUrl += f"&apikey={apikey}"

        baseUrl += f"&sorting={sorting}"    #relevance/toplist/views

        baseUrl += f"&atleast={resolution}"


        print(baseUrl)

        r = requests.get(baseUrl)
        print(r.status_code)
        
        self.wapiJson = r.json()
    
    #iterate through search results and download pictures
    def downloadWallpapers(self, limit=10):

        if not self.wapiJson:
            print("Error no search results found")
            return

        if not os.path.exists('wallpapers'):
            os.makedirs('wallpapers')

        for i in range(0, limit):
            if i >= len(self.wapiJson['data']):
                break
            wallpaper = self.wapiJson['data'][i]
            

            download = requests.get(wallpaper['path'])
            with open(f"wallpapers/{wallpaper['id']}", "wb") as image:
                image.write(download.content)

    #generate category code based on strings
    def setCategories(self, *arg):

        anime = False
        general = False
        people = False

        if "anime" in arg:
            anime = True
        if "general" in arg:
            general = True
        if "people" in arg:
            people = True

        return f"{int(general)}{int(anime)}{int(people)}"

    def setPurity(self, *arg):

        sfw = False
        sketchy = False
        nsfw = False

        if "sfw" in arg:
            sfw = True
        if "sketchy" in arg:
            sketchy = True
        if "nsfw" in arg:
            print("WARNING: Keep in mind that you must have a api key for this")
            nsfw = True

        return f"{int(sfw)}{int(sketchy)}{int(nsfw)}"

    def setBackgroundCycle(self):
        while True:
            for file in os.listdir('wallpapers'):
                print(f"Now displaying {file}")

                #Gnome
                os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri {os.path.dirname(os.path.abspath(__file__))}/wallpapers/{file}")
                time.sleep(10)






if __name__ == '__main__':
    wapi = wallhavenapi()
    wapi.search()
    wapi.downloadWallpapers()
    wapi.setBackgroundCycle()


