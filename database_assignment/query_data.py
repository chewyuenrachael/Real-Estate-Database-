
def main():

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
