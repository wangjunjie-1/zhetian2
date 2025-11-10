from coordinate import *
import json
class Technology:
    def __init__(self,ocr):
        self.ocr = ocr
        self.current_level = {
            "camp": {
                "Q":0,
                "W":0,
                "E":0,
                "R":0,
                "S":0,
                "D":0
                },
            "research": {
                "Q":0,
                "W":0,
                "E":0,
                "R":0,
                "D":0,
                "F":0
            },
            "advanced_camp":{
            }
        }
        self.require_resources = json.load(open("tech_requirements.json","r"))
        print(self.require_resources)
        self.map = {
            str(research_idx):"research",
            str(camp_idx):"camp",
            str(advanced_camp_idx):"advanced_camp",
        }

    def upgrade(self,build_idx,tech_idx,level):
        tech_name = self.map[build_idx]
        cur_level = self.current_level[tech_name][tech_idx]
        for aim_level in range(cur_level+1,level+1):
            # require resources
            requirements = self.require_resources[tech_name][tech_idx][str(aim_level)]
            req_gold = int(requirements["gold"])
            req_wood = int(requirements["wood"])
            while True:
               cur_gold,cur_wood = self.ocr.check_gold_wooden()
               if cur_gold >= req_gold and cur_wood >= req_wood:
                   break
               else:
                   time.sleep(int(aim_level))
            # upgrade
            self.current_level[tech_name][tech_idx] = aim_level
            pyautogui.press(str(builder_idx))
            pyautogui.press(str(tech_idx))
            enter_info(f"upgrade {tech_name} {tech_idx} to level {aim_level}")

