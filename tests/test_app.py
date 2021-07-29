import unittest
import socket
import requests
import logging
import json
from multiprocessing import Process
from web_app import flask_app

logging.getLogger().setLevel(logging.DEBUG)


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.host = get_ip()
        self.port = 5000
        self.process = Process(target=flask_app.run, kwargs={'host': '0.0.0.0'})
        self.process.start()

    def test_get_data(self):
        url = f'http://{self.host}:{self.port}/get_data/Temperature'
        response = requests.get(url)
        logging.debug(f'response is {response}')
        self.assertTrue(response.hasKey('data'))

    def test_get_sensors(self):
        url = f'http://{self.host}:{self.port}/get_sensors'
        response = requests.get(url)
        response_dict = json.loads(response.text)
        logging.debug(f'response is {response_dict}')
        self.assertTrue(response_dict['status'] == 200)


    def tearDown(self) -> None:
        self.process.terminate()
        self.process.join()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close
    return IP


if __name__ == '__main__':
    unittest.main()

