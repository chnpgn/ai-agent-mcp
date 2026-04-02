"""The MCP tools module"""

import sqlite3


def get_users():
    """Get users from db"""
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    conn.close()

    return rows


def calculate(a: int, b: int):
    """Addition of two integers"""
    return a + b


def search_docs(query: str):
    """"Search company documents"""
    with open("docs/company_docs.txt", "r", encoding='utf-8') as f:
        text = f.read()

    if query.lower() in text.lower():
        return "Found information in company docs"

    return "No results"
