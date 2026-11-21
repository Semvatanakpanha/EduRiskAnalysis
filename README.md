# CamBud — Cambodia Budget Analytics

CamBud is a student-built Streamlit dashboard for exploring Cambodia's approved government budget allocations.

## Dataset used

The supplied CSV was translated from Khmer into professional English and saved as `budget_data.csv`.

**Original dataset:** Current and Capital Expenditure by Entity of Budget Law in Brief FY2021–FY2026  
**Publisher:** Ministry of Economy and Finance (MEF), Cambodia  
**Dataset page:** https://data.mef.gov.kh/datasets/pd_69942a5e9eaed400071a6ca9

### Translated columns

| English column | Original column | Meaning |
|---|---|---|
| Fiscal Year | `Ref_year` | Budget fiscal year |
| Government Entity | `Entity_name` | Ministry or government institution |
| Budget Category | `Budget_Group` | Current or capital expenditure |
| Approved Budget (Million KHR) | `Budget_Law` | Amount in million Cambodian riel |

### Data profile

- Rows: 446
- Fiscal years: 2021–2026
- English entity labels: 41
- Categories: Current Expenditure and Capital Expenditure
- Missing budget amounts in original file: 49

**Data-quality note:** The original file contains blank budget amounts. They are preserved as missing values in the translated CSV and excluded from totals and charts; they have not been replaced with zero or estimated values. Some entity labels that differed only by Khmer spacing were standardized to the same English entity name.

## Project structure

```text
CamBud/
├── .venv/                 # Create locally; not included in the ZIP
├── app.py
├── README.md
├── requirements.txt
├── budget_data.csv        # Translated dataset from your upload
└── style.css
```

## Run on Windows using VS Code

Open the CamBud folder in VS Code and run these commands in the terminal:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

If PowerShell prevents environment activation, run:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

## Application pages

1. **Dashboard** — KPI cards, yearly trend, expenditure composition, top entities.
2. **Budget Analysis** — Current vs capital allocations by year and category summary.
3. **Entity Analysis** — Entity ranking and comparison.
4. **Data Explorer** — Search, inspect, filter and export the dataset.

## Design

- Main interface: Navy, blue, sky blue and white.
- Charts: distinct complementary teal, amber, violet and coral accents for readability.
- Font: Times New Roman.
- Layout: sidebar navigation, filter panel, KPI cards, charts and data tables.

## Interpretation

The dataset is about approved Budget Law allocations. Do not describe the values as actual cash expenditure, actual spending, budget execution or remaining budget unless another source supports those measures.
