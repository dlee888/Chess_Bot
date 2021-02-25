import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    return stdout, stderr, f'[{cmd!r} exited with {proc.returncode}]', proc.returncode

async def main():
    while True:
        print('Restarting')
        out, err, status, code = await run('python3.9 Chess_Bot.py')
        print(out)
        print(err)
        print(status)
        if code != 0:
            return

asyncio.run(main())