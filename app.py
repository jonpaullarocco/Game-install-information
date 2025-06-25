from flask import Flask, request, render_template_string
import json
import difflib

app = Flask(__name__)

with open("escape_room_data.json", "r") as f:
    data = json.load(f)

with open("template.html", "r") as f:
    HTML_TEMPLATE = f.read()

@app.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    results = []
    if query:
        query_terms = query.lower().split()
        for entry in data:
            blob = entry.get("search_blob", "").lower()
            if any(term in blob for term in query_terms) or any(
                difflib.SequenceMatcher(None, term, blob).quick_ratio() > 0.6 for term in query_terms
            ):
                results.append(entry)
    return render_template_string(HTML_TEMPLATE, query=query, results=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)