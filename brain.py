#brain.py
import re
#define all RegEx patterns, so that the brain actually understands which word for which.
#NOTE: the "open_folder" should always be above "open_app". this is to prevent greedy "open_app" RegEx matching that instantly hijacks the open_folder
NOISE_PREFIXES=sorted(["hello", "helo", "hi", "hii", "plzzz", "hello bro", "helo bro", "hey xeler", "hey"], key=len, reverse=True)
def noise_prefixes_remover(text: str)-> str:
           text=text.lower().strip()
           for Nprefixes in NOISE_PREFIXES:
                if text.startswith(Nprefixes):
                     #this works as a imagianary scissor cutting the filler words. so that xeler can hear only the words needed to hear.
                     text=text[len(Nprefixes):].strip()
                     break
           text=re.sub(r"\s+", " ", text)
           return text
INTENTS= {
 "get_status": {
     "patterns":[r"\b(working|where am i|status|system status|working dir|dir|stats|stst|stts)\b"],
     "has_target": False
 },
 "get_time": {
     "patterns":[r"\b(time|what is the time|date|whats the time|clock|time right now|timw|tine)\b"],
     "has_target": False
 },
 "open_folder": {
     "patterns":[r"\b(?:open|go \s+to|go \s+to \s+the|get \s+in|get \s+the|get \s+me \s+the|get \s+me|show|show \s+me)\s+(?:my\s+)?(downloads|desktop|documents|home)\b"],
     "has_target": True,
     "target_formatter": lambda match: f"~/{match.group(1).capitalize()}",
 },
 "web_search": {
     "patterns":[r"\b(?:search|look\s+up|google|google\s+the|google\s+that|find|find\s+the|find\s+that)\s+(?:for\s+)?(.+)\b"],
     "has_target":True,
     "target_formatter": lambda match: match.group(1).strip(),
 },
 "wiki": {
      "patterns":[r"\b(?:lookup|look\s+up|wiki|hey\s+wiki|hey\s+wikipedia|search\s+on\s+wiki)\s+(?:for\s+)?(.+)\b"],
      "has_target":True,
      "target_formatter": lambda match: match.group(1).strip(),
 },
 "open_app": {
     "patterns":[r"\b(?:open|opn|opnn|start|strt|start \s+my|staart|run|rn|rin|launch|laucbh|leuanch|launcb|lainch|start \s+the)\s+(?:the\s+)?(?!downloads|desktop|documents|home)([a-zA-Z0-9_\-\s!&;@#*\]\[]+)\b"],
     "has_target": True,
     "target_formatter": lambda match: match.group(1).strip()  
 }
}
def handle_iterate(userInput: str)-> dict:
    if not userInput or not userInput.strip():
        return {"actions": "unknown", "target": None}
    
    Ctext=noise_prefixes_remover(userInput)
    #iterate/loop through defined datas
    for actions, configs in INTENTS.items():
        for pattern in configs["patterns"]:
            match=re.search(pattern, Ctext)

            if match:
                target=None

                if configs.get("has_target"):               
                    formatter=configs.get("target_formatter", lambda m: m.group(1))
                    target=formatter(match)
                return {"actions": actions, "target": target}
    return {"actions": "unknown", "target": None}
