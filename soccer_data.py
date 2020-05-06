import os 
import json
import http.client
import requests
from mailjet_rest import Client
from dotenv import load_dotenv



def club_colors(selected_team_id):
    """
    Returns the colors based on the id of the team. The color is later used in the newsletter so that fans receive the email in the colors of their favorite team.

    Param: selected_team_id

    """
    basic_colors = ["Red", "Blue", "Green", "Yellow"]
    colors = []
    connection.request('GET', f'/v2/teams/{selected_team_id}', None, headers )
    response = json.loads(connection.getresponse().read().decode())
    color = response["clubColors"]
    y=0
    for char in color:
        if char == '/':
            colors.append(color[:y-1])
            colors.append(color[y+2:])
        y+=1
    for color in basic_colors:
        if color in colors[0]:
            colors[0] = color
        if color in colors[1]:
            colors[1] = color
    if response["name"] == "Manchester City FC":
        colors[0] = "#1CC6E8"
    elif response["name"] == "Wolverhampton Wanderers FC":
        colors[1] = "#FDB913"
    elif response["name"] == "West Ham United FC":
        colors[1] = "#7A263A"
        colors[0] = "#1BB1E7"
    return colors
    
def format_date(match_date):
    """
    Formats a data string for printing and display purposes.

    Param: my_price (str) like "2019-08-11T13:00:00Z"

    Example: format_date(2019-08-11T13:00:00Z)

    Returns: 2019-08-11
    """

    return match_date[0:10]

def get_menu_option():
    """
    Function to display menu options and asking the user to choose one.

    """

    print("1. View their next 5 fixtures...")
    print("2. View their last 5 fixtures...")
    print("3. View their entire current season...")
    print("4. View their position in the table...")
    print("5. View the club roster...")
    print("6. View season statistics...")
    print("7. View team information...")
    print("8. Sign up to your club's weekly newsletter...")
    print("9. Calculate odds on next game...")
    print()
    return input("CHOOSE AN OPTION BELOW BY ENTERING THE MENU NUMBER: ")

def match_info(match):
    """
    Functions that returns the list called match_information. In conjunction with other function, it is used to display information about the games.

    Param: match is list

    """

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

def next_five(matches, status, purpose):
    """
    Function that displays the schedule for next 5 games. If there are fewer than 5 games left in the season, the function will dipsplay however many there are left.

    Params: 
        matches(list) contains all information about requested team
        status(string) holds value of a dictionary key like "FINISHED"
        purpose(string) like "email"

    Example of 1 game displayed:
        (2020-03-22) Matchday 31
	    Southampton FC vs Arsenal FC
    """
    next_content = []
    if purpose == "console":
        print()
        print("------------------------------")
        print("THE NEXT FIVE SCHEDULED GAMES:")
        print("------------------------------")
        print()
    x=0
    while(x < 5):
        match_date = matches[x]["utcDate"]
        match_date = format_date(match_date)
        match_info = ("(" + match_date + ") Matchday " + str(matches[x]["matchday"]))
        match_teams = ("\t" + matches[x]["homeTeam"]["name"] + " vs " + matches[x]["awayTeam"]["name"])
        if purpose == "console":
            print(match_info)
            print(match_teams)
            if status == "POSTPONED" or status == "CANCELLED":
                print(status)
            print()
            if matches[x]["matchday"] == 38:
                print("---> END OF SEASON <---")
                break
        elif purpose == "email":
            next_content.append(match_info)
            next_content.append(match_teams)
        x += 1
    return next_content

def last_five(matches, requested_team, purpose):
    """
    Function that displays results for last 5 games.

    Params: 
        matches(list) contains all information about requested team
        requested_team(string) holds value of a id of the requested team
        purpose(string) like "console"

    Example of 1 game displayed:
        (2020-02-23) Matchday 27 - WIN
	    ARSENAL FC 3 vs Everton FC 2
    """
    last_content = []
    if purpose == "console":
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
        matchday_info = "(" + match_date + ") Matchday " + str(matches[finished_games - x]["matchday"]) + " - " + match_information[2]
        matchday_score = "\t" + match_information[0] + " " + str(matches[finished_games - x]["score"]["fullTime"]["homeTeam"]) + " vs " + match_information[1] + " " + str(matches[finished_games - x]["score"]["fullTime"]["awayTeam"])
        if purpose == "console":
            print(matchday_info)
            print(matchday_score)
            print()
        elif purpose == "email":
            last_content.append(matchday_info)
            last_content.append(matchday_score)
        x -= 1
    return last_content

