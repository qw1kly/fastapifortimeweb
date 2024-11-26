import asyncio
import aiomysql


async def check_pass(m):
    connect = await aiomysql.connect(host='176.53.162.45', port=3306, user='gen_user', password='5\>Aj=nP*!Ga)s', db='default_db')
    sel = 'SELECT * FROM password'
    async with connect.cursor() as cur:
        await cur.execute(sel)
        auths = await cur.fetchall()
        for i in auths:
            if str(m[0]) == str(i[0]) and m[1]==i[1]:
                connect.close()
                return True
        connect.close()
        return False
