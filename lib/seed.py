#!/usr/bin/env python3
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, freebie

# Script goes here!
if __name__ == '__main':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Delete existing records from the tables
    session.query(freebie).delete()
    session.query(Dev).delete()
    session.query(Company).delete()

    fake = Faker()
    freebies = []
    companies = []
    developers = []

    for i in range(10):
        freebie1 = freebie(
            item_name=fake.unique.name(),
            value=random.randint(0, 100)
        )
        freebies.append(freebie1)

    for i in range(10):
        company = Company(
            name=fake.unique.name(),
            founding_year=random.randint(1900, 2023)
        )
        companies.append(company)

    for i in range(10):
        developer = Dev(
            name=fake.unique.name(),
        )
        developers.append(developer)

    session.add_all(freebies)
    session.add_all(companies)
    session.add_all(developers)

    session.commit()

    session.close()