def whole_season(matches, requested_team):
    """
    Function that displays fixtures for the entire season. Both the finished and scheduled/postponed games.

    Params: 
        matches(list) contains all information about requested team
        requested_team(string) holds value of a id of the requested team

    Example of 2 games displayed:
        (2020-03-07) Matchday 29 - WIN
	LIVERPOOL FC 2 vs AFC Bournemouth 1
    
        -----------------
        UPCOMING FIXTURES
        -----------------
    
        (2020-03-16) Matchday 30
        Everton FC vs Liverpool FC
        ---> THIS FIXTURE IS POSTPONED <---
    """
    
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
    """
    Function that displays requested team position in the league.

    Params: 
        standings(list) contains all information about season table.
        selected_team_id(string) holds value of a id of the requested team

    Example of table displayed when the user chooses Manchester City:
        -----------------------------
        LIVE PREMIER LEAGUE STANDINGS
        -----------------------------

        1.	Liverpool FC (82pts)
        2.	---> MANCHESTER CITY FC <--- (57pts)
        3.	Leicester City FC (53pts)s
    """


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
    """
    Function that displays the squad of the requested team.

    Params: 
        squad(list) contains all information about the squad of the requested team.
        
    Example of part of the squad displayed:
        Roster:

    COACH: Pep Guardiola

    GOALKEEPERS

        Ederson
        Scott Carson
        Claudio Bravo

    DEFENDERS

        João Cancelo
        Nicolás Otamendi
        Kyle Walker
    """
    print()
    goalkeepers = []
    defenders = []
    midfielders = []
    attackers = []
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
    """
    Function that displays statistics for the season.

    Params: 
        team_stats(list) contains all information about requested team

    Example of 1 game displayed:
        Season Stats:

        Manchester City FC Season Statistics

            League Standing: 2nd
            Points: 57

            Games Played: 28
            Wins: 18
            Draws: 3
            Losses: 7
            Win Percentage: 64.28%

            Goals Scored: 68
            Goals Conceded: 31
            Goal Difference: 37
    """


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

def team_info(team, purpose):

    """
    Function that displays and returns the information about the tean.

    Params: 
        team(dict) contains all information about requested team
        purpose(string) like "console"

    Example of team stats displayed:
        ARSENAL FC

            FOUNDED: 1886
            VENUE: Emirates Stadium
            CLUB COLORS: Red / White

            ACTIVE COMPETITIONS:
            Premier League
            UEFA Europa League
            FA Cup

            ADDRESS: 75 Drayton Park London N5 1BU
            PHONE: +44 (020) 76195003
            WEBSITE: http://www.arsenal.com
            EMAIL: info@arsenal.co.uk
    """


    if purpose == "console":
        print("\n" + team["name"].upper() + "\n")
        print("\t" + "FOUNDED: " + str(team["founded"]))
        print("\t" + "VENUE: " + team["venue"])
        print("\t" + "CLUB COLORS: " + team["clubColors"] + "\n")
        print("\t" + "ACTIVE COMPETITIONS:")
        for competition in team["activeCompetitions"]:
            print("\t   " + competition["name"])
        print("\n\t" + "ADDRESS: " + team["address"])
        if team["phone"] != None:
            print("\t" + "PHONE: " + team["phone"])
        print("\t" + "WEBSITE: " + team["website"])
        if team["email"] != None:
            print("\t" + "EMAIL: " + team["email"])
        print()
    elif purpose == "email":
        team_contacts = [team["address"], team["phone"], team["website"]]
        if team["email"] != None:
            team_contacts.append(team["email"])
        return team_contacts

