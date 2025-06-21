
from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

# Load data once at startup
with open("escape_room_data.json", "r") as f:
    data = json.load(f)

# Extract distinct game titles from filenames
game_titles = sorted(set(entry["file_name"].split(" ")[1] for entry in data if " " in entry["file_name"]))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Escape Room Search</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        input[type=text], select { padding: 8px; }
        input[type=text] { width: 50%; }
        button { padding: 8px 12px; }
        .result { margin-top: 1.5em; padding: 10px; border-bottom: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>Escape Room Search Tool</h1>
    <form method="get">
        <input type="text" name="q" placeholder="Search for a term..." value="{{ query }}" />
        <select name="game">
            <option value="">All Games</option>
            {% for game in games %}
                <option value="{{ game }}" {% if game == selected_game %}selected{% endif %}>{{ game }}</option>
            {% endfor %}
        </select>
        <button type="submit">Search</button>
    </form>

    {% if results %}
        <h2>Results ({{ results|length }})</h2>
        {% for res in results %}
            <div class="result">
                <strong>{{ res.file_name }}</strong><br/>
                <em>...{{ res.snippet }}...</em>
            </div>
        {% endfor %}
    {% elif query %}
        <p>No results found for '{{ query }}'{{ ' in ' + selected_game if selected_game else '' }}.</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    selected_game = request.args.get("game", "")
    results = []
    if query:
        q_lower = query.lower()
        for entry in data:
            game_name = entry["file_name"].split(" ")[1] if " " in entry["file_name"] else ""
            if (not selected_game or selected_game == game_name) and q_lower in entry["text"].lower():
                idx = entry["text"].lower().find(q_lower)
                snippet = entry["text"][max(0, idx - 100): idx + 200].replace("\n", " ").strip()
                results.append({
                    "file_name": entry["file_name"],
                    "snippet": snippet
                })
    return render_template_string(HTML_TEMPLATE, query=query, results=results, games=game_titles, selected_game=selected_game)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
