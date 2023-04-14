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
