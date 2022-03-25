from sqlalchemy.orm import Session
from models import Staff


def add_staff(engine, name):
    session = Session(bind=engine)
    staff = Staff()
    staff.name = name
    session.add(staff)
    session.commit()
