from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! This app is running on GKE private cluster."
s
if __name__ == '__main__':
    # Setting host to 0.0.0.0 allows access from outside the container
    app.run(host='0.0.0.0', port=8080)
