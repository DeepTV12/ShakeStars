import requests
import json
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Initialize Console for Rich Formatting
console = Console()

BASE_URL = "https://shakestars.bar/shaker/api"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "referer": "https://shakestars.bar/dgame/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "priority": "u=1, i"
}
def display_logo():
    console.print(Panel.fit(
        "[bold cyan] ██████████                               ███████████ █████   █████ ████   ████████ [/]\n"
        "[bold cyan]░░███░░░░███                             ░█░░░███░░░█░░███   ░░███ ░░███  ███░░░░███[/]\n"
        "[bold cyan] ░███   ░░███  ██████   ██████  ████████ ░   ░███  ░  ░███    ░███  ░███ ░░░    ░███[/]\n"
        "[bold cyan] ░███    ░███ ███░░███ ███░░███░░███░░███    ░███     ░███    ░███  ░███    ███████[/]\n"
        "[bold cyan] ░███    ░███░███████ ░███████  ░███ ░███    ░███     ░░███   ███   ░███   ███░░░░[/]\n"
        "[bold cyan] ░███    ███ ░███░░░  ░███░░░   ░███ ░███    ░███      ░░░█████░    ░███  ███      █[/]\n"
        "[bold cyan] ██████████  ░░██████ ░░██████  ░███████     █████       ░░███      █████░██████████[/]\n"
        "[bold cyan]░░░░░░░░░░    ░░░░░░   ░░░░░░   ░███░░░     ░░░░░         ░░░      ░░░░░ ░░░░░░░░░░[/]\n"
        "\n[bold yellow]© DeepTV | Telegram: [blue]https://t.me/DeepTV12[/][/]"
    ))

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def watermark(text, status="INFO", color="white"):
    timestamp = get_time()
    return f"[{timestamp}] [{status}] [bold {color}]{text}[/] [dim]— DeepTV12[/]"



def read_query_ids(file_path="data.txt"):
    """Reads query IDs from a file and returns them as a list."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def get_user_details(query_id):
    """Fetches user details using the given query_id."""
    headers = HEADERS.copy()
    headers["x-telegram-init-data"] = query_id

    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        console.print(watermark(f"Failed to fetch user details: {response.text}","WARNING","red"))
        return None

def get_task_list(query_id):
    """Fetches the list of available tasks."""
    headers = HEADERS.copy()
    headers["x-telegram-init-data"] = query_id

    response = requests.get(f"{BASE_URL}/tasks/list", headers=headers)
    if response.status_code == 200:
        return response.json().get("tasks", [])
    else:
        console.print(watermark(f"Failed to fetch task list: {response.text}","WARNING","red"))
        return []

def shake(query_id, energy):
    """Sends a shake request using the given query_id and energy as tapsCount."""
    headers = HEADERS.copy()
    headers["x-telegram-init-data"] = query_id

    timestamp = str(int(time.time() * 1000))  # Generate current timestamp in milliseconds
    payload = {
        "tapsCount": energy,
        "shakesCount": 0,
        "hash": timestamp
    }

    response = requests.post(f"{BASE_URL}/shake/apply", headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        console.print(watermark(f"Shake successful! Used {energy} energy.","SUCCESS","yellow"))
    else:
        console.print(watermark(f"Shake failed: {response.text}","WARNING","red"))

def claim_task(query_id, task_id, task_type):
    """Claims a task with the given ID and type."""
    headers = HEADERS.copy()
    headers.update({
        "x-telegram-init-data": query_id,
        "content-type": "application/json",
        "origin": "https://shakestars.bar"
    })

    payload = json.dumps({"id": task_id, "type": task_type})
    response = requests.post(f"{BASE_URL}/tasks/claim", headers=headers, data=payload)

    if response.status_code == 200:
        console.print(watermark(f"Task {task_id} claimed successfully.","SUCCESS","yellow"))
    else:
        console.print(watermark(f"Failed to claim task {task_id}: {response.text}","WARNING","red"))

def claim_cocktail(query_id):
    """Sends a request to claim the cocktail after shaking."""
    headers = HEADERS.copy()
    headers["x-telegram-init-data"] = query_id

    response = requests.post(f"{BASE_URL}/shake/claim", headers=headers)

    if response.status_code == 200:
        console.print(watermark("Cocktail claimed successfully! 🍹","SUCCESS","yellow"))
    else:
        console.print(watermark(f"Failed to claim cocktail: {response.text}","WARNING","red"))

def get_cocktails(query_id):
    """Fetches the user's available cocktails."""
    headers = HEADERS.copy()
    headers["x-telegram-init-data"] = query_id

    response = requests.get(f"{BASE_URL}/users/cocktails?offset=0&limit=50", headers=headers)

    if response.status_code == 200:
        data = response.json()
        console.print(watermark("User cocktails:", json.dumps(data, indent=4)))
        return data["cocktails"] if "cocktails" in data else []
    else:
        console.print(watermark(f"Failed to fetch cocktails: {response.text}","WARNING","red"))
        return []

def sell_cocktail(query_id, cocktail_id):
    """Sells a cocktail by its ID."""
    headers = HEADERS.copy()
    headers["x-telegram-init-data"] = query_id

    payload = {"cocktailId": cocktail_id}
    response = requests.post(f"{BASE_URL}/users/sellCocktail", headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        console.print(watermark(f"Cocktail {cocktail_id} sold successfully! 💰","SUCCESS","yellow"))
    else:
        console.print(watermark(f"Failed to sell cocktail {cocktail_id}: {response.text}","WARNING","red"))


def main():
    display_logo()
    query_ids = read_query_ids()
    
    for query_id in query_ids:
        console.print(watermark(f"\nProcessing account with query_id: {query_id}","INFO","yellow"))

        # Get user details
        user_details = get_user_details(query_id)
        if user_details:
            console.print(watermark(f"User: {user_details['username']}, Level: {user_details['level']}, TON: {user_details['tonAmount']}"))
            
            energy = user_details.get('energy')  # Safely get energy, returns None if key doesn't exist
            if energy is not None :
                console.print(watermark(f"Energy: {energy}","INFO","yellow"))
                shake(query_id,energy)
                time.sleep(2)
                claim_cocktail(query_id)
                time.sleep(1)
            else:
                console.print(watermark(f"No Energy","WARNING","red"))
        user_cocktail= get_cocktails(query_id)
        if user_cocktail:
            for cocktails in user_cocktail:
                sell_cocktail(query_id, cocktails["coctailId"])
                time.sleep(2)

        # Get tasks
        tasks = get_task_list(query_id)
        if tasks:
            console.print(watermark(f"Found {len(tasks)} tasks for user."))
            for task in tasks:
                claim_task(query_id, task["id"], task["type"])
                time.sleep(1)
        else:
            console.print(watermark("No tasks available.","WARNING","red"))

if __name__ == "__main__":
    while True:
        main()
        console.print(watermark("Accounts Finished","SUCCESS","yellow"))
        console.print(watermark("Sleeping for 1 hours before retrying"))
        time.sleep(1 * 60 * 60)
