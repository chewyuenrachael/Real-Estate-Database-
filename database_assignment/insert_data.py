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
