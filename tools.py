#tools.py
import subprocess
import random
import os
import platform
import urllib.request
import urllib.parse
import json
#import traceback
import webbrowser
from datetime import datetime
#to check for third party apps, that users use
THIRD_PARTY_APPS= {
    "chrome":"chrome",
    "duckduckgo":"https://www.duckduckgo.com",        #opens browser
    "duck browser":"https://www.duckduckgo.com",      #opens browser
    "chatgpt":"https://www.chatgpt.com",              #opens browser
    "cgpt":"https://www.chatgpt.com",                 #opens browser
    "gemini":"https://gemini.google.com",             #opens browser
    "google gemini":"https://gemini.google.com",      #opens browser
    "gmni":"https://gemini.google.com",               #opens browser
    "claude":"https://www.claude.com",                #opens browser
    "clde":"https://www.claude.com",                  #opens browser
    "claud":"https://www.claude.com",                 #opens browser
    "snapchat":"https://www.snapchat.com",            #opens browser
    "snap":"https://www.snapchat.com",                #opens browser
    "snpp":"https://www.snapchat.com",                #opens browser
    "discord":"discord",
    "spotify":"spotify",
    "instagram":"https://instagram.com",  #opens browser
    "insta":"https://instagram.com",      #opens browser
    "edge":"msedge",
    "brave":"brave",
    "firefox":"firefox",
    "facebook":"https://facebook.com",     #opens browser
    "fb":"https://facebook.com",           #opens browser
    "word":"Word",
    "excel":"Excel",
    "powerpoint":"PowerPoint",
    "ppt":"PowerPoint",
    "drive":"https://drive.google.com",    #opens browser
}

def intDownReply():
     INTERNETdown_REPLYS= [
         "Seems like You are offline! please check your Internet connection...",
         "We are offline, Please turn on your internet",
         "Ugh ohh... Check your Internet connection",
         "hey, please turn on your Internet, so that I can search what you want!",
    ]
     return random.choice(INTERNETdown_REPLYS)

def wikipediaSearch(query: str):   
    '''It is to search in wikipedia. its the first step for actual API search. 
        So that the AI sends the wikipedia api an query to find the answer.'''
    parametersWikis=urllib.parse.urlencode({
        "action":"query",
        "list":"search",
        "srsearch":query,
        "format":"json",
        "utf8":1,
        "srlimit":6
    })
    Wikiurl=f"https://en.wikipedia.org/w/api.php?{parametersWikis}"
    
    try:
        apiId=urllib.request.Request(Wikiurl, headers={"User-Agent": "Xeleroid/1.0 (system terminal assistant)"})

        with urllib.request.urlopen(apiId, timeout=5) as response:
            Wdata=json.loads(response.read().decode("utf-8"))

            wikiResponse=Wdata["query"]["search"]
            #print(Wdata)
            firstResponse=wikiResponse[0]
            Title_of_firstResp=firstResponse["title"]

        if not wikiResponse:
            return {
                "success": False,
                "message":"sorry, I couldn't find anything relevant on Internet."
            }
        return {
               "success": True,
               "results":wikiResponse
        }
    except Exception as e:
        #traceback.print_exc()
        return {
              "success": False,
              "message":f"Search failed {e}"
        }

def wikipediaSummary(title: str) ->dict:
      '''It is used to return the summary of wiki's infos. so that, 
      it gives the infos to another function "wikiAns" for further processing.'''
      encodedData=urllib.parse.quote(title.replace(" ","_"))
      sumUrl=(f"https://en.wikipedia.org/api/rest_v1/page/summary/{encodedData}")
      try:
          apiId=urllib.request.Request(sumUrl, headers={"User-Agent": "Xeleroid/1.0 (system terminal assistant)"})

          with urllib.request.urlopen(apiId, timeout=4) as response:
              data=json.loads(response.read().decode("utf-8"))
          return {
                "success":True,
                "title":data["title"],
                "extract":data["extract"]
            }
      except Exception as e:
          return {
              "success":False,
              "message":f"couldn't get relevant informations or search failed {e}"
          }

