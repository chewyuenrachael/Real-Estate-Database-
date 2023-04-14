# Real-Estate-Database-

## Overview 

This is a database system for a large franchised real estate company. This company has multiple offices located all over the country, where each office is responsible for selling houses in a particular area. An estate agent can be associated with one or more offices.

## Execution (Python)

These are the recommended commands for macOS:

`
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 create.py
python3 insert_data.py
python3 query_data.py
python3 test_data.py
`

Recommended commands for Windows:

`
python3 -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
python3 create.py
python3 insert_data.py
python3 query_data.py
python3 test_data.py
`

## Summary of the Database 

Each of the listed houses will capture the following details: seller details, # of bedrooms, # of bathrooms, listing price, zip code, date of listing, the listing estate agent, and the appropriate office.

Whenever a house is sold the following activities will be performed:
The estate agent commission needs to be calculated. This happens on a sliding scale:
1. For houses sold below $100,000 the commission is 10%
2. For houses between $100,000 and $200,000 the commission is 7.5%
3. For houses between $200,000 and $500,000 the commission is 6%
4. For houses between $500,000 and $1,000,000 the commission is 5%
5. For houses above $1,000,000 the commission is 4%
All appropriate details related to the sale must be captured, ie. at least: buyer details, sale price, date of sale, the selling estate agent.
The original listing must be marked as sold.

## Data Queries

Every month, 5 reports need to be generated. Hence, the following queries will be executed to compile information from the database:
1. Find the top 5 offices with the most sales for that month.
2. Find the top 5 estate agents who have sold the most for the month (include their contact details and their sales details so that it is easy to contact them and congratulate them).
3. Calculate the commission that each estate agent must receive and store the results in a separate table.
4. For all houses that were sold that month, calculate the average number of days on the market.
5. For all houses that were sold that month, calculate the average selling price

## Testing 

Fictitious data is created to test my code, and ensure that the correct results are calculated from my code.

## Application of data normalization, indices and transactions:

The database is created with four tables - Properties, Buyers, Offices, and Agents - using SQLAlchemy. It then inserts some data into the Properties table and defines a transaction function for adding purchases of properties to the database.

#### Normalization: 
I normalized the data by creating separate tables for each of the 4 main key categories: buyers, offices, agents, and properties. Each table has its own primary key ID, which makes it easier for identification of each unique instance of each object. This database is normalized to the third normal form, whereby there is no transitive dependency. No non-primary-key attribute is transitively dependent on the primary key. Foreign keys are used to link each table together which ensures that there is no redundant or duplicated data. 

#### Indices:
Indexing is used, for instance in the 'name' and 'address' columns of the Buyers and Offices tables. This optimizes query performance because it makes the columns faster to query by creating pointers to where data is stored within this database.

#### Transactions: 
I implemented a transaction function that takes in the following arguments: ID of a property, the ID of a buyer, and the date of purchase. It updates the status of the property in the Properties table, calculates the cost and commission for the purchase using a sliding scale, and inserts the details of the purchase into the Purchases table. This insertion and updating process occurs in  multiple tables, and is a function that is often used, in order to abstract the operation for users of the system. This function has a built-in commit command, which implements the use of transactions with ease. The use of transactions ensures that the data in the database remains consistent and accurate across all tables.
