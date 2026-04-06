# 🏎️ Daily Sports Updates Agent

An intelligent Python agent built with the **Google ADK** (Gemini) and **Pushover API** to deliver automated, real-time sports standings directly to your mobile device.

### 🚀 Features
*   **Agentic Search:** Uses the `google_search` tool to dynamically fetch the latest F1 Driver, Constructor, and IPL standings.
*   **Smart Summarization:** Powered by **Gemini 2.5 Flash** to clean up raw search data into brief, notification-friendly summaries with emojis.
*   **Push Notifications:** Instant delivery via **Pushover** to individual devices or delivery groups.
*   **Secure Config:** Full support for `.env` files to keep API keys and Pushover tokens private.
*   **Cron-Ready:** Designed to run as a lightweight daily automation script.

### 🛠️ Tech Stack
*   **Language:** Python 3.14+
*   **Core:** Google Agent Development Kit (ADK)
*   **LLM:** Gemini 2.5 Flash
*   **API:** Pushover (for notifications)
*   **Tools:** Google Search tool

### 📦 Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rajajo/sports_agent.git
    cd sports_agent
    ```
2.  **Environment Variables:**
    Create a `.env` file in the root directory and add your keys (see `.env.example`):
    ```env
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
    PUSHOVER_APP_TOKEN=YOUR_PUSHOVER_APP_TOKEN
    PUSHOVER_USER_KEY=YOUR_PUSHOVER_USER_KEY
    ```
3.  **Run the agent:**
    ```bash
    python3 agent.py
    ```

### 📅 Automatic Scheduling
To run the agent daily, add a cron job:
```bash
0 8 * * * /usr/bin/python3 /path/to/sports_agent/agent.py
```
