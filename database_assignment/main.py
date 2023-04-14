
# main.py is a compilation of create, insert, and query files.

# 1 - First, we import the modules that we need
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import create_engine, case, func, Column, Text, Integer, \
    ForeignKey, join, text, extract, Date, Boolean, extract, select

import pandas as pd
import numpy as np

# import datetime to show date of purchase
from datetime import datetime as dt

# 2 - Next, we have to initialise the database

# create engine
engine = create_engine('sqlite:///database.db')
engine.connect()
Base = declarative_base()

# 3 - To create the database, we need to create a separate class
# for each main Object in the database

# Property class keeps track of details of each property
# This includes crucial information including the office and agent
# that are linked to each property


class Property(Base):
    __tablename__ = 'Properties'
    id = Column(Integer, primary_key=True)
    address = Column(Text)
    office_id = Column(Integer, ForeignKey('Offices.id'))
    agent_id = Column(Integer, ForeignKey('Agents.id'))
    seller_id = Column(Integer, ForeignKey('Buyers.id'))
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    listing_cost = Column(Integer, nullable=False)
    zip = Column(Integer)
    date_listed = Column(Date)
    sold = Column(Boolean)

# Since one instance of an Agent
# is associated to many instances of multiple Offices
# Agent to Office has a one-to-many relationship

# Buyer class tracks the ID and name of each buyer


class Buyer(Base):
    __tablename__ = 'Buyers'
    id = Column(Integer, primary_key=True)
    name = Column(Text, index=True)

# Office class tracks the ID and location of each office


class Office(Base):
    __tablename__ = 'Offices'
    id = Column(Integer, primary_key=True)
    address = Column(Text, index=True)

# Agent class tracks the ID and name of each agent


class Agent(Base):
    __tablename__ = 'Agents'
    id = Column(Integer, primary_key=True)
    name = Column(Text, index=True)
    email = Column(Text, index=True)

# Purchase class compiles all details for each purchase


class Purchase(Base):
    __tablename__ = 'Purchases'
    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('Properties.id'))
    buyer_id = Column(Integer, ForeignKey('Buyers.id'))
    purchase_cost = Column(Integer, nullable=False)
    purchase_date = Column(Date)
    purchase_commission = Column(Integer)


# Create tables
Base.metadata.create_all(bind=engine)

# Function to add a transaction to the database


def transaction(property, buyer, date):

    # Create Session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Update the status of the property
    property_row = session.query(Property).filter(Property.id == property)
    property_row.update({Property.sold: True})

    # Calculate cost and comission
    cost = session.query(Property.listing_cost).filter(Property.id == property)
    cost = 0

    # these percentages are taken from the sliding scale instructions

    commission = case(
        (Property.listing_cost < 100000, 0.01),
        (Property.listing_cost < 200000, 0.075),
        (Property.listing_cost < 500000, 0.06),
        (Property.listing_cost < 1000000, 0.05),
        (Property.listing_cost > 1000000, 0.04),
    ).label('property_cost')


# check if you should use the app version or the one in ipynb

    commission = session.query(
        Property.listing_cost*commission).filter(Property.id == property)

    # Add Purchase
    session.add(Purchase(
        property_id=property,
        buyer_id=buyer,
        purchase_cost=cost,
        purchase_date=date,
        purchase_commission=commission))

    # Commit Change and close session
    session.commit()
    session.close()

# Insert data into the database


