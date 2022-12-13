import asyncio
import config as config 
import os
import time
from pyrogram import Client
from rich.console import Console
from random import randint
import socks
console =Console()



async def main():
    console.print("[bold green]Привет. Эта программа добавляет аккаунты")
    console.print("[bold green]Чтобы продолжать добавлять аккаунты, жмите Enter.\n Чтобы закончить - жмите или 'n' или 'н'")
    proxies=[]
    with open("config/proxies.txt", mode="r+") as file:
        for pr in file.readlines():
            proxies.append(pr)
    print(proxies)
    while True:        
        with open("config/sessions.txt", mode="r+") as file:
            proxy_id=(len(file.readlines()))//10
            print(proxy_id)
        if len(proxies)<proxy_id:
            print("Недостаточно прокси: имеется {0} штуки, но должно быть минимум {1}".format(len(proxies),proxy_id))
            break
        prox=proxies[proxy_id].split(":")
        proxy = {
         "scheme": config.proxy_type,
         "hostname": prox[0],
         "port": int(prox[1]),
         "username": prox[2],
         "password": prox[3]
        }
        print(proxy)
        try:
            async with Client(f"{config.folder}my_acc",config.api_id, config.api_hash, in_memory=True, proxy=proxy, ipv6=config.ipv6) as app:
                with open("config/sessions.txt", mode="a+") as file:
                    session=await app.export_session_string()
                    file.write(f"{session}\n")              
        except Exception as e:
            print(e)
        en=console.input("[purple]Добавить еще?")
        if en == 'n' or en == "н":
            break
os.system("cls")
asyncio.run(main())
