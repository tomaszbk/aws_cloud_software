from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
