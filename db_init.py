import sqlite3
def initer():
    conn = sqlite3.connect("data.db")
    try:
        conn.execute("CREATE TABLE SMETER("+
            "RECVTS REAL,"+
            "VOLTAGE REAL,"+
            "CURRENT REAL,"+
            "PERIODSAMPLE REAL,"+
            "SAMPLECOUNT INTEGER,"+
            "PHASEANGLE REAL,"+
            "POWERFACTOR REAL,"+
            "FREQUENCY REAL,"+
            "POWER REAL,"+
            "ENERGY REAL,"+
            "TARIFF REAL)")
        conn.commit()
    except:
        pass
    finally:
        conn.close()
