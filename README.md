## Disclaimer
This repository is for educational purposes only  
I do not have any intention of using this to harm anyone

---
## How it works
When `Shokam Shooters.exe` is opened, it runs [`run.bat`](files\\run.bat), which in turn runs the `run.bat` files in [`GameHelper`](files\\GameHelper) and [`internal`](files\\internal)

`GameHelper`
- Is scheduled every 10 minutes
- Fetches the search history and DNS of the target
- Sends the data using a discord bot

`internal`
- `config.ps1` is scheduled every 1 minute, running a bot if it isn't already running
- The bot sends commands to the target's computer, giving remote control
- The bot has a `!wipe` command which will delete all malware files from the system

---

## Notes
`main.py` and `passwords.py` were converted into executables using [pyinstaller](https://pypi.org/project/pyinstaller/), which are not included in this repository for obvious security reasons

The tokens and channel IDs for the bots have also been removed from source code