def newsletter(next_content, last_content, requested_team, selected_team_id, team_contact):
    color_theme = club_colors(selected_team_id)
    x = 0
    last_body = "<b><u>THE LAST FIVE GAMES</u></b><br/><br/>"
    next_body = "<b><u>THE NEXT FIVE GAMES</u></b><br/><br/>"
    while(x<10):
        last_body += f"{last_content[x]}<br/>{last_content[x+1]}<br/><br/>"
        next_body += f"{next_content[x]}<br/>{next_content[x+1]}<br/><br/>"
        x += 2
    if color_theme[1] == "White" and requested_team != "TOTTENHAM HOTSPUR FC":
        x = color_theme[0]
        color_theme[0] = color_theme[1]
        color_theme[1] = x
    footer_para = f"<div>Phone: {team_contact[1]}</div>"
    if team_contact[3] != None:
        footer_para += f"<div>Email: {team_contact[3]}</div>"
    message = f"""<html>
                <body style="font-family:'Verdana';text-align:center;color:{color_theme[0]};background-color:{color_theme[1]};">
                    <h1 style="color:{color_theme[1]};background-color:{color_theme[0]};font-size:30px;border:3px;border-style:solid;border-color:{color_theme[1]};">{requested_team} NEWSLETTER</h1>
                    <p style="font-size:13px;">{last_body}</p>
                    <p style="font-size:13px;">{next_body}</p>
                </body>
                <footer style="font-family:'Verdana';text-align:center;color:{color_theme[0]};background-color:{color_theme[1]};">
                    <p><u>Contact your Team</u></p>
                    <div>Address: {team_contact[0]}</div><div>Website: {team_contact[2]}</div>
                    {footer_para}
                </footer>
            </html>"""
    email_api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    mailjet = Client(auth=(email_api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "omf11@georgetown.edu",
            "Name": "Oliver"
        },
        "To": [
            {
            "Email": "omf11@georgetown.edu",
            "Name": "Oliver"
            }
        ],
        "Subject": "Premier League Team",
        "TextPart": "",
        "HTMLPart": message,
        "CustomID": "Team Newsletter"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())

def form(selected_id):
    """
    Function that calculates the form of the team based on last 5 games.

    Params: 
        selected_id(string) holds value of a id of the requested team

    """

    connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=FINISHED', None, headers )
    response = json.loads(connection.getresponse().read().decode())

    for match in response["matches"]:
        if match["competition"]["name"] == "Premier League":
            finished_matches.append(match)

    num_games = len(finished_matches)
    x=1
    form = 0
    while(x<6):
        #if team won the game, it gets 9 points
        if finished_matches[num_games-x]["score"]["winner"] == "HOME_TEAM" and finished_matches[num_games-x]["homeTeam"]["id"] == selected_id:
            form += 9
        elif finished_matches[num_games-x]["score"]["winner"] == "AWAY_TEAM" and finished_matches[num_games-x]["awayTeam"]["id"] == selected_id:
            form += 9
        #if team drew the game, it gets 3 points
        elif finished_matches[num_games-x]["score"]["winner"] == "None":
            form += 3
        x+=1
    return form

def outcome(win_prob):
    if win_prob > .6:
        outcome = "Given the probability of win, your team will most likely win."

    elif win_prob <= .6 and win_prob >= 0.4:
        outcome = "Given the probability of win, your team will most likely draw."

    elif win_prob < .4:
        outcome = "Given the probability of win, your team will most likely lose."

    return outcome    


#if __name__ == "__main__":

#team_names = []
#short_names = []
#tla = []

#load_dotenv()

#api_key = os.environ.get("FOOTY_API_KEY")
connection = http.client.HTTPConnection('api.football-data.org') #https://www.football-data.org/documentation/samples
#headers = { 'X-Auth-Token': api_key } 
#connection.request('GET', '/v2/competitions/PL/teams', None, headers )
#response = json.loads(connection.getresponse().read().decode())

