import logging
import json
import requests

# Splunk HEC configuration
SPLUNK_HEC_URL = "https://your-splunk-hec-endpoint"
SPLUNK_HEC_TOKEN = "YOUR_SPLUNK_HEC_TOKEN"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_to_splunk(event):
    """
    Sends an event to Splunk HEC.
    """
    try:
        headers = {
            "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
            "Content-Type": "application/json"
        }
        data = json.dumps(event)
        response = requests.post(SPLUNK_HEC_URL, headers=headers, data=data)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error sending log to Splunk: {e}")
