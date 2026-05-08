from api.database import SessionLocal

def pegar_sessao():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()