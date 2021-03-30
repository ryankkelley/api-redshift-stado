
import argparse

import uvicorn

from api.__main__ import app

# parser = argparse.ArgumentParser(description='Redshift Rest Service')
# parser.add_argument('--port')


if __name__ == '__main__':
    #args = parser.parse_args()
    uvicorn.run(app, host='0.0.0.0', port=int(3333))