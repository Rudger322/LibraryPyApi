from app.database.db import  engine, metadata

def create_tables():
    engine.echo = False
    metadata.drop_all(engine)
    metadata.create_all(engine)
    engine.echo = True
