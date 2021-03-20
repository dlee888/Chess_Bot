# Chess Bot

Chess Bot is a bot that plays chess.
It also has a built-in elo rating system.

## Links

[Chess Bot support server](https://discord.gg/Bm4zjtNTD2)

[Top.gg](https://top.gg/bot/801501916810838066/vote)

[Github](https://github.com/jeffarjeffar/Chess_Bot)

[Invite](https://discord.com/api/oauth2/authorize?client_id=801501916810838066&permissions=268815424&scope=bot)

## Mechanics

### Basic Mechanics

You can use the command `$challenge` to challenge the bot to a game of chess.

Use `$move` to make a move. Make sure your move is in SAN (Standard Algebraic Notation)

Use `$view` to view your game.

### Chess Bot engine

Chess Bot uses a custom built engine to determine which moves it plays. (It's not very good though, because I built it).

The default time it thinks for is 30 seconds, although you can specify otherwise with the `-t` flag when using `$challenge`.

For example, `$challenge -t 60` to make the bot think for one minute.

### Time

To prevent people from abandoning a the game without loss of rating, you will automatically resign if you do not make a move for 3 days.

You will receive a warning when you only have 1 day left.

Use `$time` to see how much time you have left.

## Commands

### Playing

- challenge: Challenges Chess Bot to a game

- fen:       Sends current game in FEN format

- move [move]:      Plays [move] against the computer

- resign:    Resigns the game

- view:      Views your current game

- time: Sends how much time you have left.
  
### Moderation

These commands require special permissions

- abort:     Aborts a game. At least "Debugger" in Chess Bot support server required.

- refund [user] [points]: Refunds [user] [points] amount of rating points. At least "Moderator" in Chess Bot support server required.

- prefix [prefix]: Makes or changes the server's server specific prefix. Must have administrator permission in the server.

### Other

- botinfo:   Sends basic info and stats about the bot

- ping:      Sends "Pong!" and gives latency

- rating:    Tells you your rating

- leaderboard: Shows top rated players

- rank: Shows your rank out of all rated players

- help:      Sends a message with all of the commands
