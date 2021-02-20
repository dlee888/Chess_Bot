import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    return stdout, stderr, f'[{cmd!r} exited with {proc.returncode}]'

async def main():
    while True:
        f = open('status.txt')
        lines = f.readlines()
        print(lines)
        f.close()

        if lines[0] != 'RUNNING\n':
            print(f'Status code "{lines[0].strip()}" found')
            print('Restarting')
            out, err, status = await run('python3.9 Chess_Bot.py')
            print(out)
            print(err)
            print(status)

        f = open('status.txt', 'w')
        f.write('CHECKING\n')
        f.close()

        await asyncio.sleep(6)

asyncio.run(main())