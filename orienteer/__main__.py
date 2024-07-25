import asyncio
import os
import subprocess
import platform


async def run_script(module_name: str):
    system = platform.system()
    if system == 'Windows':
        subprocess.Popen(['start', 'cmd', '/k', 'py', module_name], shell=True)
    elif system == 'Linux':
        subprocess.call(['gnome-terminal', '--', 'py', '-m', module_name])
    else:
        print(f'Your os ({system}) isn\'t supported yet')


async def main():
    await run_script('orienteer.api')
    await run_script('orienteer.bot')
    await run_script('orienteer.checker')


if __name__ == '__main__':
    asyncio.run(main())
