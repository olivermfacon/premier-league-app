# Premier League Project

Our application is designed for English Premier League fans who want a centralized, team-specific tool that provides them with all information about the league in one place. The program allows you to display the following features for your favorite teams: next 5 fixtures, last 5 fixtures, entire season, position in the table, club roster, season statistics, team information, odds for the next game.
Additionally, you can sign up for an email newsletter containing the odds on the next game, last five games, next five games, and contact information to your club. Because of Coronavirus the Premier League has been suspended. Therefore, at this point in time the automatic email newsletter is not available. Note however, that our program still can send you a single email with the odds for the next game and other information.


## Installation
Fork this repository, clone it (choose a familiar download location such as Desktop). Then, navigate to your repository from command line:
```sh
cd ~/'download location'/soccer_data
```
## Setup and Security
Consider creating a virtual environment called something like soccer-env:
```sh
conda create -n soccer-env python=3.7 # (first time only)
```
Then, activate your virtual environment:
```sh
conda activate soccer-env
```
From the created virtual environment, install the required packages specified in the "requirements.txt" file you created:
```sh
pip install -r requirements.txt
```
Your program needs 3 API Keys. The first one is called Football-data and is available here https://www.football-data.org/. The second and third ones API Keys are available at https://www.mailjet.com. Program's source code, however, should absolutely not include the secret API Key values.
Consequently, you need to create an environment variable called FOOTY_API_KEY at https://www.football-data.org/ so that the program can request data about your favorite team. Also, go to https://www.mailjet.com to get two environment variables: API_KEY and API_SECRET so that you can access email functionality. After signing up, you'll the website will show you both the API_KEY and API_SECRET Your program should read the API Key from this environment variable at run-time.

Please keep in mind that in order for the program to send you email newsletters (one of the functionalities of our application) you need to purchase at least "Three + Free"  API package from https://www.football-data.org/. This is because the free version of the API limits user ability so that he or she can only make 10 requests per minute. Unfortunately, the newsletter requires more than that. We're sorry for that but it's not in our capability to change it. The good news is that all other features of our application can be accessed using free API!

Create a new file called ".env" in the root directory of this repo, and paste the following contents inside, using your own values as appropriate. The exception is 
```sh
FOOTY_API_KEY="your API key from https://www.football-data.org/"
API_KEY="your API_KEY from https://www.mailjet.com"
API_SECRET="your API_SECRET from https://www.mailjet.com "
MY_EMAIL_ADDRESS="Your_Email_Address@gmail.com"
```

## Usage
Please make sure that the virtual environment you just created is active. To run the script, type the following in the command line:
```sh
python soccer_data.py
```

No you should be able to enter the name of the premier league team. If your input is valid, you'll see a menu with 9 options to choose. Depending on what you want, please enter an integer from 1 to 9. Afterwards, the program will display the desired the chosen content. If you enter "8" - the email newsletter function - the program will prompt you to enter your email. After entering an email and pressing enter, go to your inbox. It should include the email newsletter in the colors of your favorite club. To exit the application, enter 'Done'.


## Testing
Install ```pytest``` package (first time only):
command line:
```sh
pip install pytest
```

Run tests:

```sh
pytest
```

## Help

If you have any questions regarding the application, please contact US at support@premeierleague.edu
Also, we would appreciate any feedback from you so that we can bring you an even better user experience!
Thank you for using our program!