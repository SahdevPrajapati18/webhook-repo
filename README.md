# 🌐 webhook-repo

This is the Flask application that:

1. Receives GitHub webhook events from `action-repo`
2. Stores event data in **MongoDB**
3. Exposes a simple **UI** that updates every 15 seconds to show the latest events

## 🧠 Features

- 📬 GitHub Webhook Receiver (`/webhook`)
- 🗃️ MongoDB Integration
- 🖥️ Live UI that polls every 15 seconds
- ✅ Supports Push, Pull Request, and Merge events

## 🛠️ Tech Stack

- Python (Flask)
- MongoDB (via PyMongo)
- HTML/CSS for minimal frontend
- JavaScript (polling UI)

## 🔧 Setup Instructions

### 🔁 1. Clone the Repo
```bash
git clone https://github.com/SahdevPrajapati18/webhook-repo
cd webhook-repo
