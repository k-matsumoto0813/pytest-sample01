#!/bin/sh

pip install pytest pytest-cov SQLAlchemy psycopg2-binary

pytest --setup-show tests/ -v -s --cov=.
exit $?
