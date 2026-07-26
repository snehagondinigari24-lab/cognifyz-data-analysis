# Cognifyz Data Analysis Internship

## Aim
To analyze a restaurant dataset and extract meaningful business insights — covering cuisine trends, city-wise restaurant distribution, pricing patterns, service offerings (online delivery/table booking), rating behavior, restaurant chains, and geographic spread — using Python and interactive Streamlit dashboards, as part of the Cognifyz Data Analysis internship program.

## Why This Structure
The internship requires submitting each level (Level 1, 2, 3) as a **separate file/task**, per the program guidelines. Keeping each level in its own folder with its own script and dataset copy:
- Lets each level run independently without conflicts
- Makes it easy for reviewers to open and test one level at a time
- Matches the "separate file per level" submission requirement
- Keeps the project organized and easy to navigate on GitHub

## Folder Structure
```
Cognifyz-DataAnalysis/
├── Level1/
│   ├── level1_app.py
│   └── Dataset .csv
├── Level2/
│   ├── level2_app.py
│   └── Dataset .csv
├── Level3/
│   ├── level3_app.py
│   └── Dataset .csv
└── README.md
```

## Setup (one-time)
```
pip install streamlit pandas matplotlib
```

## How to Run

**Level 1** — Top Cuisines, City Analysis, Price Range Distribution, Online Delivery
```
cd Level1
streamlit run level1_app.py
```

**Level 2** — Restaurant Ratings, Cuisine Combinations, Geographic Map, Restaurant Chains
```
cd Level2
streamlit run level2_app.py
```

**Level 3** — Restaurant Reviews, Votes Analysis, Price Range vs Delivery/Booking
```
cd Level3
streamlit run level3_app.py
```

Each command opens the app automatically in your browser at `http://localhost:8501`.

## Notes
- Ensure `Dataset .csv` is present in the same folder as the script you're running.
- Level 3 Task 1 (Restaurant Reviews) requires a review-text column not present in this dataset; the app displays a note explaining this limitation.

## Tech Stack
- Python
- pandas (data analysis)
- matplotlib (charts)
- Streamlit (interactive dashboard)

## Author
Submitted as part of the Cognifyz Technologies Data Analysis Internship.
