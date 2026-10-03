#brain.py
import re
#define all RegEx patterns, so that the brain actually understands which word for which.
#NOTE: the "open_folder" should always be above "open_app". this is to prevent greedy "open_app" RegEx matching
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
     "patterns":[r"\b(?:open|go to|go to the|get in|get the|get me the|get me|show|show me)\s+(?:my\s+)?(downloads|desktop|documents|home)\b"],
     "has_target": True,
     "target_formatter": lambda match: f"~/{match.group(1).capitalize()}",
 },
 "open_app": {
     "patterns":[r"\b(?:open|opn|opnn|start|strt|start my|staart)\s+(?:the\s+)?([a-zA-Z0-9_\-\s!&;@#*\]]+)\b"],
     "has_target": True,
     "target_formatter": lambda match: match.group(1).strip()     
 }
}
def handle_iterate(userInput: str)-> dict:
    text=userInput.strip().lower()
    #iterate/loop through
    for actions, configs in INTENTS.items():
        for pattern in configs["patterns"]:
            match=re.search(pattern, text)

            if match:
                target=None

                if configs.get("has_target"):               
                    formatter=configs.get("target_formatter", lambda m: m.group(1))
                    target=formatter(match)
                return {"actions": actions, "target": target}
    return {"actions": "unknown", "target": None}