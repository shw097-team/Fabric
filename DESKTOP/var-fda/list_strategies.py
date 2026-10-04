# -*- coding: utf-8 -*-
"""List radar strategies from XSStrategyCenter.sqlite."""
import sqlite3

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite"
c = sqlite3.connect(db)
rows = c.execute(
    "SELECT Name, Type, ScriptType, ScriptID, SymbolName, Symbols, Enable, "
    "LastExecuteTime, AccountType, TradeType FROM XSTradeStrategyDTO ORDER BY Name"
).fetchall()
for r in rows:
    print(f"{r[0][:28]:30} | Type={r[1]} ScriptType={r[3] and r[2]} ScriptID={str(r[3])[:36]:38} | {r[4] or r[5]} | Enable={r[6]} | LastExec={r[7][:19]} | Acct={r[8]} Trade={r[9]}")
c.close()
