import requests
import time
import csv
import os

class SQLiEngine:
    def __init__(self, target_url, session_cookie=None):
        self.target_url = target_url
        self.headers = {'Cookie': session_cookie} if session_cookie else {}
        self.results_path = "data/campaigns/latest_run.csv"

    def fire_payloads(self, payload_list):
        """Iterates through payloads and logs response metadata."""
        os.makedirs(os.path.dirname(self.results_path), exist_ok=True)

        with open(self.results_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "payload", "status_code", "response_time", "response_len"])

            for p_type, payloads in payload_list.items():
                for payload in payloads:
                    start_time = time.time()
                    try:
                        # Assuming 'id' parameter for DVWA SQLi
                        response = requests.get(f"{self.target_url}?id={payload}&Submit=Submit", headers=self.headers)
                        end_time = time.time()

                        writer.writerow([
                            time.strftime("%Y-%m-%d %H:%M:%S"),
                            payload,
                            response.status_code,
                            round(end_time - start_time, 4),
                            len(response.text)
                        ])
                    except Exception as e:
                        print(f"Error firing payload {payload}: {e}")

        return self.results_path