
from flask import Flask, request, render_template_string
import json
import difflib

app = Flask(__name__)

# Load data once at startup
with open("escape_room_data.json", "r") as f:
    data = json.load(f)

# Extract distinct game titles from filenames
game_titles = sorted(set(entry["file_name"].split(" ")[1] for entry in data if " " in entry["file_name"]))

# Load the full HTML template
with open("template.html") as f:
    HTML_TEMPLATE = f.read()

def extract_meta(text, keys):
    lines = text.split("\n")
    for line in lines:
        for key in keys:
            if key.lower() in line.lower():
                return line.strip()
    return "Unknown"

@app.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    selected_game = request.args.get("game", "")
    results = []
    if query:
        query_terms = query.lower().split()
        for entry in data:
            game_name = entry["file_name"].split(" ")[1] if " " in entry["file_name"] else ""
            if not selected_game or selected_game == game_name:
                text = entry["text"].lower()
                if all(term in text for term in query_terms) or any(
                    difflib.SequenceMatcher(None, term, text).quick_ratio() > 0.6 for term in query_terms
                ):
                    idx = min((text.find(term) for term in query_terms if term in text), default=0)
                    snippet = entry["text"][max(0, idx - 200): idx + 600].replace("\n", " ").strip()
                    results.append({
                        "file_name": entry["file_name"],
                        "snippet": snippet,
                        "game": game_name,
                        "room": extract_meta(entry["text"], ["room", "room number"]),
                        "puzzle": extract_meta(entry["text"], ["puzzle", "title", "name"])
                    })
    return render_template_string(HTML_TEMPLATE, query=query, results=results, games=game_titles, selected_game=selected_game)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
