# -*- coding: utf-8 -*-
import asyncio
import http.cookies
import random
from typing import *

import aiohttp

import blivedm
import blivedm.models.web as web_models
import json
import datetime

import os

# 读取 config.json
config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

TEST_ROOM_IDS = config.get("TEST_ROOM_IDS", [])
SESSDATA = config.get("SESSDATA", "")



session: Optional[aiohttp.ClientSession] = None


async def main():
    init_session()
    try:
        await run_single_client()
        await run_multi_clients()
    finally:
        await session.close()


def init_session():
    cookies = http.cookies.SimpleCookie()
    cookies['SESSDATA'] = SESSDATA
    cookies['SESSDATA']['domain'] = 'bilibili.com'

    global session
    session = aiohttp.ClientSession()
    session.cookie_jar.update_cookies(cookies)


async def run_single_client():
    """
    演示监听一个直播间
    """
    room_id = random.choice(TEST_ROOM_IDS)
    client = blivedm.BLiveClient(room_id, session=session)
    handler = MyHandler()
    client.set_handler(handler)

    client.start()
    try:
        # 演示5秒后停止
        await asyncio.sleep(5)
        client.stop()

        await client.join()
    finally:
        await client.stop_and_close()


async def run_multi_clients():
    """
    演示同时监听多个直播间
    """
    clients = [blivedm.BLiveClient(room_id, session=session) for room_id in TEST_ROOM_IDS]
    handler = MyHandler()
    for client in clients:
        client.set_handler(handler)
        client.start()

    try:
        await asyncio.gather(*(
            client.join() for client in clients
        ))
    finally:
        await asyncio.gather(*(
            client.stop_and_close() for client in clients
        ))


class MyHandler(blivedm.BaseHandler):
    def __init__(self):
        super().__init__()
        self.queue = []  # 排队列表
	
	# 动态读取关键词
        self.join_words = config.get("join_words", [])
        self.pop_words = config.get("pop_words", [])

    # ---------- 工具函数 ----------
    def save_json(self, filename, data: dict):
        """追加保存 JSON"""
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    def save_queue(self):
        """保存队列到 queue.json"""
        with open("queue.json", "w", encoding="utf-8") as f:
            json.dump(self.queue, f, ensure_ascii=False, indent=2)

    def in_queue(self, uid):
        """是否已经排队"""
        return any(u["uid"] == uid for u in self.queue)

    def add_to_queue(self, uid, uname, face=None):
        """加入队列（带防重复）"""
        if self.in_queue(uid):
            print(f"【排队】{uname} 已在队列中，忽略")
            return

        entry = {
            "uid": uid,
            "uname": uname,
            "face": face,
            "join_time": datetime.datetime.now().isoformat()
        }
        self.queue.append(entry)
        self.save_queue()
        print(f"【排队】{uname} 已加入队列（当前人数 {len(self.queue)}）")

    def pop_self(self, uid):
        """只允许自己出队"""
        for i, user in enumerate(self.queue):
            if user["uid"] == uid:
                u = self.queue.pop(i)
                self.save_queue()
                print(f"【排队】{u['uname']} 自己离开队列（剩余 {len(self.queue)}）")
                return u
        print(f"【排队】UID={uid} 不在队列中")
        return None

    # ---------- B站回调 ----------
    def _on_heartbeat(self, client, message):
        print(f'[{client.room_id}] 心跳')

    def _on_danmaku(self, client, message):
        uid = message.uid
        uname = message.uname
        msg = message.msg.strip()
        face = getattr(message, "face", None)

        # 保存弹幕
        record = {
            "time": datetime.datetime.now().isoformat(),
            "room_id": client.room_id,
            "type": "danmaku",
            "uid": uid,
            "uname": uname,
            "face": face,
            "msg": msg
        }
        self.save_json("danmu.json", record)
        print(f"[{client.room_id}] {uname}: {msg}")

        
        # --- 出队关键词（优先判断） ---
        if any(w in msg for w in self.pop_words):
            self.pop_self(uid)
            return

        # --- 排队关键词 ---
        if any(w in msg for w in self.join_words):
            self.add_to_queue(uid, uname, face)

    def _on_gift(self, client, message):
        uid = message.uid
        uname = message.uname
        face = getattr(message, "face", None)

        record = {
            "time": datetime.datetime.now().isoformat(),
            "room_id": client.room_id,
            "type": "gift",
            "uid": uid,
            "uname": uname,
            "face": face,
            "gift_name": message.gift_name,
            "num": message.num,
            "coin_type": message.coin_type,
            "total_coin": message.total_coin
        }
        self.save_json("gift.json", record)
        print(f"[{client.room_id}] {uname} 赠送 {message.gift_name}x{message.num}")

    def _on_user_toast_v2(self, client, message):
        if message.source != 2:
            uid = message.uid
            uname = message.username
            face = getattr(message, "face", None)

            record = {
                "time": datetime.datetime.now().isoformat(),
                "room_id": client.room_id,
                "type": "guard",
                "uid": uid,
                "uname": uname,
                "face": face,
                "guard_level": message.guard_level
            }
            self.save_json("guard.json", record)
            print(f"[{client.room_id}] {uname} 上舰 LV{message.guard_level}")

    def _on_super_chat(self, client, message):
        uid = message.uid
        uname = message.uname
        face = getattr(message, "face", None)

        record = {
            "time": datetime.datetime.now().isoformat(),
            "room_id": client.room_id,
            "type": "superchat",
            "uid": uid,
            "uname": uname,
            "face": face,
            "price": message.price,
            "message": message.message
        }
        self.save_json("superchat.json", record)
        print(f"[{client.room_id}] SC ¥{message.price} {uname}: {message.message}")

if __name__ == '__main__':
    asyncio.run(main())
