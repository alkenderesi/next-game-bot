# Config guide

Setting up the application requires the following 2 files inside the `config` directory:
* token.txt
* games.json

## token.txt

The `token.txt` file stores the [Discord Token](https://discord.com/developers/docs/getting-started#configuring-your-bot) for your bot.  
No special formatting is needed, create the file and paste the token.

## games.json

The `games.json` file stores the list of games available for the polls.  
Keys represent the short names of the games, and their corresponding values represent the full names of the games.

Example:

```json
{
    "game": "Full Name of the Game",
    "another": "Another Game"
}
```
