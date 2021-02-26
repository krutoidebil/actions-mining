#!/usr/bin/env python3
import socket, hashlib, urllib.request, time, os, sys

soc = socket.socket()
soc.settimeout(10)

username = "httsmvkcom"
UseLowerDiff = False 

while True:
    try:
        serverip = "https://mhcoin.s3.filebase.com/Pool.txt"  # Serverip file
        with urllib.request.urlopen(serverip) as content:
            content = (
                content.read().decode().splitlines()
            )  
        pool_address = content[0] 
        pool_port = content[1] 

        soc.connect((str(pool_address), int(pool_port)))
        server_version = soc.recv(3).decode()
        print("Версия сервера:", server_version)
        while True:
            if UseLowerDiff:
                soc.send(
                    bytes("JOB," + str(username) + ",MEDIUM", encoding="utf8")
                )  
            else:
                soc.send(
                    bytes("JOB," + str(username), encoding="utf8")
                )  
            job = soc.recv(1024).decode()  
            job = job.split(",")  
            difficulty = job[2]

            for result in range(
                100 * int(difficulty) + 1
            ): 
                ducos1 = hashlib.sha1(
                    str(job[0] + str(result)).encode("utf-8")
                ).hexdigest()
                if job[1] == ducos1:
                    soc.send(
                        bytes(str(result) + ",,Github Actions", encoding="utf8")
                    )  
                    feedback = soc.recv(1024).decode()
                    if feedback == "GOOD":
                        print("[Accepted!] Решение:", result, "Сложность:", difficulty)
                        break
                    elif feedback == "BAD":
                        print("[Rejected!!!] Решение:", result, "Сложность:", difficulty)
                        break
    except Exception as e:
        os._exit(1)
