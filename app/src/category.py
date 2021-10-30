#!/usr/bin/env python3

from table import Table


class Category(Table):
    TABLE = 'CATEGORIES'
    PK = 'ID'
    UNIKEYS = ['NAME']
    CREATE_TABLE_QUERY = f"""
    CREATE TABLE IF NOT EXISTS {TABLE}(
    {PK} INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME STRING,
    RETO_WEBHOOK STRING,
    TIP_WEBHOOK STRING
    )
    """
