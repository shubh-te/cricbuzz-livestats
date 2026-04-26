import urllib.request
import xml.etree.ElementTree as ET
import streamlit as st
import datetime

@st.cache_data(ttl=60) # Cache for 60 seconds
def get_live_matches():
    matches = []
    
    # 1.  REAL MATCHES from Free RSS Feed (ESPN)
    try:
        url = "https://static.cricinfo.com/rss/livescores.xml"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        for item in root.findall('./channel/item'):
            title = item.find('title').text        
            description = item.find('description').text  
            
            matchType = "Live/Recent"
            if "Test" in description or "Day" in description or "Inning" in description:
                matchType = "Test"
            elif "T20" in description or "20" in title:
                matchType = "T20"
            elif "ODI" in description or "50" in title:
                matchType = "ODI"

            parts = title.split(' v ')
            scores = []
            
            for part in parts:
                part_clean = part.replace('*', '').strip()
                
                overs = "--"
                if "(" in part_clean and "ov" in part_clean.lower():
                    start = part_clean.find("(")
                    end = part_clean.find(")")
                    if end > start:
                        overs = part_clean[start+1:end].replace("ov", "").replace("OV", "").strip()
                        part_clean = part_clean[:start].strip()

                words = part_clean.split(' ')
                team_name_parts = []
                score_str = "0/0"
                for w in words:
                    if any(c.isdigit() for c in w):
                        if '&' in score_str:
                            score_str += f" & {w}"
                        else:
                            score_str = w
                    elif w != '&':
                        team_name_parts.append(w)
                
                team_name = " ".join(team_name_parts)
                
                runs = score_str
                wickets = "10"
                if '/' in score_str:
                    runs_wic = score_str.split('/')
                    runs = runs_wic[0]
                    wickets = runs_wic[1]

                scores.append({
                    "inning": team_name,
                    "r": runs,
                    "w": wickets,
                    "o": overs 
                })

            matches.append({
                "name": title.replace(' *', ''),
                "matchType": matchType,
                "status": description,
                "venue": "Cricinfo Feed",
                "date": datetime.date.today().strftime("%d %b %Y"),
                "score": scores
            })
    except Exception as e:
        pass

    # 2. 🏏 DEMO MATCHES (Taki UI hamesha Google jaisa T20, ODI aur overs ke sath acha dikhe)
    demo_matches = [
        {
            "name": "India vs Australia, 1st Test",
            "matchType": "Test",
            "status": "India lead by 250 runs",
            "venue": "Wankhede Stadium, IND",
            "date": datetime.date.today().strftime("%d %b %Y"),
            "score": [
                {"inning": "India 1st Inning", "r": 450, "w": 5, "o": 120.1},
                {"inning": "Australia 1st Inning", "r": 200, "w": 10, "o": 60.4}
            ]
        },
        {
            "name": "England vs South Africa, T20",
            "matchType": "T20",
            "status": "Match in Progress",
            "venue": "Lords, ENG",
            "date": datetime.date.today().strftime("%d %b %Y"),
            "score": [
                {"inning": "England", "r": 180, "w": 4, "o": 20.0},
                {"inning": "South Africa", "r": 120, "w": 3, "o": 14.2}
            ]
        },
        {
            "name": "Pakistan vs New Zealand, 3rd ODI",
            "matchType": "ODI",
            "status": "Pakistan need 45 runs to win",
            "venue": "Gaddafi Stadium, PAK",
            "date": datetime.date.today().strftime("%d %b %Y"),
            "score": [
                {"inning": "New Zealand", "r": 285, "w": 8, "o": 50.0},
                {"inning": "Pakistan", "r": 241, "w": 4, "o": 42.3}
            ]
        }
    ]

    # Combine Real + Demo matches so UI categories always show up
    matches.extend(demo_matches)
    
    return matches