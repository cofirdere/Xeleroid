#tools.py
import subprocess
import os
import platform
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
    "discord":"discord",
    "spotify":"spotify",
    "instagram":"https://instagram.com",  #opens browser
    "insta":"https://instagram.com",      #opens browser
    "edge":"msedge",
    "brave":"brave",
    "firefox":"firefox",
    "facebook":"https://facebook.com",     #opens browser
    "fb":"https://facebook.com",           #opens browser
    "word":"word",
    "excel":"excel",
    "powerpoint":"powerpoint",
    "ppt":"powerpoint",
    "drive":"https://drive.google.com",    #opens browser
}

def getStatus()-> dict:        #status
    return {
        "status": "Active",
        "working_directory":os.getcwd(),
        "os":platform.system(),
    }

def webSearch(query: str)-> dict:
    import urllib.parse
    encodedQuery=urllib.parse.quote(query)
    webbrowser.open(f"https://www.google.com/search?q={encodedQuery}")
    return {"success": True, "message": f"searching for {query}"}
    
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
     
