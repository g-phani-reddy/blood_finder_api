import os
from flask import Flask # Import db from extensions
from src import create_app  # Import the function to create the app

app = create_app()  # Create the Flask app instance

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('PORT', 5000), debug=os.getenv('DEBUG', 'True') == 'True')
