import os
from hcloud import Client
from hcloud.servers.types import ServerCreate
from bot.db import get_user_balance, deduct_balance

HCLOUD_TOKEN = os.getenv("HCLOUD_TOKEN")
client = Client(token=HCLOUD_TOKEN)

def create_server(user_id: int, server_type: str, image: str = "ubuntu-22.04"):
    price = get_server_price(server_type)
    
    if get_user_balance(user_id) < price:
        return {"error": "موجودی کافی نیست"}
    
    server = client.servers.create(
        name=f"hetz-{user_id}-{server_type}",
        server_type=server_type,
        image=image,
        location="nbg1" # نورنبرگ آلمان
    )
    
    deduct_balance(user_id, price)
    
    return {
        "id": server.server.id,
        "name": server.server.name,
        "ip": server.server.public_net.ipv4.ip,
        "root_password": server.root_password
    }

def get_servers(user_id: int):
    all_servers = client.servers.get_all()
    return [s for s in all_servers if str(user_id) in s.name]

def get_server_price(server_type: str) -> float:
    prices = {
        "cx22": 2.99,
        "cx32": 5.83,
        "cx42": 11.89
    }
    return prices.get(server_type, 0)

def reboot_server(server_id: int):
    server = client.servers.get_by_id(server_id)
    if server:
        server.reboot()
        return True
    return False
