import os 
import json
import http.client
import requests
from dotenv import load_dotenv

def format_date(match_date):
    return match_date[0:10]

def get_menu_option():
    print("1. View their next five fixtures...")
    print("2. View their last 5 fixtures...")
    print("3. View their entire current season...")
    print("4. View their position in the table...")
    print("5. View the club roster...")
    print("6. View season statistics...")
    print("7. View team information...")
    print()
    return input("CHOOSE AN OPTION BELOW BY ENTERING THE MENU NUMBER: ")

def match_info(match):
    match_information = []
    if match["score"]["winner"] == "HOME_TEAM":
        match_information.append(match["homeTeam"]["name"].upper())
        match_information.append(match["awayTeam"]["name"])
        if match_information[0] == requested_team:
            match_information.append("WIN")
        else:
            match_information.append("LOSS")
    elif match["score"]["winner"] == "AWAY_TEAM":
        match_information.append(match["homeTeam"]["name"])
        match_information.append(match["awayTeam"]["name"].upper())
        if match_information[1] == requested_team:
            match_information.append("WIN")
        else:
            match_information.append("LOSS")
    else:
        match_information.append(match["homeTeam"]["name"])
        match_information.append(match["awayTeam"]["name"])
        match_information.append("DRAW")
    return match_information

def next_five(matches):
    print()
    print("------------------------------")
    print("THE NEXT FIVE SCHEDULED GAMES:")
    print("------------------------------")
    print()
    x=0
    while(x < 5):
        match_date = matches[x]["utcDate"]
        match_date = format_date(match_date)
        print("(" + match_date + ") Matchday " + str(matches[x]["matchday"]))
        print("\t" + matches[x]["homeTeam"]["name"] + " vs " + matches[x]["awayTeam"]["name"])
        print()
        if matches[x]["matchday"] == 38:
            print("---> END OF SEASON <---")
            break
        x += 1
    print()

def last_five(matches, requested_team):
    print()
    print("-----------------------------")
    print("THE LAST FIVE COMPLETED GAMES")
    print("-----------------------------")
    print()
    x=5
    finished_games = len(matches)
    while(x > 0):
        match_date = matches[finished_games - x]["utcDate"]
        match_date = format_date(match_date)
        match_information = match_info(matches[finished_games - x])
        print("(" + match_date + ") Matchday " + str(matches[finished_games - x]["matchday"]) + " - " + match_information[2])
        print("\t" + match_information[0] + " " + str(matches[finished_games - x]["score"]["fullTime"]["homeTeam"]) + " vs " + match_information[1] + " " + str(matches[finished_games - x]["score"]["fullTime"]["awayTeam"]))
        print()
        x -= 1

def whole_season(matches, requested_team):
    x=0
    if matches[x]["status"] == "FINISHED":
        print()
        print("-------------")
        print("PAST FIXTURES")
        print("-------------")
        print()
    for match in matches:
        match_date = match["utcDate"]
        match_date = format_date(match_date)
        if match["status"] == "FINISHED":
            match_information = match_info(match)
            print("(" + match_date + ") Matchday " + str(match["matchday"]) + " - " + match_information[2])
            print("\t" + match_information[0] + " " + str(match["score"]["fullTime"]["homeTeam"]) + " vs " + match_information[1] + " " + str(match["score"]["fullTime"]["awayTeam"]))
        else:
            print("(" + match_date + ") Matchday " + str(match["matchday"]))
            print("\t" + match["homeTeam"]["name"] + " vs " + match["awayTeam"]["name"])
        if(match["status"] == "POSTPONED"):
            print("\t---> THIS FIXTURE IS POSTPONED <---")
        if(match["status"] == "CANCELLED"):
            print("\t---> THIS FIXTURE IS CANCELLED <---")
        print()
        if match["status"] == "FINISHED" and (matches[x+1]["status"] == "SCHEDULED" or matches[x+1]["status"] == "POSTPONED") and x != 37:
            print()
            print("-----------------")
            print("UPCOMING FIXTURES")
            print("-----------------")
            print()
        x += 1
    print()

def prem_table(standings, selected_team_id):
    print()
    print("-----------------------------")
    print("LIVE PREMIER LEAGUE STANDINGS")
    print("-----------------------------")
    print()
    for team in standings:
        if team["team"]["id"] == selected_team_id:
            print(str(team["position"]) + ".\t---> " + team["team"]["name"].upper() + " <--- (" + str(team["points"]) + "pts)")
        else:
            print(str(team["position"]) + ".\t" + team["team"]["name"] + " (" + str(team["points"]) + "pts)")
    print()

