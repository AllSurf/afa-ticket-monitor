🕵️‍♂️ AFA Ticket Monitor
- AFA Ticket Monitor is a lightweight Python bot that monitors the AFA ticket sales website and alerts you as soon as any changes are detected on the page — such as a new match, a change in status, or the release of new tickets.
- It is designed for football fans who want to secure tickets as soon as they become available, without manually refreshing the site every few minutes.

🔍 How It Works
- Loads the AFA Tickets site in a headless Chrome browser using Selenium.
- Calculates a hash of the HTML structure of the key content area (#catalog and its siblings).
- Checks the site periodically (default: every 30 seconds).
- Plays a siren when a change is detected.
- Optionally beeps quietly every few checks to confirm it's still running.
- Logs timestamps and can export HTML snapshots for debugging or auditing.

🔔 Features
  🧠 Smart change detection based on DOM structure, not just visible text.
  🎧 Loud siren (sirena-tornado.wav) on ticket changes.
  🔕 Optional short beep every few checks without change.
  📁 Saves the initial and updated HTML versions for manual comparison.
  🖥️ Headless or visible browser mode.
  ⚙️ Customizable check interval and behavior.

🚀 Setup
- Requirements
  - Python 3.8+
  - Google Chrome installed
  - pip install selenium webdriver-manager

🛠 Customization
- You can configure:
  - Check interval (CHECK_INTERVAL)
  - Headless mode (HEADLESS = True/False)
  - Alert sound file (SIRENA_FILE)
  - DOM section to monitor (get_ticket_html() logic)

