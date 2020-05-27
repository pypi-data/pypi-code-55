import datetime
import json
import psycopg2
import random
from pynidus.clients import DatabaseClient

class ABTest(DatabaseClient):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def heads_or_tails():
        return random.choice(['A', 'B'])[0]

    def _get_or_create_user_tests(self, user_id, ab_test_id):
        
        conn = self._connect()

        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM ab_tests WHERE user_id='{user_id}' AND ab_test_id='{ab_test_id}'")
        user = cursor.fetchone()

        if not user:
            coin_flip = self.heads_or_tails()
            user = { 
                'user_id': user_id, 
                'created_at': datetime.datetime.now(),
                'ab_test_id': ab_test_id,
                'properties': json.dumps({
                    'ab_test_group': coin_flip
                })
            }
            cursor.execute('INSERT INTO ab_tests (user_id, created_at, ab_test_id, properties) VALUES(%(user_id)s, %(created_at)s, %(ab_test_id)s, %(properties)s)', user)
            conn.commit()
            user['properties'] = json.loads(user['properties'])
            user = list(user.values())
            print(f"User {user_id} has been assigned to group {coin_flip}.")

        cursor.close()
        conn.close()
        
        return user

    def _log_event(self, user_id, event_properties):

        conn = self._connect()

        cursor = conn.cursor()
        cursor.execute('INSERT INTO events (user_id, created_at, properties) VALUES(%(user_id)s, %(created_at)s, %(properties)s)', { 
            'user_id': user_id, 
            'created_at': datetime.datetime.now(),
            'properties': json.dumps(event_properties)
        })
        conn.commit()
        cursor.close()
        conn.close()