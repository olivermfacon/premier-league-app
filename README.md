# Premier League Project

Our application is designed for English Premier League fans who want a centralized, team-specific tool that provides them with all information about the league in one place.

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
Your program needs an API Key to issue requests to the Football-data API available here https://www.football-data.org/. Program's source code, however, should absolutely not include the secret API Key value. Instead, you should set an environment variable called FOOTY_API_KEY, and your program should read the API Key from this environment variable at run-time.

Please keep in mind that in order for the program to send you email newsletters (one of the functionalities of our application) you need to purchase at least "Three + Free"  API package. This is because they free version of the API limits user ability so that he or she can only make 10 requests per minute. Unfortunately, the newsletter requires more than that. We're sorry for that but it's not in our capability to change it. The good news is that all other features of our application can be accessed using free API!

You need to create an 'env' file and put the following inside:
```sh
FOOTY_API_KEY="your API key"
```

## Usage
To run the script, type the following in the command line:
```sh
python soccer_data.py
```

No you should be able to enter a stock ticker. 
The program will return the latest close price, 52 week high, 52 week low, and recommendation. Also, if you want to, the program will return the graph with the stock prices over time.

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