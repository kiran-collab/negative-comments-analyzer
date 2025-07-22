import os
from flask import Flask, request, render_template_string
import tweepy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Twitter API setup
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
client = tweepy.Client(bearer_token=bearer_token)

# HTML template
HTML_TEMPLATE = """
<!doctype html>
<title>Twitter Search</title>
<h2>Search Tweets</h2>
<form method="get">
  <input name="query" placeholder="Enter keyword" required>
  <input type="submit" value="Search">
</form>
{% if tweets %}
  <h3>Results for "{{ query }}":</h3>
  <ul>
    {% for tweet in tweets %}
      <li>{{ tweet }}</li>
    {% endfor %}
  </ul>
{% endif %}
"""

@app.route("/", methods=["GET"])
def search_tweets():
    query = request.args.get("query")
    tweets = []

    if query:
        response = client.search_recent_tweets(query=query, max_results=5)
        if response.data:
            tweets = [tweet.text for tweet in response.data]

    return render_template_string(HTML_TEMPLATE, tweets=tweets, query=query)

if __name__ == "__main__":
    app.run(debug=True)
