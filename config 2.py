"""
Shared configuration for all VaR_CEE Quantlets.

Published in: 'Zero-Shot Foundation Models for VaR and ES Forecasting in CEE Markets'

This file defines paths, market definitions, VaR parameters, and model
lists used by every Quantlet in this collection.  Each Quantlet imports
from this file so that assumptions stay consistent across the pipeline.
"""

from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent   # <project root>
RAW_DIR = BASE_DIR / "data" / "raw"
PROC_DIR = BASE_DIR / "data" / "processed"
VAR_DIR = BASE_DIR / "data" / "var_forecasts"
BT_DIR = BASE_DIR / "data" / "backtesting"
FIG_DIR = BASE_DIR / "data" / "figures"
STATS_DIR = BASE_DIR / "data" / "stats"
OUTPUT_DIR = BASE_DIR / "output"

for d in [RAW_DIR, PROC_DIR, VAR_DIR, BT_DIR, FIG_DIR, STATS_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── CEE Markets ──────────────────────────────────────────────────────
MARKETS = {
    "Romania":  {"index": "BET",   "stooq": "^BET",   "fx": "EUR/RON", "yahoo_fx": "EURRON=X"},
    "Poland":   {"index": "WIG20", "stooq": "^WIG20", "fx": "EUR/PLN", "yahoo_fx": "EURPLN=X"},
    "Czechia":  {"index": "PX",    "stooq": "^PX",    "fx": "EUR/CZK", "yahoo_fx": "EURCZK=X"},
    "Hungary":  {"index": "BUX",   "stooq": "^BUX",   "fx": "EUR/HUF", "yahoo_fx": "EURHUF=X"},
    "Bulgaria": {"index": "SOFIX", "stooq": "^SOFIX", "fx": "USD/BGN", "yahoo_fx": "USDBGN=X"},
}

# ── Date Range ───────────────────────────────────────────────────────
START_DATE = "2007-01-01"
END_DATE = "2025-12-31"
OOS_START = "2018-01-01"          # out-of-sample evaluation starts here

# ── VaR / ES Parameters ─────────────────────────────────────────────
VAR_ALPHAS = [0.01, 0.025, 0.05]  # VaR confidence levels
ES_ALPHA = 0.025                   # ES confidence level
ROLLING_WINDOW = 250               # rolling estimation window (days)
REFIT_EVERY_LSTM = 21              # LSTM retrain frequency (days)

# ── Foundation Model Parameters ──────────────────────────────────────
FM_CONTEXT = 512                   # R1: was 250
FM_NUM_SAMPLES = 1000              # R1: was 200
FM_HORIZON = 1                     # 1-step ahead

# ── Computational ────────────────────────────────────────────────────
STRIDE = 1                         # R1: was 5 — full daily run
SEED = 42

# ── Model Lists ──────────────────────────────────────────────────────
BASELINE_MODELS = ["HS", "GJR-GARCH", "ARIMA-Conformal", "LSTM-Conformal"]
FM_MODELS = ["Chronos-2", "TimesFM-2.5", "Moirai-2.0"]
FM_CONF_MODELS = ["Chronos-2-Conf", "TimesFM-2.5-Conf", "Moirai-2.0-Conf"]
ALL_MODELS = BASELINE_MODELS + FM_MODELS + FM_CONF_MODELS

# ── Helper ───────────────────────────────────────────────────────────
def get_all_series():
    """Return list of (country, series_id, series_type) tuples."""
    series = []
    for country, info in MARKETS.items():
        series.append((country, f"{info['index']}_ret", "index"))
        fx_id = info['fx'].replace("/", "") + "_ret"
        series.append((country, fx_id, "fx"))
    return series
