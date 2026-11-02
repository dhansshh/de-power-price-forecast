# Roadmap: German Day-Ahead Electricity Price Forecasting

Work through the steps in order. Each step ends with a **checkpoint**: something you can show or explain.
Tick the boxes as you go, and commit to GitHub after every step.

---

## Step 1 · Set up and get the data
- [ ] Create a virtual environment and install `requirements.txt`
- [ ] Run `python src/download_smard.py --start 2024-01-01 --end 2026-10-31`
- [ ] Open `data/raw/smard_hourly.csv` and check: number of rows, period, missing values

**Checkpoint:** you can say what each column means and in which unit it is measured.

## Step 2 · Explore the data (`notebooks/01_eda.ipynb`)
Answer these questions with one chart each:
- [ ] What does a typical day look like? (average price by hour of day)
- [ ] How do weekdays differ from weekends?
- [ ] How often are prices negative, and at what times of day?
- [ ] How strongly is price related to residual load? (scatter plot + correlation)
- [ ] Are there gaps, duplicates or daylight-saving issues in the timestamps?

**Checkpoint:** 3–5 written findings at the end of the notebook, each one sentence with a number.

## Step 3 · Define the problem properly
- [ ] Forecast target: the 24 hourly prices of **day D**, made on **day D−1 before the noon auction**
- [ ] Decide which information is really available at that moment (see "Leakage" below)
- [ ] Time-based split: train up to 2026-06-30, test 2026-07-01 → 2026-10-31. **Never a random split.**
- [ ] Metrics: MAE and RMSE in €/MWh

**Leakage.** On D−1 morning you already know all prices up to day D−1 (published on D−2),
so price lags of 24 h, 48 h and 168 h are allowed. You do **not** know the actual wind, solar
or load of day D. Using them gives a "perfect foresight" model. That is fine as an upper bound,
but label it clearly.

**Checkpoint:** you can explain in two sentences why a random train/test split would be wrong here.

## Step 4 · Baselines (`notebooks/02_baselines.ipynb`)
- [ ] Naive: price of the same hour yesterday
- [ ] Seasonal naive: price of the same hour last week
- [ ] Record MAE/RMSE on the test period

**Checkpoint:** a small table of baseline scores. Every model after this must beat them.

## Step 5 · SARIMA (`notebooks/03_sarima.ipynb`)
- [ ] Fit SARIMA with daily seasonality (m = 24) on a recent window (e.g. last 8–12 weeks)
- [ ] Forecast the test period day by day (rolling, refit or update each day)
- [ ] Compare with the baselines

**Checkpoint:** you can explain each SARIMA parameter you chose and why.

## Step 6 · Gradient boosting (`notebooks/04_xgboost_lightgbm.ipynb`)
- [ ] Build features in `src/features.py`: hour, weekday, month, public holiday, price lags (24/48/168 h), rolling means
- [ ] Train XGBoost and LightGBM on the same split
- [ ] Version A: only information available at forecast time
- [ ] Version B: add actual wind/solar/load ("perfect foresight" upper bound)
- [ ] Feature importance or SHAP plot

**Checkpoint:** a results table with all models, and one sentence on what the gap between version A and B tells you.

## Step 7 · Experiment tracking
- [ ] Log every model run with MLflow (parameters, MAE, RMSE, plot)

**Checkpoint:** a screenshot of the MLflow comparison view in `reports/figures/`.

## Step 8 · Streamlit app (`app/streamlit_app.py`)
- [ ] Pick a date in the test period → show actual vs forecast prices for each model
- [ ] Deploy for free on Streamlit Community Cloud

## Step 9 · Finish and publish
- [ ] Fill in every section of `README.md` with your real results
- [ ] Add 2–3 figures to the README
- [ ] Add the project to your CV with the live app link

---

### What interviewers will ask
- Why is a random split wrong for time series?
- What is data leakage, and where could it happen in your project?
- Why did gradient boosting beat (or not beat) SARIMA?
- Why are German prices sometimes negative?
- What would you change to use this in production?
