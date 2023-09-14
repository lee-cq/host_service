#!/bin/env python3
# coding: utf8
"""
@File Name  : bin/send_ip_to_feishu.py
@Author     : LeeCQ
@Date-Time  : 2023/9/14 09:47

将ip推送到飞书
"""
import logging
import re
import socket
import subprocess
import time

import typer

import _base
from tools import getencoding

_base.logging_configurator("send_ip_to_feishu", console_print=True)

logger = logging.getLogger("host-service.bin.send-ip-to-feishu")
app = typer.Typer()

HOSTNAME = socket.gethostname()


def get_ips() -> str:
    """获取本机的所有ip地址"""
    proc = subprocess.run(
        "ip addr | grep inet", shell=True, check=True, stdout=subprocess.PIPE
    )

    return "\n".join(
        re.findall(
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", proc.stdout.decode(getencoding())
        )
    )


def wait_network(host="feishu.cn"):
    """等待网络连接"""
    while True:
        try:
            proc = subprocess.run(["ping", "-c", "1", "-w", "1", host])
            if proc.returncode == 0:
                return
        except:
            logger.warning("Can not connect to %s", host)
            time.sleep(1)
            pass


@app.command()
def send_message(chat_id="oc_935401cad663f0bf845df98b3abd0cf6"):
    start = time.time()
    wait_network()
    wait_time = int(time.time() - start)

    from feishu.im_adapter import IMAdapter
    from feishu.client import client

    msg_content = f"设备 {HOSTNAME} 新的IP地址：\n {get_ips()}\nwait time: {wait_time}"

    im = IMAdapter(client)
    resp = im.send_text_message_to_chat(chat_id, msg_content)
    logger.info(resp)


if __name__ == "__main__":
    app()
