## Disclaimer
This repository is for educational purposes only  
I do not have any intention of using this to harm anyone

---
## How it works

[`GameHelper`](files\\GameHelper)
- Scheduled every 10 minutes
- Fetches the DNS and chrome search history (all chrome profiles) of the target
- Sends the data using a discord bot

[`internal`](files\\internal)
- `config.ps1` is scheduled every 1 minute, running a bot if it isn't already running
- The bot sends commands to the target's computer, giving remote control
- The bot is also responsible for deleting all malware files from the computer

---

## Notes
`main.py` and `passwords.py` were converted into executables using [pyinstaller](https://pypi.org/project/pyinstaller/), which are not included in this repository for obvious security reasons

The tokens and channel IDs for the bots have also been removed from source code
