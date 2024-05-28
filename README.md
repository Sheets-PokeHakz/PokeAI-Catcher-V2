# Poke AI Catcher V2

- Automatic Webhook Logging
- Poketwo AI Autocatcher With Advanced Spam Features
- Had Commands Like `start` And `stop` For Spamming & Much More

## Installation
1. Install Python 3.10
2. Install `discord.py-self`, `tensorflow`, `pillow` & `discord-webhook`
3. Put The Token, Webook Link, Prefix And Channel Ids In `config.json`
4. Run `Main.py`

### Example Cofig.json
```json
{
    "BOT": {
        "Prefix": ".",
        "Token": [
            "Bot Token"
        ]
    },
    "SPAM": {
        "Spam": "Enabled", // Enable Or Disable Spam
        "Channel": 122313213 //Spam Channel ID,
        "Intervals": [
            3,
            3.2,
            3.5,
            3.8,
            4,
            4.2,
            4.5,
            4.8,
            5,
            5.2,
            5.5,
            5.8,
            6
        ]
    },
    "CATCH": {
        "Intervals": [
            1.0,
            1.2,
            1.3,
            1.4,
            1.5,
            1.6,
            1.7,
            1.8,
            1.9,
            2.0
        ],
        "Incense": "False", // For Only Incense
        "Count": 8
    },
    "GUILDS": {
        "Guilds": [
            2132131313 //Allowed Guild ID
        ]
    },
    "WEBHOOK": {
        "Webhook": "Webhook URL"
    }
}
```
   
