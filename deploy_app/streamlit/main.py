import threading
import time
import sys
import os

# Make streamlit folder importable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# -------------------------------
# Start Flask backend in background
# -------------------------------
def run_flask():
    from backend.app import app
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Give Flask time to boot
time.sleep(2)

# -------------------------------
# Start Streamlit frontend
# -------------------------------
from frontend.app import main
main()
