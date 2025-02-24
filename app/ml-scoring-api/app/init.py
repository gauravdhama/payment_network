from flask import Flask

app = Flask(__name__)

# Import API modules
from app.api import score

# Register API blueprints
app.register_blueprint(score.bp, url_prefix='/api/ml-scoring')

#... other initialization code if needed...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)  # Run on port 5003
