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
    print("7. View additional information on the club...")
    print()
    return input("CHOOSE AN OPTION BELOW BY ENTERING THE MENU NUMBER: ")
    print()

def next_five(response):
    print()
    print("THE NEXT FIVE SCHEDULED GAMES:")
    print()
    x=0
    while(x < 5):
        match_date = response["matches"][x]["utcDate"]
        match_date = format_date(match_date)
        print(response["matches"][x]["homeTeam"]["name"] + " vs " + response["matches"][x]["awayTeam"]["name"] + " (" + match_date + ")")
        x += 1
    print()

def last_five(response, requested_team):
    print(response)
    print()
    print("THE LAST FIVE COMPLETED GAMES")
    print()
    x=1
    finished_games = len(response["matches"])
    while(x < 6):
        match_date = response["matches"][finished_games - x]["utcDate"]
        match_date = format_date(match_date)
        if response["matches"][finished_games - x]["score"]["winner"] == "HOME_TEAM":
            home_team = response["matches"][finished_games - x]["homeTeam"]["name"].upper()
            if home_team == requested_team.upper():
                result = "W"
            else:
                result = "L"
            away_team = response["matches"][finished_games - x]["awayTeam"]["name"]
        elif response["matches"][finished_games - x]["score"]["winner"] == "AWAY_TEAM":
            home_team = response["matches"][finished_games - x]["homeTeam"]["name"]
            away_team = response["matches"][finished_games - x]["awayTeam"]["name"].upper()
            if away_team == requested_team.upper():
                result = "W"
            else:
                result = "L"
        else:
            home_team = response["matches"][finished_games - x]["homeTeam"]["name"]
            away_team = response["matches"][finished_games - x]["awayTeam"]["name"]
            result = "D"
        print(home_team + " " + str(response["matches"][finished_games - x]["score"]["fullTime"]["homeTeam"]) + " vs " + away_team + " " + str(response["matches"][finished_games - x]["score"]["fullTime"]["awayTeam"]) + " (" + match_date + ") " + result)
        x += 1

def whole_season(response, requested_team):
    x=0
    if response["matches"][x]["status"] == "FINISHED":
        print()
        print("------------")
        print("PAST FIXTURES")
        print("------------")
        print()
    for match in response["matches"]:
        if match["competition"]["name"] == "Premier League":
            match_date = match["utcDate"]
            match_date = format_date(match_date)
            if match["status"] == "FINISHED":
                if match["score"]["winner"] == "HOME_TEAM":
                    home_team = match["homeTeam"]["name"].upper()
                    away_team = match["awayTeam"]["name"]
                elif match["score"]["winner"] == "AWAY_TEAM":
                    home_team = match["homeTeam"]["name"]
                    away_team = match["awayTeam"]["name"].upper()
                else:
                    home_team = match["homeTeam"]["name"]
                    away_team = match["awayTeam"]["name"]
                print(home_team + " " + str(match["score"]["fullTime"]["homeTeam"]) + " vs " + away_team + " " + str(match["score"]["fullTime"]["awayTeam"]) + " (" + match_date + ")")
            else:
                print(match["homeTeam"]["name"] + " vs " + match["awayTeam"]["name"] + " (" + match_date + ")")
            if(match["status"] == "POSTPONED"):
                print("THE ABOVE GAME IS POSTPONED")
            if match["status"] == "FINISHED" and (response["matches"][x+1]["status"] == "SCHEDULED" or response["matches"][x+1]["status"] == "POSTPONED") and x != 37:
                print()
                print("------------")
                print("UPCOMING FIXTURES")
                print("------------")
                print()
        x += 1
    

team_names = []
short_names = []
tla = []



api_key = os.environ.get("API_KEY")

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': '3d0a31585ed447b2899c048748e26386' }
connection.request('GET', '/v2/competitions/PL/teams', None, headers )
response = json.loads(connection.getresponse().read().decode())
print(response)
print("-----------------------------")
print("PREMIER LEAGUE SQUAD TRACKER")
print("-----------------------------")

y = 1
for team in response["teams"]:
    print(y)
    y += 1
    team_names.append(team["name"])
    short_names.append(team["shortName"])
    tla.append(team["tla"])

valid_team = False

x=0

while valid_team == False:
    requested_team = input("ENTER THE NAME OF YOUR FAVORITE PREMIER LEAGUE TEAM: ").lower()
    for team in response["teams"]:
        print(requested_team)
        print(team_names[x].lower())
        if requested_team == team_names[x].lower() or requested_team == short_names[x].lower() or requested_team == tla[x].lower():
            selected_team_id = team["id"]
            valid_team = True
        x += 1
    if valid_team == False:
        print("Invalid team entry")
        x = 0

print()

menu_selection = get_menu_option()

if menu_selection == "1":
    connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=SCHEDULED', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    next_five(response)
elif menu_selection == "2":
    connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=FINISHED', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    last_five(response, requested_team)
elif menu_selection == "3":
    connection.request('GET', f'/v2/teams/{selected_team_id}/matches', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    whole_season(response, requested_team)


