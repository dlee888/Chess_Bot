# Chess Bot

README for version 2.0.0

Chess Bot is a discord bot that plays chess.
It also has a built-in elo rating system.

## Links

[Chess Bot support server](https://discord.gg/Bm4zjtNTD2)

[Top.gg](https://top.gg/bot/801501916810838066/vote)

[Github](https://github.com/jeffarjeffar/Chess_Bot)

[Invite](https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=268815424&scope=bot)

## Mechanics

### Basic Mechanics

You can use the command `$challenge` to challenge the bot to a game of chess.

Use `$move` to make a move. Make sure your move is in SAN (Standard Algebraic Notation). Otherwise, the bot will not understand it.

Use `$view` to view your game.

### Chess Bot profiles

You can challenge multiple levels of the bot. Make sure to specify which level you want to play when using the `$challenge` command.

Use the `$profiles` command to see a list of all levels you can challenge, and use `$profile <tag>` to learn more about a specific bot.
Note: the tag of a bot is _not_ the same as it's name. For example, the tag of the bot "Chess Bot level 1" is `cb1`.

Chess Bot uses a custom built engine to determine which moves it plays. (It's not very good though, because I built it, and I'm bad at coding).

### Timer

To prevent people from abandoning a the game without loss of rating, you will automatically resign if you do not make a move for 3 days.

You will receive a low time warning when you only have 1 day left.

Use `$time` to see how much time you have left.

## Commands

### Playing

- challenge: Challenges Chess Bot to a game.

- move [move]: Plays [move] against the computer.

- resign: Resigns the game.

- view: Views your current game.

- time: Sends how much time you have left.

- profiles: Sends a list of which profiles you can challenge.

- fen: Sends current game in [FEN format](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation).
  
### Moderation

These commands require special permissions.

- prefix [prefix]: Makes or changes the server's server specific prefix. Must have administrator permission in the server.

### Other

- botinfo: Sends basic info and stats about the bot

- ping: Sends "Pong!" and gives latency

- rating: Tells you your rating

- leaderboard: Shows top rated players

- rank: Shows your rank out of all rated players

- help: Sends a message with all of the commands

- theme: Change your board theme

- vote: Gifts you 5 rating points after voting for Chess Bot on top.gg

- stats: Sends your stats.

To get more information about any command, use `$help <command>`
