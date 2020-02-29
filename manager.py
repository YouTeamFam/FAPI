from flask_migrate import Migrate

from apiapp import create_app
from apiapp.models import db

app = create_app()
Migrate(app,db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
