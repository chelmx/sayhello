# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import random
import datetime
import click

from sayhello import app, db
from sayhello.models import User, Message


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages, default is 20.')
def forge(count):
    """Generate fake messages."""
    from faker import Faker

    db.drop_all()
    db.create_all()

    fake = Faker()
    click.echo('Working...')

    user = User(
        username='lguujg'
    )
    user.set_password('lguujg')
    db.session.add(user)
    db.session.commit()
    click.echo('Created user lguujg.')

    user_count = User.query.count()

    for i in range(count):
        start_date = datetime.datetime(datetime.datetime.now().year - 1, 1, 1, 0, 0, 0)
        end_date = datetime.datetime.now()
        message = Message(
            name=fake.name(),
            color=f"#{random.randint(0, 0xFFFFFF):06x}",
            body=fake.sentence(),
            reviewed=True,
            timestamp=fake.date_time_between(start_date=start_date, end_date=end_date),
            user=User.query.get(random.randint(1, user_count))
        )
        db.session.add(message)
    db.session.commit()
    click.echo('Created %d fake messages.' % count)

    message_count = Message.query.count()

    for i in range(int(count * 0.5)):
        replied = Message.query.get(random.randint(1, message_count))
        start_date = replied.timestamp
        end_date = datetime.datetime.now()
        message = Message(
            name=fake.name(),
            color=f"#{random.randint(0, 0xFFFFFF):06x}",
            body=fake.sentence(),
            reviewed=True,
            timestamp=fake.date_time_between(start_date=start_date, end_date=end_date),
            root_id=replied.id,
            user=User.query.get(random.randint(1, user_count)),
            replied=replied,
        )
        db.session.add(message)
    db.session.commit()
    click.echo('Created %d fake message replies.' % int(count * 0.5))

    message_count = Message.query.count()

    for i in range(int(count * 0.1)):
        replied = Message.query.get(random.randint(count + 1, message_count))
        start_date = replied.timestamp
        end_date = datetime.datetime.now()
        message = Message(
            name=fake.name(),
            color=f"#{random.randint(0, 0xFFFFFF):06x}",
            body=fake.sentence(),
            reviewed=True,
            timestamp=fake.date_time_between(start_date=start_date, end_date=end_date),
            root_id=replied.root_id,
            user=User.query.get(random.randint(1, user_count)),
            replied=replied,
        )
        db.session.add(message)
    db.session.commit()
    click.echo('Created %d fake message replies.' % int(count * 0.1))
