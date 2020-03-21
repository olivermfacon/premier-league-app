import os 
import json
import http.client
import requests

def format_date(match_date):
    return match_date[0:10]

def get_menu_option():
    print("1. View their next five fixtures...")
    print("2. View their last 5 fixtures...")
    print("3. View their entire current season...")
    print("4. View their position in the table...")
    print("5. View the odds on their next game...")
    print("6. View the club's most recent lineup...")
    print("7. View season statistics...")
    print()
    return input("CHOOSE AN OPTION BELOW BY ENTERING THE MENU NUMBER: ")

def match_info(match):
    match_information = []
    print(match["homeTeam"]["name"])
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


team_names = []
short_names = []
tla = []

api_key = os.environ.get("API_KEY")

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': '3d0a31585ed447b2899c048748e26386' }
connection.request('GET', '/v2/competitions/PL/teams', None, headers )
response = json.loads(connection.getresponse().read().decode())

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

    menu_selection = get_menu_option()

