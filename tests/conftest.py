import time
import pytest
# DELETE
import docker
from sqlalchemy import create_engine

# ADD
import os

@pytest.fixture()
def pg_conf():
    """PostgreSQLの設定を管理"""
    # CHANGE
    # host = '127.0.0.1'
    # port = 5432
    # dbname = 'pytest'
    # user = 'testuser'
    # password = 'test'
    host = os.environ['DB_HOST']
    port = os.environ['DB_PORT']
    dbname = os.environ['DB_NAME']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']

    pg_conf = {'host': host,
               'port': port,
               'dbname': dbname,
               'user': user,
               'password': password,
               'url': f'postgresql://{user}:{password}@{host}/{dbname}'}
    return pg_conf


@pytest.fixture()
def engine(pg_conf):
    return create_engine(pg_conf['url'])


@pytest.fixture(autouse=True)
def pg_container(pg_conf):
    """PostgreSQLコンテナを起動する"""
    # CHANGE
    client = docker.from_env()
    container = client.containers.run(image='postgres:11.6-alpine',
                                      tty=True,
                                      detach=True,
                                      auto_remove=True,
                                      environment={'POSTGRES_DB': pg_conf['dbname'],
                                                   'POSTGRES_USER': pg_conf['user'],
                                                   'POSTGRES_PASSWORD': pg_conf['password']},
                                      ports={pg_conf['port']: '5432'})
    # コンテナが準備完了になるまで待機
    while True:
        log = container.logs(tail=1)
        if 'database system is ready to accept connections' in log.decode():
            break
        time.sleep(0.5)
    yield  # ここでテストに遷移
    container.kill()
#     yield