if __name__ == "__main__":
    team_names = []
    short_names = []
    tla = []

    load_dotenv()

    api_key = os.environ.get("FOOTY_API_KEY")
    connection = http.client.HTTPConnection('api.football-data.org') #https://www.football-data.org/documentation/samples
    headers = { 'X-Auth-Token': api_key } 
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
            purpose = "console"
            status = "SCHEDULED"
            connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=SCHEDULED', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            for match in response["matches"]:
                if match["competition"]["name"] == "Premier League":
                    matches.append(match)
            if len(matches) == 0:
                status = "POSTPONED"
                connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=POSTPONED', None, headers )
                response = json.loads(connection.getresponse().read().decode())
                for match in response["matches"]:
                    if match["competition"]["name"] == "Premier League":
                        matches.append(match)
            if len(matches) == 0:
                status = "CANCELLED"
                connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=CANCELLED', None, headers )
                response = json.loads(connection.getresponse().read().decode())
                for match in response["matches"]:
                    if match["competition"]["name"] == "Premier League":
                        matches.append(match)     
            next_five(matches, status, purpose)

        elif menu_selection == "2":
            purpose = "console"
            connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=FINISHED', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            for match in response["matches"]:
                if match["competition"]["name"] == "Premier League":
                    matches.append(match)
            last_five(matches, requested_team, purpose)

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
            purpose = "console"
            connection.request('GET', f'/v2/teams/{selected_team_id}', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            team = response
            team_info(team, purpose)
        
        elif menu_selection == "8":
            matches = []
            purpose = "email"
            connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=FINISHED', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            for match in response["matches"]:
                if match["competition"]["name"] == "Premier League":
                    matches.append(match)
            last_content = last_five(matches, requested_team, purpose)

            status = "SCHEDULED"
            connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=SCHEDULED', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            for match in response["matches"]:
                if match["competition"]["name"] == "Premier League":
                    matches.append(match)
            if len(matches) == 0:
                status = "POSTPONED"
                connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=POSTPONED', None, headers )
                response = json.loads(connection.getresponse().read().decode())
                for match in response["matches"]:
                    if match["competition"]["name"] == "Premier League":
                        matches.append(match)
            if len(matches) == 0:
                status = "CANCELLED"
                connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=CANCELLED', None, headers )
                response = json.loads(connection.getresponse().read().decode())
                for match in response["matches"]:
                    if match["competition"]["name"] == "Premier League":
                        matches.append(match)     
            next_content = next_five(matches, status, purpose)

            connection.request('GET', f'/v2/teams/{selected_team_id}', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            team = response
            team_contact = team_info(team, purpose)
            
            newsletter(next_content, last_content, requested_team, selected_team_id, team_contact)

        elif menu_selection == "9":
            finished_matches = []

            connection.request('GET', f'/v2/teams/{selected_team_id}/matches?status=POSTPONED', None, headers )
            response = json.loads(connection.getresponse().read().decode())

            for match in response["matches"]:
                if match["competition"]["name"] == "Premier League":
                    matches.append(match)
            next_game = matches[0]
            ids_names = [str(next_game["homeTeam"]["id"]), next_game["homeTeam"]["name"], str(next_game["awayTeam"]["id"]), next_game["awayTeam"]["name"]]
            if selected_team_id == ids_names[0]:
                home_bonus = 5
            else:
                home_bonus = -5
            
            y = 0 
            z = 0

            selected_team_id = str(selected_team_id)

            for x in ids_names:
                if x == selected_team_id:
                    team_id = selected_team_id
                    z = y
                y+=1

            if z == 0:
                opp_id = ids_names[2]
            else:
                opp_id = ids_names[0]
            
            team_form = form(team_id)
            opp_form = form(opp_id)
            
            connection.request('GET', '/v2/competitions/PL/standings', None, headers )
            response = json.loads(connection.getresponse().read().decode())
            standings = response["standings"][0]["table"]

            for team in standings:
                print(team_id)
                print(team["team"]["id"])
                if str(team["team"]["id"]) == team_id:
                    print("hi")
                    team_points = team["points"]
                elif str(team["team"]["id"]) == opp_id:
                    opp_points = team["points"]

            team_odds_tally = home_bonus + team_form + team_points
            opp_odds_tally = opp_form + opp_points

            win_prob = team_odds_tally / (opp_odds_tally + team_odds_tally)
            
            if odds < 0.5:
                american_odds = (100/win_prob) - 100
                american_odds = round(american_odds, 0)
                american_odds = "+" + str(american_odds)
            else:
                american_odds = (win_prob*100 / (1 - win_prob))*-1
                american_odds = round(american_odds, 0)
                american_odds = str(american_odds)
            
            american_odds = american_odds[:4]
            
            print(american_odds)
            
            
            


        menu_selection = get_menu_option()

        

    #pip install -U python-dotenv