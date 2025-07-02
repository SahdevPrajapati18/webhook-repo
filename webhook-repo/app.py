from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://sahdevprajapati27:987066@cluster0.guvgwcw.mongodb.net/webhookDB?retryWrites=true&w=majority&tlsInsecure=true")

  # Replace this with your Mongo URI
db = client.webhookDB
collection = db.events

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        event = request.headers.get('X-GitHub-Event')
        print("✅ Webhook received:", event)

        if event == "push":
            author = data['pusher']['name']
            to_branch = data['ref'].split("/")[-1]
            timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            message = f"{author} pushed to {to_branch} on {timestamp}"
            print("Inserting to DB:", message)
            collection.insert_one({"event": "push", "message": message, "timestamp": timestamp})

        elif event == "pull_request" and data['action'] == "opened":
            author = data['pull_request']['user']['login']
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            message = f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
            print("Inserting to DB:", message)
            collection.insert_one({"event": "pull_request", "message": message, "timestamp": timestamp})

        elif event == "pull_request" and data['action'] == "closed" and data['pull_request']['merged']:
            author = data['pull_request']['user']['login']
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            message = f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"
            print("Inserting to DB:", message)
            collection.insert_one({"event": "merge", "message": message, "timestamp": timestamp})

        print("✅ Done processing.")
        return jsonify({"status": "received"}), 200

    except Exception as e:
        print("❌ Webhook error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort('_id', -1).limit(10))
    return jsonify([{"message": e["message"]} for e in events])

if __name__ == '__main__':
    app.run(debug=True)
