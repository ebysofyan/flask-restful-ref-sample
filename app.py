import os

from flask import Flask

from movie_api.context import movie_app

app: Flask = movie_app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", "5010"), debug=True)
