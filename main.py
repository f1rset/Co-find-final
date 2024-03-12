"""Main control module"""
from src import create_app

#Creates app
app = create_app()
#Start app
if __name__ == '__main__':
    app.run(debug=True)
