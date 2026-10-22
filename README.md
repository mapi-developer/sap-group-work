Questions to analyse:
- Which top 10 suppliers account for the largest share of total Net PO Value across US purchasing organizations over the reporting period, and what proportion of total spend is concentrated in the top 20% of suppliers?
- How is the US net procurement value and PO item volume distributed across supplier countries and domestic regions (states), and what proportion of spend relies on overseas vs. domestic vendors?
- How has monthly total Net PO Value and Purchase Order volume (PO Count) evolved across the last 12 complete months, and are there noticeable seasonal purchasing spikes?
- What is the breakdown of Net PO Value by Material Group (e.g., Frames/Wheels, Off-road Components, Accessories), and which suppliers dominate the spend in critical, high-performance categories?
- Supplier (order pattern): How do US suppliers differ in ordering frequency (PO count) and average net value per PO, and which suppliers receive many small orders that could be consolidated into long-term contracts?
- Geography (plant-supplier link): For each US receiving plant, what share of its net PO value comes from suppliers in each country/region, and does any plant depend on a single supplier region?
- Time (price development): How has the average unit price of the five highest-value materials changed month by month over the reporting period (fixed-base and chain indices)?
- Additional variable - material (sourcing risk): What proportion of net PO value is spent on single-sourced materials (only one supplier) versus multi-sourced materials?

## Project structure

```
resources/              raw SE16N exports (never edit)
data/processed/         parquet cache + po_scope.parquet (gitignored, rebuilt by the notebooks)
reports/figures/        PNG charts saved by the analysis notebooks, for the Word report
src/
  sap_data.py           paths, scope constants, cached table loaders, product-family mapping
  charts.py             shared matplotlib style + save()
  eda/                  1. exploratory data analysis, run first
    ekko_eda.ipynb      PO headers
    ekpo_eda.ipynb      PO items
    lfa1_eda.ipynb      supplier master
    ekbe_eda.ipynb      PO history (not used for the questions)
    scope_eda.ipynb     join + US scope -> data/processed/po_scope.parquet
  analysis/             2. one notebook per question above
    q1_supplier_concentration.ipynb
    q2_geography.ipynb
    q3_monthly_trend.ipynb
    q4_material_group.ipynb
    q5_order_pattern.ipynb
    q6_plant_supplier_region.ipynb
    q7_price_development.ipynb
    q8_single_sourcing.ipynb
```

Run `src/eda/scope_eda.ipynb` once before the analysis notebooks (it creates `po_scope.parquet`).
