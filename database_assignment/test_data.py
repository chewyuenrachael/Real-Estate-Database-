import unittest
from datetime import datetime as dt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from your_module import Agent, Property, Office, Buyer, Purchase, transaction, main


class TestTransaction(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()

        Agent.__table__.create(bind=engine)
        Office.__table__.create(bind=engine)
        Property.__table__.create(bind=engine)
        Buyer.__table__.create(bind=engine)
        Purchase.__table__.create(bind=engine)

        self.agent1 = Agent(name='Alice', email='alice@example.com')
        self.office1 = Office(address='1 Main St.')
        self.buyer1 = Buyer(name='Bob')
        self.property1 = Property(address='123 Main St.',
                                  office_id=self.office1.id,
                                  agent_id=self.agent1.id,
                                  seller_id=self.buyer1.id,
                                  bedrooms=2,
                                  bathrooms=1,
                                  listing_cost=100000,
                                  zip=12345,
                                  date_listed=dt(2022, 4, 11),
                                  sold=False)

        self.session.add_all(
            [self.agent1, self.office1, self.buyer1, self.property1])
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_transaction(self):
        transaction(self.property1.id, self.buyer1.id, dt(2022, 4, 12))

        self.assertEqual(self.property1.sold, True)
        self.assertEqual(len(self.property1.purchases), 1)

    def test_main(self):
        main()

        property_count = self.session.query(Property).count()
        buyer_count = self.session.query(Buyer).count()
        office_count = self.session.query(Office).count()
        agent_count = self.session.query(Agent).count()
        purchase_count = self.session.query(Purchase).count()

        self.assertEqual(property_count, 6)
        self.assertEqual(buyer_count, 6)
        self.assertEqual(office_count, 5)
        self.assertEqual(agent_count, 5)
        self.assertEqual(purchase_count, 6)


if __name__ == '__main__':
    unittest.main()
