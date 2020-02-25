import unittest
from cast.application.test import run
from cast.application import create_postgres_engine
import logging

logging.root.setLevel(logging.DEBUG)

class TestIntegration(unittest.TestCase):

    def test2(self):
        
        #run(kb_name='sjms_local', application_name='jmsatt', engine=create_postgres_engine())
        run(kb_name='jslink_local', application_name='perlsh', engine=create_postgres_engine())



if __name__ == "__main__":
    unittest.main()
