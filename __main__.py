import asyncio
import os
import subprocess


async def run_script(script_name: str, keep: bool):
    if keep:
        subprocess.Popen(["start", "cmd", "/k", "py", os.path.join(os.getcwd(), script_name)], shell=True)
    else:
        subprocess.Popen(["start", "cmd", "py", os.path.join(os.getcwd(), script_name)], shell=True)


async def main():
    await run_script("core/bot.py", keep=True)
    await run_script("core/bans.py", keep=True)
    await run_script("core/api.py", keep=True)


if __name__ == "__main__":
    asyncio.run(main())
