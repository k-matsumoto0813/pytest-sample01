from sqlalchemy.orm import Session
from models import Base, Staff
from main import add_staff


def test_add(engine):
    # レコードを1件追加
    Base.metadata.create_all(bind=engine)  # テーブルを作成
    add_staff(engine=engine,
              name='alice')
    # 追加したレコードをチェック
    session = Session(bind=engine)
    assert session.query(Staff.id).filter_by(name='alice').first() == (1,)
    session.close()
