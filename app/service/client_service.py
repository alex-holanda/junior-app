from collections import defaultdict
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
from sqlalchemy import func

from app.database import client_table, database

scheduler = AsyncIOScheduler(timezone=utc)


@scheduler.scheduled_job("interval", seconds=10)
async def get_expiration_date_near_end():
    target_date = (datetime.now(timezone.utc) + timedelta(days=3)).date()
    query = client_table.select().where(
        func.date(client_table.c.effective_end_at) == func.date(target_date)
    )

    clients = await database.fetch_all(query)
    if not clients:
        print("Sem clientes para notificar")
        return

    grouped_clients = defaultdict(list)
    for client in clients:
        grouped_clients[client.panel_name].append(client)

    print("-" * 20)
    print("⚠️" + " " * 5 + "ALERTA DE COBRANÇA" + " " * 5 + "⚠️")
    print()
    for panel_name, clients_in_panel in grouped_clients.items():
        print(f"Painel: {panel_name}")
        for client in clients_in_panel:
            print(f"Cliente: {client.name}")
        print("-" * 20)


@scheduler.scheduled_job("interval", seconds=10)
async def buscar_inadimplentes():
    target_date = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    query = client_table.select().where(
        func.date(client_table.c.effective_end_at) == func.date(target_date)
    )

    clients = await database.fetch_all(query)
    if not clients:
        print("Sem clientes para notificar")
        return

    print("👌 Acabando a validade")
    for client in clients:
        print(f"Cliente: {client.name}")
