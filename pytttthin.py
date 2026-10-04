#main.py
import random
from brain import handle_iterate
import tools as tl
#ansii code schemes
YELLOW="\033[33m"
RESET = "\033[0m"
logoBANNER=f"""{YELLOW}
       __
  __  / /_____ _   ___________  
  \ \/ / ___ | |   | ____|  _ \ 
   \  /| ___ | |   |  __ | |_) |
   /  \| \___| |___|  ___|  _ < 
  /_/\_\_____| ____|_____|_| \_\

 
 {RESET}"""
print(logoBANNER)

def greeter()-> str:
    greetingWords=[
        "Hi, I am Xeler",
        "Xeler here",
        "Ready when you are!",     #woah
        "What should we work on?",
        "How can I help you?"
    ]
    return random.choice(greetingWords)        
print(greeter())
def handleProcess(UserInput: str):
       result=handle_iterate(UserInput)
       actions=result["actions"]
       targets=result["target"]
       match actions:
            case "get_status":
                 statusResult=tl.getStatus()
                 if statusResult["status"]:
                      print(f"I am {statusResult['status']}, and we are on {statusResult['os']}!")
            case "get_time":
                 timeResult=tl.getTime()
                 if timeResult["success"]:
                      print(timeResult['message'])
                 else:
                     print(f"sorry, can't tell the time!")
            case "open_folder":
                 #folderResult=tl.openFolder(targets)
                 print(tl.openFolder(targets))
            case "open_app":
                 #this, to get the function at tools.
                 appResult=tl.openApp(targets)
                 if appResult["success"]:
                      print(appResult["message"])
                 else:
                      print(f"ugh? seems like it couldn't open! [{appResult['message']}]")
            case "web_search":
                 searchResult=tl.webSearch(targets)
                 print(searchResult["message"])
            case _:
                 print("sorry, I didn't understand it")                                       
if __name__=="__main__":        #made so that, if this file is imported in other file, it dont automatically run. it's an graceful exit guard.
 while True:    
    UserInput=input("[").strip().lower()
    if UserInput in {"quit", "bye", "leave", "leav", "ok bye", "get out", "peace out", "peece out"}:
            print("Ok Bye!")
            break
    if UserInput:
        handleProcess(UserInput)        
