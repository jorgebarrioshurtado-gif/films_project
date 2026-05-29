# 🎬 WhatToWatch

A data analytics and machine learning project that explores film representation, genre patterns, and user taste to recommend what to watch next.

---

## 📌 Overview

**WhatToWatch** is built around three core ideas:

- **Women underrepresentation is a real concern**: the film industry has a measurable, quantifiable bias that shows up in budgets, genres, and decades
- **Genres do not give us relevant information**: "Drama" and "Action" are labels so broad they're almost meaningless for understanding what a film actually feels like
- **Everyone has a favourite film and wants to find similar ones**: the recommender uses cinematic DNA, not genre labels, to surface films you'll actually want to watch

The project combines data engineering, SQL, exploratory analysis, Tableau dashboards, and a deployed machine learning application.

---

## 🔗 Links

- [🎬 Live Streamlit App](https://whattowatch-by-jorge.streamlit.app/)
- [📊 Tableau Dashboards](https://public.tableau.com/app/profile/jorge.barrios.hurtado/viz/WhatToWatch_17798156743590/general_info?publish=yes)
- [🖥️ Google Slides](https://docs.google.com/presentation/d/1E057H2P5qvkuw8Vy8kKKSXgiDXSf_15Dzfs7-vy3kZ0/edit?usp=sharing)

---

## 📂 Dataset & Sources

| Source | Description | Size |
|--------|-------------|------|
| [MovieLens 32M](https://grouplens.org/datasets/movielens/latest/) | User ratings and genome tag scores | ~70,000 films · 32M ratings |
| [IMDb Non-Commercial Datasets](https://developer.imdb.com/non-commercial-datasets/) | Film metadata, ratings, genres | `title.basics`, `title.ratings` |
| [TMDB API](https://developer.themoviedb.org/docs/getting-started) | Budget, revenue, poster paths, overviews, taglines | Enrichment layer |
| [Bechdel Test Dataset](https://www.kaggle.com/datasets/alisonyao/movie-bechdel-test-scores?select=Bechdel_detailed.csv) | Pass/fail representation scores | ~9,000 films |

> IMDb people and episode datasets were excluded as they were not required for this project's scope.

---

## 🗂️ Project Structure

```
.
├── data
│   ├── app
│   │   ├── streamlit_data.csv
│   │   └── tmdb_details_cache.json
│   ├── external
│   │   └── bechdel_detailed.csv
│   └── visualizations
│       ├── film_genres.csv
│       ├── film_main_info.csv
│       └── user_ratings.csv
├── notebooks
│   ├── cleaning_datasets.ipynb
│   ├── creating_sql_database.ipynb
│   └── unsupervised_ml_model.ipynb
├── README.md
├── requirements.txt
├── runtime.txt
├── sql
│   ├── creating_dataset_streamlit.sql
│   ├── creating_tables_for_visualizations.sql
│   ├── recommendations.sql
│   ├── small_eda.sql
│   └── WhatToWatch_schema.mwb
├── src
│   ├── __pycache__
│   │   ├── data_collection.cpython-313.pyc
│   │   └── styles.cpython-313.pyc
│   ├── data_collection.py
│   └── styles.py
├── streamlit
│   ├── 0_Home.py
│   └── pages
│       ├── 1_🔍_WhatToWatch.py
│       ├── 2_🚫_Filter_Search.py
│       └── 3_📊_Our_Catalog.py
└── visualizations
    └── WhatToWatch.twbx
```

---

## 🔬 Methodology

### 1. Data Collection & Engineering
- Downloaded MovieLens 32M, IMDb bulk datasets, and Bechdel CSV
- Used `links.csv` from MovieLens as the anchor, it maps MovieLens IDs to IMDb IDs and TMDB IDs across all sources
- Filtered IMDb datasets to only films present in MovieLens, removing TV shows, shorts, and adult content
- Enriched the dataset via TMDB API with budget, revenue, poster paths, overviews, and taglines (with a checkpoint-based loop to handle interruptions)
- Built a lazy-loading JSON cache for poster and film details to minimise API calls in the Streamlit app

### 2. Database
- Loaded all cleaned datasets into a **MySQL** database using SQLAlchemy from Python
- Wrote SQL joins to produce analysis-ready tables for Tableau and Streamlit
- Key tables: `films`, `film_genres`, `user_ratings`, `bechdel`

### 3. Exploratory Analysis & Tableau Dashboards
Three dashboards built in Tableau Public:

**General Info**: database overview with KPI cards (film count, year range, total ratings, genre count), films per decade, genre distribution, and average rating over time

**Representation**: Bechdel pass/fail trends by decade and genre, budget gap between passing and failing films, IMDb rating distribution by Bechdel result

**Genre DNA**: scatter plots showing internal variance within genre labels, runtime distributions, and genre co-occurrence patterns. The visual argument that genre labels are too broad to be useful

### 4. Machine Learning — KMeans Clustering
- Used **MovieLens genome scores** as the feature matrix. 1,100 tag relevance scores per film, capturing cinematic DNA rather than broad genre labels
- Applied **PCA** (150 components, ~80% variance explained) to reduce dimensionality before clustering
- Used the **elbow method** to guide cluster selection
- Final model: **KMeans with 150 clusters** on the PCA-reduced genome scores
- Each cluster groups films with genuinely similar taste profiles, the recommender samples from the same cluster as the input film

---

## 🤖 Recommendation System

The app takes a film the user loves and returns similar films drawn from the same KMeans cluster.

**How it works:**
1. User selects a film from the catalog
2. The system finds its cluster
3. Random films are sampled from that cluster (excluding the input film)
4. Results are displayed with poster, year, IMDb rating, tagline, overview, and a direct IMDb link
5. Bechdel pass status is shown where available

**Cold start:** not applicable. The model clusters films, not users. Any film in the catalog can be used as a seed immediately.

**Poster caching:** film details (poster path, tagline, overview) are fetched from the TMDB API on first request and stored in a local JSON cache. Subsequent requests for the same film are served from cache without API calls.

---

## 📊 Key Findings

- Bechdel pass rate has improved over decades but remains below 60% for several major genres including Action & Adventure
- Films that pass the Bechdel test receive smaller average budgets than failing films within the same genre — a measurable industry bias
- IMDb rating distributions between Bechdel-passing and failing films are similar, countering the assumption that representation-forward films perform worse with audiences
- Genre labels explain almost nothing about what a film actually feels like — films within the same genre show enormous variance in runtime, rating, tone, and theme
- The MovieLens genome scores capture nuanced taste profiles that genre labels cannot, making them a far stronger foundation for recommendations

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Libraries:**
  - `pandas`, `numpy`: data manipulation
  - `scikit-learn`: PCA, KMeans clustering
  - `sqlalchemy`: MySQL connection from Python
  - `streamlit`: web application deployment
  - `requests`, `python-dotenv`: API calls and secrets management
  - `matplotlib`: exploratory visualisation
- **Database:** MySQL
- **BI Tool:** Tableau Public
- **Deployment:** Streamlit Cloud

---

## ▶️ How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/jorgebarrioshurtado-gif/films_project.git
   cd films_project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your TMDB API key to `.streamlit/secrets.toml`:
   ```toml
   TMDB_API_KEY = "your_key_here"
   ```

4. Run the app:
   ```bash
   streamlit run streamlit/whattowatch.py
   ```

> ⚠️ The full dataset and MySQL database are not included in this repository. The Streamlit app loads pre-processed CSV files. See `notebooks/01_data_collection.ipynb` for the full data pipeline.

---

## 👤 Author

**Jorge Barrios Hurtado**