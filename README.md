# Smart Angkor Tourist Guide — Website

A Django website version of the Smart Angkor Tourist Guide console app.
It reuses your original `graph.py`, `hash_table.py`, and `decision_tree.py`
logic (ported into `guide/algorithms/`, unchanged apart from being callable
as a library), stores temple/road data in **SQLite** via Django models, and
adds a Bootstrap 5 front end with an **interactive network map** (BFS / DFS /
Dijkstra, drawn live with vis-network) and a tour recommendation page.

## Project layout

```
angkor_site/
├── manage.py
├── requirements.txt
├── config/                  # Django project settings/urls
└── guide/                   # the app
    ├── models.py            # Temple, Road (SQLite via Django ORM)
    ├── views.py              # pages + JSON API for the map
    ├── urls.py
    ├── admin.py
    ├── algorithms/
    │   ├── graph.py          # ported Graph class (BFS/DFS/Dijkstra)
    │   ├── hash_table.py     # ported HashTable class
    │   ├── decision_tree.py  # ported recommend_tour()
    │   └── utils.py          # estimate_travel_time()
    ├── management/commands/
    │   └── load_data.py      # loads guide/data/*.csv into SQLite
    ├── data/
    │   ├── temples.csv
    │   └── roads.csv
    ├── templates/guide/       # Bootstrap templates
    └── static/guide/          # CSS
```

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations (creates db.sqlite3)
python manage.py migrate

# 4. Load temple & road data from CSV into the database
python manage.py load_data

# 5. (Optional) create an admin user
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

## Pages

- `/` — home
- `/temples/` — browse & search temples (by name / category)
- `/temples/<ID>/` — temple detail (looked up via the ported HashTable)
- `/navigation/` — interactive map: run BFS, DFS, or Dijkstra's shortest
  route between temples; results are highlighted live on the graph
- `/recommend/` — pick a time budget + interest, get a tour list (the
  ported decision tree)
- `/api/navigation/?algorithm=bfs|dfs|dijkstra&start=...&end=...` — the
  small JSON API the map page calls

## Notes on the source data

Two small fixes were made while porting the CSVs so the graph loads
cleanly:
- `temples.csv`: a missing comma on the Bayon (`T04`) row was corrupting
  that row's `VisitTime`/`Description` fields — fixed.
- `roads.csv`: `"Neak Poan"` was renamed to `"Neak Pean"` to match the
  spelling used in `temples.csv`, so that road connects properly.
- `decision_tree.py`: `"Krawan"` was normalized to `"Kravan"` to match
  `temples.csv`.

If you edit the CSVs later, just re-run `python manage.py load_data` —
it's safe to run repeatedly (it upserts by temple ID / road pair).
