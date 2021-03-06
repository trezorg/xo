import os

from app.app import create_app
from app.constant import APP_PORT

app = create_app()

if __name__ == '__main__':
    port = os.getenv('APP_PORT', APP_PORT)
    app.run(debug=True, port=port)
