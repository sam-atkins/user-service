import coverage
import unittest

from flask.cli import FlaskGroup

from src import create_app, db
from src.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.coverage(
    branch=True,
    include='src/*',
    omit=[
        'src/tests/*',
        'src/config.py',
    ])
COV.start()


@cli.command()
def cov():
    """Runs the unit tests with coverage"""
    tests = unittest.TestLoader().discover('src/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    """Seeds the database"""
    db.session.add(
        User(username='sam', email="sam@example.com", password="weakpassword"))
    db.session.add(
        User(
            username='sammi',
            email="sammi@example.com",
            password="weakpassword"))
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('src/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