def main():
    # Open Session
    Session = sessionmaker(bind=engine)
    session = Session()

    property_key = [column.key for column in Property.__table__.c][1:]
    property_value = [
        ['Marina Bay', 1, 1, 1, 11, 1, 116003,
            877687, dt(2016, 3, 7), False],
        ['Holland Village', 2, 2, 2, 4, 2, 410030,
            908887, dt(2020, 1, 1), False],
        ['Queenstown', 3, 3, 2, 2, 3, 31002, 982634, dt(2017, 2, 8), False],
        ['Bukit Timah', 4, 4, 3, 4, 2, 56240, 488036, dt(2020, 7, 4), False],
        ['Serangoon', 5, 4, 3, 5, 6, 75430, 255490, dt(2021, 1, 2), False],
        ['Tanjong Pagar', 2, 5, 5, 1, 5, 87364,
            544726, dt(2021, 8, 8), False]
    ]

    buyer_key = [column.key for column in Buyer.__table__.c][1:]
    buyer_value = [['Thomas Linck'], ['Paulina Lee'], ['Minjae Kim'],
                   ['Jan Johannsman'], ['Lucille Glassman'], ['Chia Zhi Zhi']]

    office_key = [column.key for column in Office.__table__.c][1:]
    office_value = [['Marina Boulevard 43'], ['48 Lor Mambong'], ['2 Fusionopolis Way'],
                    {'Greenwood Avenue 51'}, ['14 Lorong Liew Lian'], ['9 Cantonment Road']]

    agent_key = [column.key for column in Agent.__table__.c][1:]
    agent_value = [['Yelani Sawithra', 'yelani@gmail.com'], ['Rachel Tey', 'tey16253@gmail.com'], ['Ching Wan Kang', 'wankang@gmail.com'],
                   ['Cheng Hong Jiun', 'honghong@gmail.com'], ['Ethan Tan', 'ethantan43@yahoo.com'], ['Wu Zhihao', 'wuzhihao23@yahoo.com']]

    classes = [Property, Buyer, Office, Agent]
    keys = [property_key, buyer_key, office_key, agent_key]
    values = [property_value, buyer_value, office_value, agent_value]

    # group objects
    num_classes = len(classes)
    for i in range(num_classes):

        # create an empty list to hold grouped objects
        groups = []

        for object in values[i]:

            objects = dict(zip(keys[i], object))
            groups.append(objects)

            for group in groups:
                session.add(classes[i](**group))

                session.commit()
                session.close()

                transaction(1, 4, dt(2023, 3, 1))
                transaction(2, 3, dt(2023, 2, 3))
                transaction(3, 3, dt(2022, 5, 2))
                transaction(4, 4, dt(2021, 8, 2))
                transaction(5, 4, dt(2021, 8, 4))
                transaction(6, 6, dt(2022, 9, 9))

    # Query 1
    # Find the top 5 offices with the most sales for that month.

    '''
    Logic of Query 1:
        1. create variable that calcs the purchases per office
        2. query office details
        3. filter by sold properties
        4. group by office ID
        5. sort by descending order (biggest to smallest count)
    '''

    subquery = session.query(
        Property.office_id,
        func.count(Property.id).label('num_purchases')
    ).filter(
        Property.sold == True
    ).group_by(
        Property.office_id
    ).subquery()

    query_1 = session.query(
        subquery.c.office_id,
        Office.address,
        subquery.c.num_purchases.label('Purchases')
    ).join(
        Office,
        subquery.c.office_id == Office.id
    ).order_by(
        subquery.c.num_purchases.desc()
    ).limit(5)
    print("SHOWING QUERY 1")
    print(pd.read_sql(query_1.statement, session.bind))

    # Query 2
    # Find the top 5 estate agents who have sold the most for the month

    '''
    Logic of Query 2:
        1. create variable that calcs the purchases per agent
        2. query agent details 
        3. filter by sold properties
        4. group by agent ID
        5. sort by descending order (biggest to smallest count)
    '''

    query_2 = session.query(
        Agent.id,
        Agent.name,
        Agent.email,
        func.count(Property.id).label('Purchases')
    ).join(Property, Agent.id == Property.agent_id)\
        .filter(Property.sold == True)\
        .group_by(Agent.id)\
        .order_by(func.count(Property.id).desc())\
        .limit(5)
    print("SHOWING QUERY 2")
    print(pd.read_sql(query_2.statement, session.bind))

    # Query 3
    # Calculate the commission that each estate agent must receive
    # Store the results in a separate table.

    # need to edit this query

    query_3 = session.query(
        Agent.name,
        func.sum(Purchase.purchase_commission).label('Commission')
    ).filter(Property.sold == True)\
        .join(Property)\
        .join(Purchase)\
        .group_by(Agent.id)

    print(pd.read_sql(query_3.statement, session.bind))

    # Query 4
    # For all houses that were sold that month, calculate the average number of days on the market.

    query_4 = text("""
WITH curr_month (year_month) AS ( /* eg: '2021-05' */
    /* using both year and month to not group Jan 2022 with Jan 2023 */
    SELECT STRFTIME('%Y-%m', CURRENT_DATE)
),
     last_month (year_month) AS ( /* doing last month to capture more properties */
         /* '2021-05' -> '2021-05-01' -> 2021-04-30 -> '2021-04' */
         SELECT STRFTIME('%Y-%m', DATE(year_month || '-01', '-1 day')) FROM curr_month
     ),
     sold_last_month AS (
         SELECT Properties.address,
                Properties.date_listed,
                Purchases.purchase_date,
                STRFTIME('%Y-%m', Purchases.purchase_date)                             AS year_month,
                JULIANDAY(Purchases.purchase_date) - JULIANDAY(Properties.date_listed) AS days_on_market
         FROM Properties
                  JOIN Purchases ON Properties.id == Purchases.property_id
         WHERE year_month == (SELECT year_month FROM last_month)

     )
SELECT MIN(year_month)     AS sold_in_month,  /* min for convenience to state month explicitly */
       AVG(days_on_market) AS avg_days_until_sold
FROM sold_last_month
;        """)
    print("SHOWING QUERY 4")
    print(pd.read_sql(query_4, session.bind))

    # Query 5
    # For all houses that were sold that month, calculate the average cost of each property

    '''
    Logic of Query 5:
        1. create variable that calcs the average cost of each property
        2. query based on av. cost
        3. filter by month
    '''

    query_5 = text("""
WITH curr_month (year_month) AS ( /* eg: '2021-05' */
    /* using both year and month to not group Jan 2022 with Jan 2023 */
    SELECT STRFTIME('%Y-%m', CURRENT_DATE)
),
     last_month (year_month) AS ( /* doing last month to capture more properties */
         /* '2021-05' -> '2021-05-01' -> 2021-04-30 -> '2021-04' */
         SELECT STRFTIME('%Y-%m', DATE(year_month || '-01', '-1 day')) FROM curr_month
     ),
     sold_last_month AS (
         SELECT Properties.address,
                Properties.date_listed,
                Purchases.purchase_date,
                Purchases.purchase_cost,
                STRFTIME('%Y-%m', Purchases.purchase_date)                             AS year_month
         FROM Properties
                  JOIN Purchases ON Properties.id == Purchases.property_id
         WHERE year_month == (SELECT year_month FROM last_month)

     )
SELECT MIN(year_month)     AS sold_in_month,  /* min for convenience to state month explicitly */
       AVG(purchase_cost) AS avg_purchase_cost
FROM sold_last_month
;        """)
    print("SHOWING QUERY 5")
    print(pd.read_sql(query_5, session.bind))


main()
