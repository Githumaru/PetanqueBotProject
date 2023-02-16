# NonameProject
This project is a Telegram bot for tracking the ratings of players in a game, using the ELO rating system.

The bot has a starting menu with four buttons:

Add player
Add match
Show rating
Show rank
When each button is selected, the bot offers the necessary actions to achieve the goal.

How to use the bot
To use the bot, you need to:

Find the bot on Telegram by username or link.
Start a conversation with the bot.
Select the required option from the starting menu, following the bot's instructions.
How to run the bot
To run the bot, you need to:

Obtain the Telegram Bot API token and set up bot access to the API.
Install all necessary dependencies specified in the requirements.txt file using the command: pip install -r requirements.txt.
Run the bot using the command: python bot.py.
Function Descriptions
Add player
When this option is selected, the bot prompts to enter the name of a new player. After the name is entered, the player is given an initial score and added to the csv-file with other players.

Add match
When this option is selected, the bot prompts to choose two players who played against each other, specify the match result (win, lose, or draw), and updates their score in the csv-file using the ELO system.

Show rating
When this option is selected, the bot displays a list of all players and their score in descending order.

Show rank
When this option is selected, the bot prompts to choose a player and displays his ranking and score.

Authors
This project was created by Vyacheslav Trofimov

![show rating and add match result]([url](https://github.com/Githumaru/PetangBotProject/blob/main/show%20rating%20and%20add%20match%20result.jpg?raw=true))
![add match result and show rating]([url](https://github.com/Githumaru/PetangBotProject/blob/main/add%20match%20result%20and%20show%20rating%20.jpg?raw=true))
![add a new player and show rating]([url](https://github.com/Githumaru/PetangBotProject/blob/main/add%20a%20new%20player%20and%20show%20rating.jpg?raw=true))
![show rank]([url](https://github.com/Githumaru/PetangBotProject/blob/main/show%20rank.jpg?raw=true))
