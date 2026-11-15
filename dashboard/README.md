# NFHS-5 | India Health Intelligence — Starter

## Run locally (Windows / VS Code)

1. Extract this ZIP.
2. Open the extracted folder in VS Code.
3. Create and activate a virtual environment (recommended):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   streamlit run app.py
   ```

## Upload these files in the sidebar

- Primary NFHS-5 district CSV (required)
- India.csv (optional)
- India_Change.csv (optional)
- Metadata dictionary CSV (optional)
- District GeoJSON (optional)

## Important

- The app does not modify source files.
- Supplementary datasets remain separate; no automatic merge is performed.
- Historical comparisons must be checked for indicator definition, unit, survey period, geography and coverage.
- State/district averages are not population-weighted unless appropriate weights are supplied.
- The map page requires manual confirmation that the selected join keys use compatible boundary definitions.
- PCA uses standardized selected predictors and complete-case observations; it does not silently impute missing values.

This is a functional starter scaffold. We will tailor the indicator descriptions, supplementary comparisons, GeoJSON join logic and dashboard findings after validating the exact source files and analysis outputs.
