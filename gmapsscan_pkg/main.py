import requests
import json
import os
import webbrowser
import concurrent.futures

class UltimateGMapScanner:
    def __init__(self, api_key):
        self.api_key = api_key
        self.vulnerable_apis = []
        self.project_id = "Hidden/Restricted"
        self.project_name = "Unknown"
        self.headers = {"User-Agent": "Mozilla/5.0 (Pentest-Scanner/2.0)"}
        self.author = "Parag"
        self.author_url = "https://github.com/parag25mcf10022"
        self.tool_name = "gmapsscan"
        self.tool_url = "https://github.com/parag25mcf10022/gmapsscan"

        # 2026 Pricing Table (Cost per 1,000 requests)
        self.pricing = {
            "Static Maps": "$2.00",
            "Street View": "$7.00",
            "Directions": "$5.00 - $15.00",
            "Distance Matrix": "$5.00",
            "Geocoding": "$5.00",
            "Places - Text Search": "$32.00 (Pro)",
            "Places - Nearby": "$32.00 (Pro)",
            "Places - Details": "$17.00",
            "Places - Autocomplete": "$2.83",
            "Air Quality": "$5.00",
            "Address Validation": "$17.00",
            "Elevation": "$5.00",
            "Timezone": "$5.00",
            "Roads - Snap": "$10.00",
            "Solar": "$10.00"
        }

    def get_detailed_metadata(self):
        """Advanced OSINT: Extracts Project ID and Name."""
        url_err = f"https://language.googleapis.com/v1/documents:analyzeEntities?key={self.api_key}"
        try:
            res = requests.post(url_err, json={}, timeout=5)
            if "project=" in res.text:
                self.project_id = res.text.split("project=")[1].split(" ")[0].replace('"', '').strip()
        except: pass

        if self.project_id != "Hidden/Restricted":
            url_meta = f"https://cloudresourcemanager.googleapis.com/v1/projects/{self.project_id}?key={self.api_key}"
            try:
                res_meta = requests.get(url_meta, timeout=5)
                if res_meta.status_code == 200:
                    self.project_name = res_meta.json().get("name", "Unknown")
            except: pass

    def check_endpoint(self, name, url):
        formatted_url = url.format(key=self.api_key)
        try:
            response = requests.get(formatted_url, headers=self.headers, timeout=10)
            res_data = response.json() if "json" in response.headers.get("Content-Type", "") else {}
            internal_status = res_data.get("status", "OK")
            error_msg = res_data.get("error_message", "")
            
            status, severity, billing = "SECURE", "None", "N/A"

            if response.status_code == 200 and not error_msg and internal_status == "OK":
                status, severity, billing = "VULNERABLE", "High", "✅ ACTIVE / BILLED"
            elif "BillingNotEnabled" in error_msg:
                status, severity, billing = "VULNERABLE", "Medium", "❌ UNBILLED"
            
            if status == "VULNERABLE":
                self.vulnerable_apis.append({
                    "name": name, 
                    "url": formatted_url, 
                    "billing": billing, 
                    "severity": severity,
                    "price": self.pricing.get(name, "Variable")
                })
                print(f"[!] {name}: {billing} (Est. Cost: {self.pricing.get(name, 'N/A')}/1k)")
            else:
                print(f"[-] {name}: SECURE")
        except: pass

    def run_scan(self):
        print(f"\n{'='*60}\n{self.tool_name.upper()} - RESEARCHER: {self.author.upper()}\n{'='*60}")
        self.get_detailed_metadata()
        print(f"[*] Project: {self.project_name} ({self.project_id})")
        print(f"[*] Starting Multi-Threaded Audit...\n")

        endpoints = {
            "Static Maps": "https://maps.googleapis.com/maps/api/staticmap?center=45,45&zoom=7&size=400x400&key={key}",
            "Street View": "https://maps.googleapis.com/maps/api/streetview?size=400x400&location=40.72,-74&key={key}",
            "Directions": "https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios&key={key}",
            "Distance Matrix": "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver&destinations=Seattle&key={key}",
            "Geocoding": "https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway&key={key}",
            "Places - Text Search": "https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants&key={key}",
            "Places - Nearby": "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33,151&radius=1500&key={key}",
            "Places - Autocomplete": "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Bing&key={key}",
            "Air Quality": "https://airquality.googleapis.com/v1/currentConditions:lookup?key={key}",
            "Address Validation": "https://addressvalidation.googleapis.com/v1:validateAddress?key={key}",
            "Elevation": "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7,-104.9&key={key}",
            "Timezone": "https://maps.googleapis.com/maps/api/timezone/json?location=39.6,-105.2&timestamp=1331161200&key={key}",
            "Roads - Snap": "https://roads.googleapis.com/v1/snapToRoads?path=-35,149|-35,148&key={key}"
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda item: self.check_endpoint(item[0], item[1]), endpoints.items())

    def generate_html_report(self):
        file_name = "gmap_report.html"
        abs_path = os.path.abspath(file_name)
        
        html_content = f"""
        <html>
        <head><title>Scan Report - {self.tool_name}</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; padding: 40px; background: #f4f7f9; color: #333; }}
            .card {{ background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); max-width: 1000px; margin: auto; }}
            h1 {{ color: #1a73e8; border-bottom: 2px solid #e8eaed; padding-bottom: 10px; margin-top: 0; }}
            .meta-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; background: #f8f9fa; padding: 20px; border-radius: 8px; }}
            table {{ width:100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #f8f9fa; padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6; color: #5f6368; }}
            td {{ padding: 12px; border-bottom: 1px solid #eee; }}
            .High {{ color: #d93025; font-weight: bold; background: #fce8e6; padding: 4px 8px; border-radius: 4px; }}
            .price-tag {{ color: #1a73e8; font-family: monospace; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 30px; font-size: 13px; color: #70757a; }}
            a {{ color: #1a73e8; text-decoration: none; }}
        </style>
        </head>
        <body>
            <div class="card">
                <h1>Google Maps Security Audit</h1>
                <p>Generated by: <a href="{self.tool_url}" target="_blank"><strong>{self.tool_name}</strong></a></p>
                <div class="meta-grid">
                    <div><strong>Researcher:</strong> <a href="{self.author_url}" target="_blank">{self.author}</a></div>
                    <div><strong>Project:</strong> {self.project_name}</div>
                    <div><strong>Project ID:</strong> {self.project_id}</div>
                    <div><strong>Key Fragment:</strong> <code>{self.api_key[:12]}***</code></div>
                </div>
                <table>
                    <tr><th>API Endpoint</th><th>Billing Status</th><th>Severity</th><th>Cost / 1k Requests</th><th>PoC</th></tr>
        """
        for item in self.vulnerable_apis:
            html_content += f"""
                <tr>
                    <td>{item['name']}</td>
                    <td>{item['billing']}</td>
                    <td><span class="{item['severity']}">{item['severity']}</span></td>
                    <td class="price-tag">{item['price']}</td>
                    <td><a href="{item['url']}" target="_blank">Execute Proof</a></td>
                </tr>"""
        
        html_content += f"""
                </table>
                <div class="footer">
                    <a href="{self.author_url}">Developed by {self.author}</a> | <a href="{self.tool_url}">Source Code</a>
                </div>
            </div>
        </body>
        </html>
        """
        with open(file_name, "w") as f: f.write(html_content)
        print(f"\n{'='*60}\nAUDIT COMPLETE\nREPORT SAVED: {abs_path}\n{'='*60}")
        webbrowser.open('file://' + abs_path)

# --- THE WRAPPER FUNCTION (CRITICAL FOR PIPX) ---
def run_cli():
    """This is the function that setup.py points to."""
    key = input("Enter Google Maps API Key: ").strip()
    if key:
        scanner = UltimateGMapScanner(key)
        scanner.run_scan()
        scanner.generate_html_report()
    else:
        print("[!] Error: No API key provided.")

# Still allow manual execution (python main.py)
if __name__ == "__main__":
    run_cli()
