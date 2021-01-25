import os
import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    return stdout, stderr, f'[{cmd!r} exited with {proc.returncode}]'

async def main():
    while True:
        f = open('status.txt')
        lines = f.readlines()
        print(lines)
        f.close()

        if lines[0] != 'RUNNING\n':
            print(f'Status code "{lines[0]}" found')
            print('Restarting')
            out, err, status = await run('python3.9 Jamin_bot.py')
            print(out)
            print(err)
            print(status)

        f = open('status.txt', 'w')
        f.write('CHECKING\n')
        f.close()

        await asyncio.sleep(10)

asyncio.run(main())