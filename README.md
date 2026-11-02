# German Day-Ahead Electricity Price Forecasting

Forecasting hourly day-ahead electricity prices for the German/Luxembourg bidding zone with statistical and machine-learning models, using real open data from [SMARD](https://www.smard.de) (Bundesnetzagentur).

> 🚧 Work in progress. See [ROADMAP.md](ROADMAP.md).

## Problem
<!-- 2–3 sentences: who needs price forecasts (traders, battery operators, industry) and what you forecast. -->

## Data
| Column | Source (SMARD filter) | Unit |
|---|---|---|
| price_eur_mwh | Day-ahead price DE-LU (4169) | €/MWh |
| load_mwh | Total grid load (410) | MWh |
| residual_load_mwh | Residual load (4359) | MWh |
| wind_onshore_mwh | Wind onshore generation (4067) | MWh |
| wind_offshore_mwh | Wind offshore generation (1225) | MWh |
| solar_mwh | Photovoltaic generation (4068) | MWh |

Period: <!-- fill in --> · Resolution: hourly · Source: Bundesnetzagentur | SMARD.de, licence CC BY 4.0

## Key findings from the data
<!-- 3–5 bullet points with numbers, from your EDA notebook -->

## Approach
<!-- Forecast setup (day D forecast on D-1), train/test split, leakage rules, models -->

## Results
| Model | MAE (€/MWh) | RMSE (€/MWh) |
|---|---|---|
| Naive (same hour yesterday) | | |
| Seasonal naive (same hour last week) | | |
| SARIMA | | |
| XGBoost | | |
| LightGBM | | |

<!-- Add a chart: actual vs forecast for one week of the test period -->

## Live demo
<!-- Streamlit link -->

## How to run
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/download_smard.py --start 2024-01-01 --end 2026-10-31
```

## Project structure
```
src/          data download and feature code
notebooks/    EDA, baselines, SARIMA, gradient boosting
app/          Streamlit app
reports/      figures for the README
data/         raw and processed data (not committed)
```
