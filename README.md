
# Escape Room Search App

This is a Flask-based web app for searching through escape room puzzle guides, timelines, and game flow documents.

## 🔍 Features

- Full-text and fuzzy search
- Game filter dropdown
- Dynamic puzzle metadata (game, room, puzzle name)
- Tabbed PDF viewer with zoom/fullscreen
- Persistent tab state using localStorage
- Dynamic icons for game types (🕵️, 👻, 🧪, etc.)
- Inline notes/snippet display

## 🚀 Deployment Instructions

1. **Upload to GitHub**
   - Push the contents of this repo to your GitHub account

2. **Deploy to Render**
   - Go to [https://render.com](https://render.com)
   - Click “New Web Service”
   - Connect your GitHub repo
   - Confirm `python` environment is selected
   - Leave build command blank
   - Use `python app.py` as the start command

## 📁 File Structure

```
.
├── app.py
├── template.html
├── escape_room_data.json
├── requirements.txt
├── Procfile
├── render.yaml
└── static/
    └── <PDF guides>
```

## 🧠 Tech Stack

- Python 3.x
- Flask 3.x
- HTML5, CSS3, JavaScript
- Render.com for hosting

## 🧩 Notes

- All PDFs are loaded from the `static/` folder.
- Tab states are preserved between sessions.
- All search data is extracted from PDF content parsed into `escape_room_data.json`.

## 🔐 Optional Enhancements

- Add user accounts for saved searches
- Use OpenAI embeddings for smarter search
- Admin UI to tag puzzles and manage notes

---

Made with 💡 by [Your Name]