def display_squad(squad):
    print()
    goalkeepers = []
    defenders = []
    midfielders = []
    attackers = []
    #print(squad)
    for person in squad:
        if person["position"] == "Goalkeeper":
            goalkeepers.append(person["name"])
        elif person["position"] == "Defender":
            defenders.append(person["name"])
        elif person["position"] == "Midfielder":
            midfielders.append(person["name"])
        elif person["position"] == "Attacker":
            attackers.append(person["name"])
        elif person["role"] == "COACH":
            print("COACH: " + person["name"] + "\n")
    print("GOALKEEPERS\n")
    for keeper in goalkeepers:
        print(f"\t{keeper}")
    print(f"\nDEFENDERS\n")
    for defender in defenders:
        print(f"\t{defender}")
    print(f"\nMIDFIELDERS\n")
    for midfielder in midfielders:
        print(f"\t{midfielder}")
    print(f"\nATTACKERS\n")
    for attacker in attackers:
        print(f"\t{attacker}")
    print()

def season_statistics(team_stats):
    win_percentage = (team_stats["won"]/team_stats["playedGames"])*100
    if team_stats["position"] == 1:
        place = "st"
    elif team_stats["position"] == 2:
        place = "nd"
    elif team_stats["position"] == 3:
        place = "rd"
    else:
        place = "th"
    print("\n" + team_stats["team"]["name"] + " Season Statistics\n")
    print("\tLeague Standing: " + str(team_stats["position"]) + place)
    print("\tPoints: " + str(team_stats["points"]) + "\n")
    print("\tGames Played: " + str(team_stats["playedGames"]))
    print("\tWins: " + str(team_stats["won"]))
    print("\tDraws: " + str(team_stats["draw"]))
    print("\tLosses: " + str(team_stats["lost"]))
    print("\tWin Percentage: " + str(win_percentage)[:5] + "%\n")
    print("\tGoals Scored: " + str(team_stats["goalsFor"]))
    print("\tGoals Conceded: " + str(team_stats["goalsAgainst"]))
    print("\tGoal Difference: " + str(team_stats["goalDifference"]) + "\n")

def team_info(team):
    print("\n" + team["name"].upper() + "\n")
    print("\t" + "FOUNDED: " + str(team["founded"]))
    print("\t" + "VENUE: " + team["venue"])
    print("\t" + "CLUB COLORS: " + team["clubColors"] + "\n")
    print("\t" + "ACTIVE COMPETITIONS:")
    for competition in team["activeCompetitions"]:
        print("\t   " + competition["name"])
    print("\n\t" + "ADDRESS: " + team["address"])
    print("\t" + "PHONE: " + team["phone"])
    print("\t" + "WEBSITE: " + team["website"])
    print("\t" + "EMAIL: " + team["email"] + "\n")


team_names = []
short_names = []
tla = []

load_dotenv()

api_key = os.environ.get("API_KEY")
connection = http.client.HTTPConnection('api.football-data.org') #https://www.football-data.org/documentation/samples
headers = { 'X-Auth-Token': api_key } #
connection.request('GET', '/v2/competitions/PL/teams', None, headers )
response = json.loads(connection.getresponse().read().decode())
#3d0a31585ed447b2899c048748e26386
print("---------------------------------------------")
print("SOCCER TEAM PROGRESS TRACKER (Premier League)")
print("---------------------------------------------")

y = 1

for team in response["teams"]:
    y += 1
    team_names.append(team["name"])
    short_names.append(team["shortName"])
    tla.append(team["tla"])

valid_team = False

x=0

while valid_team == False:
    requested_team = input("ENTER THE NAME OF A PREMIER LEAGUE TEAM: ").lower()
    for team in response["teams"]:
        if requested_team == team_names[x].lower() or requested_team == short_names[x].lower() or requested_team == tla[x].lower():
            requested_team = team_names[x].upper()
            selected_team_id = team["id"]
            valid_team = True
        x += 1
    if valid_team == False:
        print("Invalid team entry")
        x = 0

print()

menu_selection = get_menu_option()

while menu_selection!="done":
    matches = []

    if menu_selection == "1":
        connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=SCHEDULED', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        for match in response["matches"]:
            if match["competition"]["name"] == "Premier League":
                matches.append(match)
        next_five(matches)

    elif menu_selection == "2":
        connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=FINISHED', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        for match in response["matches"]:
            if match["competition"]["name"] == "Premier League":
                matches.append(match)
        last_five(matches, requested_team)

    elif menu_selection == "3":
        connection.request('GET', f'/v2/teams/{selected_team_id}/matches', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        for match in response["matches"]:
            if match["competition"]["name"] == "Premier League":
                matches.append(match)
        whole_season(matches, requested_team)
    
    elif menu_selection == "4":
        connection.request('GET', '/v2/competitions/PL/standings', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        standings = response["standings"][0]["table"]
        prem_table(standings,selected_team_id)

    elif menu_selection == "5":
        connection.request('GET', f'/v2/teams/{selected_team_id}', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        squad = response["squad"]
        display_squad(squad)

    elif menu_selection == "6":
        connection.request('GET', '/v2/competitions/PL/standings', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        table = response["standings"][0]["table"]
        x = 0
        for team in table:
            if team["team"]["name"].upper() == requested_team:
                season_statistics(table[x])
            x += 1
        
    elif menu_selection == "7":
        connection.request('GET', f'/v2/teams/{selected_team_id}', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        team = response
        team_info(team)

    menu_selection = get_menu_option()

    

#pip install -U python-dotenv


#bflkjwbfkjb