def wikiAns(query: str) ->dict:
    '''It is the function for the processing for infos at wikipedia. 
    It uses the "wikipediaSearch" and "wikipediaSummary" for searching and processing the infos to user'''
    wikisearch=wikipediaSearch(query)
    if not wikisearch["success"]:
        return wikisearch
    wikiresult=wikisearch["results"]
    if not wikiresult:
        return {
            "success": False,
            "message":"couldn't get relevant informations or search failed. source is wikipedia"
        }
    firstResult=wikiresult[0]
    nameOfFirstres=firstResult["title"]
    summary=wikipediaSummary(nameOfFirstres)
    if not summary["success"]:
        return summary
    return {
        "success":True,
        "title":summary["title"],
        "answer":summary["extract"]
    }

def getStatus()-> dict:        #status
    return {
        "status": "Active",
        "working_directory":os.getcwd(),
        "os":platform.system(),
    }

def internetAvailable():  #to check if there is internet connection, so that the user wont see blank page on their browser.
    try:
       urllib.request.urlopen("https://www.google.com", timeout=2)
       return True
    except:
        return False    

def webSearch(query: str)-> dict:
    '''the "query" is just a variable. you can change them accordingly, '''
    if not internetAvailable():
          return {
              "success": False,
              "message":intDownReply()
          }
    else:
        encodedQuery=urllib.parse.quote(query)
        webbrowser.open(f"https://www.google.com/search?q={encodedQuery}")
        return {
            "success": True, 
            "message": f"searching for {query}" 
        }
    
def getTime()->dict:        #time
    timeNow=datetime.now()
    formatted=timeNow.strftime("%I: %M %p and %A %b %d")
    return{"success":True, "time": formatted, "message": f"It is {formatted} now"}

def openFolder(path: str)-> dict:                                                      #<==folder
    expandedPath=os.path.expanduser(path)#to get the raw path from os 
    if not os.path.exists(expandedPath):  #if file is not found
        return{"success": False, "message": f"the file is not found {expandedPath}"}
    system=platform.system()
    try: 
       if system=="Windows":                 #windows
           os.startfile(expandedPath)
       elif system=="Darwin":                     #macOS
             subprocess.Popen(["open", expandedPath])
       else:                                         #linux
           subprocess.Popen(["xdg-open", expandedPath])
       return{"success": True, "message": f"opening {expandedPath}"}
    except Exception as e:
            return{"success": False, "message": str(e)}
    
def openApp(appName: str)->dict:          #app
     systemApp=platform.system()
     clean_name=appName.strip().lower()
     '''it is used for this; the two arguments at the below line () is used for [getting the app if it's a third party app]
     or [is this even third party app at all?] if not, then it goes to the second argument of same name as a default fallacy.
     '''
     appTarget= THIRD_PARTY_APPS.get(clean_name, clean_name)

     if appTarget.startswith("http"):
         webbrowser.open(appTarget)
         return{"success": True, "message": f"opening {appTarget} for you"}
     
     try:
        if systemApp=="Windows": #windows
            '''this ['start "" "{appTarget}"'] has a specific quirk in windows cmd. if you write it normally, 
            the windows cmd opens a new window, but it didn't open your actual app! 
            by wrapping this into quotes[the "" in the middle is to tell windows cmd that its empty window,then the app comes after], 
            the windows treats it as a whole one file path.'''
            subprocess.Popen(f'start "" "{appTarget}"', shell=True)
        elif systemApp=="Darwin":  #macOS
             subprocess.Popen(["open", "-a", appTarget])
        else:
            subprocess.Popen([appTarget])
        return{"success": True, "message": f"launching {clean_name}"}
     except Exception as r:
         return{"success": False, "message": str(r)}
     
