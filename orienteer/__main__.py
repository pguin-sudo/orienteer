import asyncio
import os
import subprocess
import platform


async def run_script(script_name: str):
    system = platform.system()
    if system == 'Windows':
        subprocess.Popen(['start', 'cmd', '/k', 'py',
                         os.path.join(os.getcwd(), script_name)], shell=True)
    elif system == 'Linux':
        subprocess.call(
            ['gnome-terminal', '-x', os.path.join(os.getcwd(), script_name)])
    else:
        print(f'Your os ({system}) isn\'t supported yet')


async def main():
    await run_script('-m api')
    await run_script('-m bot')
    await run_script('-m checker')


if __name__ == '__main__':
    asyncio.run(main())
