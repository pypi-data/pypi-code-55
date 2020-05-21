from pymongo import MongoClient


class Mongodb:
    def __init__(self, port):
        self.client = MongoClient(port=port)
        self.db = self.client.icmp

    def add_to_db(self, icmp_src, icmp_dest):
        """
        Adds data to mongo db
        :param icmp_src: source ip address
        :param icmp_dest: destination ip address
        :return:
        """
        business = {
            'source': icmp_src,
            'destination': icmp_dest,
        }
        self.db.icmp.insert_one(business)
        print('Adding src: {} dst: {} '.format(icmp_src, icmp_dest))
        print('✓ Finished adding to db.')


if __name__ == "__main__":
    mongo = Mongodb(27017)
    mongo.add_to_db(10000, 20000)
