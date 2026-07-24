# 100 Interview Questions & Answers — Real Estate Intelligence Platform

Use this for TCS and other ML/data interviews. Answers are tied to **your capstone** (Gurgaon, 99acres, Streamlit, Random Forest, hybrid recommender).

---

## Section A: Project Overview & Business (Q1–Q10)

### Q1. What is your project in one sentence?
**Answer:** It is an end-to-end **Real Estate Intelligence Platform** for Gurgaon that predicts property prices, visualizes sector-level market analytics, and recommends similar apartment projects using machine learning and data analytics on 99acres listing data.

### Q2. What problem does it solve?
**Answer:** Buyers and investors often lack **fair price estimates**, **locality comparisons**, and **similar-property discovery**. The platform turns historical listings into **price prediction**, **interactive market dashboards**, and **content-based recommendations** so decisions are data-driven instead of guesswork.

### Q3. Who are the target users?
**Answer:** **Home buyers**, **investors**, and **market analysts** interested in Gurgaon real estate—anyone who needs valuation, sector trends, or comparable projects before visiting brokers or sites.

### Q4. What are the three main modules?
**Answer:** (1) **Property Price Prediction** — Random Forest on 12 features; (2) **Analytics Dashboard** — maps, BHK/price charts, word clouds; (3) **Smart Recommendation** — hybrid similarity (text + structured + geo) and radius search around landmarks.

### Q5. Why did you choose Gurgaon specifically?
**Answer:** The scraped dataset is **Gurgaon-centric** (sectors, 99acres listings). Sector-based planning and high property diversity (flats vs houses, luxury tiers) make it a strong case for **location-specific ML** rather than one city-wide average price.

### Q6. Is this a production enterprise system or a capstone?
**Answer:** It is a **capstone / portfolio project** with a **full ML lifecycle** and **deployed Streamlit app**, but not a production microservices stack—no separate API, database, auth, or cloud CI/CD. I can explain how I would harden it for enterprise.

### Q7. What makes your project different from a simple price calculator?
**Answer:** Besides prediction, it adds **sector geo-analytics**, **luxury and furnishing features engineered from amenities**, **rigorous model comparison (11 algorithms)**, and a **hybrid recommender** on apartment projects—not just a single regression demo.

### Q8. What data sources did you use?
**Answer:** Primary source is **99acres.com** scraped data: `flats.csv`, `houses.csv`, and `appartments.csv` (project-level). **Sector coordinates** come from `latlong.csv` / `latlong_scraper.py` for map visualizations.

### Q9. What is the scale of your dataset?
**Answer:** Roughly **~3,017 flats** and **~1,044 houses** merged to **~3,961** rows, reduced to **~3,554** after cleaning/outliers for modeling; **~247 apartment projects** for the recommender; analytics viz uses **~3,329** rows with lat/long.

### Q10. What was your role in the project?
**Answer:** **End-to-end ownership**: data cleaning and merging in notebooks, feature engineering, model selection, building recommender artifacts, Streamlit multi-page app, and deployment pattern (pickle artifacts + optional Google Drive model download).

---

## Section B: Architecture & System Design (Q11–Q20)

### Q11. Describe the high-level architecture.
**Answer:** **Offline pipeline** (Jupyter): raw CSV → clean → engineer → train → export pickles/CSVs. **Online layer** (Streamlit): `home.py` landing + three pages load artifacts and run inference/visualization **in the same Python process**—no separate backend server.

### Q12. Why Streamlit instead of Flask/Django + React?
**Answer:** For a capstone, Streamlit gives **fast multi-page UI** and direct integration with pandas/sklearn with minimal boilerplate. Trade-off: less customization and scaling than a decoupled API + SPA; for production I would add **FastAPI** and a proper frontend.

### Q13. Do you have a database? Why or why not?
**Answer:** **No.** Data lives in **CSV files** and **pickle artifacts** for simplicity and portability. For production I would use **PostgreSQL** or a warehouse for listings, versioning, and concurrent updates.

### Q14. What artifacts does the app load at runtime?
**Answer:** **Price module:** `pipeline.pkl`, `df.pkl`. **Analytics:** `datasets/data_viz1.csv`, `datasets/sector_features.pkl`. **Recommender:** `datasets/location_distance.pkl`, `cosine_sim1/2/3.pkl`.

### Q15. How is the model distributed if it is not in Git?
**Answer:** `pipeline.pkl` is **gitignored** (size). On first run, **`gdown`** downloads from a **Google Drive** file ID if the file is missing locally—so demos work after `git clone` + `pip install`.

### Q16. What is the entry point to run the application?
**Answer:** `streamlit run home.py` from the project root, with dependencies from `requirements.txt`.

### Q17. Is there any API layer?
**Answer:** **No REST API.** Streamlit callbacks invoke Python functions directly. A production extension would expose `/predict` and `/recommend` via FastAPI with the same sklearn pipeline.

### Q18. How do notebooks relate to the app?
**Answer:** Notebooks are the **source of truth** for EDA, transforms, and training; they **write** cleaned CSVs and pickles the app **reads**. The app does not retrain on user clicks.

### Q19. What are the main folders/files an interviewer should know?
**Answer:** `home.py`, `pages/` (three modules), `datasets/` (app artifacts), many `.ipynb` pipeline notebooks, `requirements.txt`, processed CSVs like `gurgaon_properties_post_feature_selection_v2.csv`, and `latlong_scraper.py`.

### Q20. Single biggest architectural limitation?
**Answer:** **Monolithic Streamlit + static files**—no real-time data refresh, no multi-user model serving layer, and training-serving coupling only broken by exporting pickles manually.

---

## Section C: Data Collection & Preprocessing (Q21–Q30)

### Q21. What columns did you drop in early cleaning?
**Answer:** Examples include **link**, **property_id** in flat/house preprocess; level-2 drops **property_name**, **address**, **description**, **rating** to reduce noise and leakage from free text not used in the final model.

### Q22. How did you normalize price?
**Answer:** Prices were converted to a **consistent unit (Crores)** from mixed Lac/Crore strings and cleaned numeric fields so the target is comparable across listings.

### Q23. How did you merge flats and houses?
**Answer:** After separate cleaning notebooks, datasets were **concatenated** with aligned columns and a **`property_type`** flag (`flat` vs `house`) in `merge-flats-and-house.ipynb`.

### Q24. What is `property_type` used for?
**Answer:** It captures **structural market differences** between flats and houses (pricing, area patterns) and powers **analytics splits** (separate scatter/histograms).

### Q25. How did you handle “Price on Request” or bad price strings?
**Answer:** Through **parsing rules and cleaning** in preprocessing notebooks—invalid or non-numeric prices are dropped or corrected so they do not corrupt the regression target.

### Q26. What preprocessing happens inside the sklearn Pipeline vs notebooks?
**Answer:** **Notebooks:** business logic—luxury score, categories, imputation, outlier removal, column selection. **Pipeline:** **StandardScaler**, **OrdinalEncoder**, **OneHotEncoder** on the final 12 features at train and predict time.

### Q27. Why separate preprocessing for flats and houses first?
**Answer:** Raw schemas differ slightly (e.g. floor field naming); cleaning **per type** then **standardizing schema** avoids errors and preserves type-specific logic before merge.

### Q28. What is `appartments.csv` used for?
**Answer:** **Project-level** data: enriching amenity information, **recommender** (247 projects), and supporting imputation where individual listing amenity text was sparse.

### Q29. What does `latlong_scraper.py` do?
**Answer:** Scrapes **sector latitude/longitude** (via web search parsing) to enable **geomaps** in analytics; coordinates merge into `data_viz1.csv`.

### Q30. How would you automate data ingestion in production?
**Answer:** Scheduled **ETL jobs** (Airflow/cron), schema validation, deduplication by property ID, store in DB, trigger **retraining pipeline** when data drift exceeds thresholds.

---

## Section D: EDA & Data Quality (Q31–Q40)

### Q31. What EDA did you perform?
**Answer:** **Univariate** and **multivariate** analysis notebooks, distributions of price/BHK/sector, relationships between area and price; optional **pandas profiling** report (`output_report.html`).

### Q32. Why is price distribution important for modeling?
**Answer:** Price is **right-skewed**; linear models on raw price behave poorly. EDA motivated **log1p transform** on the target for training and **expm1** at inference.

### Q33. What outlier method did you use?
**Answer:** **IQR-based** detection on **price** and **price per sqft**, plus **manual review** of extreme rows (~9 removed) in `outlier-treatment.ipynb`.

### Q34. Why not remove all outliers automatically?
**Answer:** Some high-price listings are **legitimate luxury** properties; blind removal would bias the model. Manual review balances **noise removal** vs **signal loss**.

### Q35. How did you handle missing built-up area?
**Answer:** **Ratio-based imputation** using relationships between super-built-up, carpet, and built-up (e.g. factors like **1.105** and **0.9** from domain ratios in `missing-value-imputation.ipynb`).

### Q36. How was `floorNum` imputed?
**Answer:** **Median imputation** where floor number was missing after cleaning.

### Q37. Why did you drop `facing`?
**Answer:** Likely **too sparse or low predictive value** after quality checks during imputation/feature selection—documented in the missing-value/feature pipeline notebooks.

### Q38. What data quality issues were unique to real estate?
**Answer:** Inconsistent **units**, **missing areas**, **duplicate listings**, rich but messy **amenity text**, and **sector naming** inconsistencies—requiring heavy cleaning before ML.

### Q39. How do you detect data drift after deployment?
**Answer:** Not implemented in capstone; in production I would monitor **input feature distributions**, **prediction distribution**, and **MAE on labeled new sales** monthly.

### Q40. Train-test split strategy?
**Answer:** Used in model-selection notebooks with **cross-validation (e.g. 10-fold)** and holdout evaluation for MAE/R²; exact split ratio should match what you used in `model-selection.ipynb` (typically 80/20 or CV-only for comparison tables).

---

## Section E: Feature Engineering (Q41–Q50)

### Q41. List the 12 final model features.
**Answer:** `property_type`, `sector`, `bedRoom`, `bathroom`, `balcony`, `agePossession`, `built_up_area`, `servant room`, `store room`, `furnishing_type`, `luxury_category`, `floor_category`.

### Q42. What is luxury score and how was it built?
**Answer:** **Weighted sum** of 50+ binary amenity features (e.g. club house, pool, park with hand-tuned weights reflecting perceived luxury), then binned into **Low / Medium / High** `luxury_category`.

### Q43. Why weight amenities instead of using raw counts?
**Answer:** Not all amenities affect price equally; weights encode **domain knowledge** and improve interpretability vs a raw count of features.

### Q44. How was furnishing_type created?
**Answer:** **KMeans clustering** (k=3) on standardized counts of furnishing-related items → clusters interpreted as **unfurnished / semi-furnished / furnished**.

### Q45. Why KMeans for furnishing?
**Answer:** Listing text/counts form **continuous patterns**; clustering discovers **natural tiers** without arbitrary thresholds.

### Q46. What is floor_category?
**Answer:** A **binned category** (e.g. Low / Mid / High Floor) derived from floor number to capture non-linear price effects of floor level.

### Q47. What encodings are applied in the Pipeline?
**Answer:** **StandardScaler** on numeric columns; **OrdinalEncoder** on ordered/low-cardinality categoricals; **OneHotEncoder** on high-cardinality **`sector`** and **`agePossession`**.

### Q48. Why OneHot for sector?
**Answer:** Sectors are **nominal** with many levels; one-hot (with Pipeline) lets tree models split on sector-specific price behavior without false ordinality.

### Q49. Did you use PCA or target encoding in experiments?
**Answer:** **Yes in model-selection notebooks**—compared ordinal, one-hot, PCA, and **target encoding** (category_encoders) across algorithms; final deployed pipeline uses the **ColumnTransformer** configuration chosen after those experiments.

### Q50. How did feature selection methods compare?
**Answer:** Used **Random Forest importance**, **gradient boosting importance**, **permutation importance**, **RFE**, and **SHAP** to drop low-value columns (e.g. some room flags) and keep the final 12-feature set.

---

## Section F: Modeling & Algorithms (Q51–Q65)

### Q51. What is the target variable?
**Answer:** Property **price in Crores** (log-transformed with **log1p** during training).

### Q52. Why log-transform the target?
**Answer:** Reduces **skew**, stabilizes variance, and helps linear and ensemble models fit **multiplicative** price effects; predictions are mapped back with **expm1**.

### Q53. Which algorithm did you deploy?
**Answer:** **RandomForestRegressor** with **n_estimators=500** inside a sklearn **Pipeline**.

### Q54. Why Random Forest?
**Answer:** Strong **R² (~0.90 CV)** and **MAE (~0.46 Cr)** in experiments, handles **mixed feature types** with preprocessing, robust to non-linearity, and **simpler ops** than heavy gradient boosting tuning for a capstone deploy.

### Q55. Did XGBoost perform better?
**Answer:** In some encoding setups **XGBoost/Gradient Boosting** showed competitive or slightly better holdout metrics in tables; Random Forest was still a **strong, stable choice** for the final pickle pipeline after GridSearch/experiments.

### Q56. What other algorithms did you compare?
**Answer:** Linear Regression, Ridge, Lasso, SVR, Decision Tree, Random Forest, Extra Trees, Gradient Boosting, AdaBoost, MLP, XGBoost—**11 models** across encoding strategies.

### Q57. What is a sklearn Pipeline and why use it?
**Answer:** Chains **preprocessing + model** so the same steps run on train and predict—prevents **data leakage** from fitting scalers on full data at inference and ensures **reproducible deployment** in one pickle.

### Q58. What is ColumnTransformer?
**Answer:** Applies **different transformers to different column subsets** (numeric vs categorical) in one step—essential for mixed real estate tabular data.

### Q59. Hyperparameter tuning approach?
**Answer:** **GridSearchCV** / cross-validation in `model-selection.ipynb` (e.g. tree count for RF); best params baked into exported `pipeline.pkl`.

### Q60. Would linear regression work alone?
**Answer:** **Baseline only**—R² and MAE were weaker; price relationships with sector and amenities are **non-linear** and need trees or regularized non-linear models.

### Q61. What is overfitting and how did you control it?
**Answer:** Models memorizing training noise; controlled via **CV**, **ensemble averaging** in RF, **feature selection**, and **outlier treatment**—compare train vs CV metrics in notebooks.

### Q62. Bias-variance tradeoff in your project?
**Answer:** Simple linear models **underfit** (high bias); very deep unpruned trees **overfit** (high variance); **Random Forest** reduces variance via bagging while capturing non-linear structure.

### Q63. Can the model extrapolate to new sectors?
**Answer:** **Limited**—one-hot sectors need **seen categories** at training; a new sector may require **retraining**, grouping rare sectors, or **target encoding / hierarchical models**.

### Q64. How do tree models handle missing values in sklearn?
**Answer:** Your pipeline **imputes in notebooks** before training; sklearn RF does not accept NaNs in all versions—** upfront imputation** is the correct design here.

### Q65. What would you use for classification if predicting sold/rent instead?
**Answer:** **Logistic Regression**, **Random Forest Classifier**, or **XGBoost** with **precision-recall** metrics if classes are imbalanced.

---

## Section G: Evaluation Metrics (Q66–Q75)

### Q66. Which metrics did you use for regression?
**Answer:** **R²** (explained variance), **MAE** (mean absolute error in Crores—interpretable for business), and **cross-validation** scores across models.

### Q67. What does MAE ~0.46 Cr mean for a user?
**Answer:** On average, predictions are off by about **₹46 lakh**—useful to set expectations; Gurgaon prices vary widely so sector-level error may differ.

### Q68. Why R² and MAE together?
**Answer:** **R²** shows overall fit; **MAE** shows **typical error in currency units** stakeholders understand—R² alone can hide large errors on expensive properties.

### Q69. Why cross-validation?
**Answer:** Single split can be **lucky/unlucky**; **k-fold CV** gives stable estimates of generalization on ~3.5k rows.

### Q70. What is RMSE vs MAE?
**Answer:** **RMSE** penalizes large errors more (squares); **MAE** is robust and linear in errors. Real estate stakeholders often prefer **MAE in Crores** for communication.

### Q71. How do you show uncertainty in the app?
**Answer:** Currently **fixed band ±0.22 Cr** around point prediction—not from model quantiles. Improvement: **prediction intervals** from quantile regression or CV residual distribution.

### Q72. What is a good R² for real estate price prediction?
**Answer:** **0.85–0.92** on cleaned listing data is strong; perfection is impossible due to **unobserved factors** (view, exact floor, builder premium, negotiation).

### Q73. How would you evaluate the recommender?
**Answer:** Offline: **precision@k**, **similarity sanity checks**, diversity; online: **click-through**, saves, site visits—capstone uses **hybrid cosine scores** and manual validation.

### Q74. Confusion matrix—relevant here?
**Answer:** **Not for price regression**; relevant if you add **classification** tasks (e.g. “undervalued” vs “overvalued” bins).

### Q75. How to explain model performance to a non-technical interviewer?
**Answer:** “On held-out properties, the model’s typical mistake is about **half a crore**, and it explains roughly **90%** of price variation in our historical Gurgaon listings.”

---

## Section H: Streamlit & Deployment (Q76–Q85)

### Q76. How does Streamlit multipage routing work?
**Answer:** Files under **`pages/`** auto appear in the sidebar; `home.py` is the main landing page when you run `streamlit run home.py`.

### Q77. Walk through the price prediction flow in code.
**Answer:** Load `df.pkl` for dropdowns → load/download `pipeline.pkl` → user inputs → build one-row DataFrame → `pipeline.predict()` → `np.expm1()` → display range **±0.22 Cr**.

### Q78. Why pickle for the model?
**Answer:** **Native sklearn serialization** of the full Pipeline—fast to load, one file for demo deployment. Caveat: pickle has **security and version** risks in untrusted environments.

### Q79. What happens if scikit-learn version mismatches?
**Answer:** `pickle.load` can **fail** or behave oddly; you pinned **`scikit-learn==1.6.1`** in requirements and commented version debug in `price_predictor.py` for this reason.

### Q80. How would you deploy on cloud?
**Answer:** **Streamlit Community Cloud**, **AWS EC2/ECS**, or **Docker** container with artifacts in S3; alternatively export to **ONNX** or **MLflow** model registry for a API service.

### Q81. Security concerns with pickle from Google Drive?
**Answer:** Only load **trusted** pickles; in production use **signed artifacts**, **MLflow**, or **joblib** with versioned builds—not arbitrary Drive downloads.

### Q82. How to scale Streamlit for many users?
**Answer:** Streamlit **re-runs script** per interaction; for scale, move inference to **stateless API** with load balancer, cache predictions, and horizontal pods.

### Q83. What is in `df.pkl`?
**Answer:** A DataFrame of training features used to populate **realistic UI dropdown values** (sectors, BHK levels, categories)—not the full raw listing dump.

### Q84. How do you handle slow model download on first run?
**Answer:** Show **“Downloading model…”** via Streamlit; production would **bake model into image** or mount from object storage at startup.

### Q85. Environment management?
**Answer:** Local **`env/`** venv; production would use **`requirements.txt`**, locked versions, and Docker for reproducibility.

---

## Section I: Analytics Dashboard (Q86–Q90)

### Q86. What visualizations are in the analytics module?
**Answer:** **Plotly mapbox** sector bubble map (color = price/sqft), **word clouds** of amenities by sector, **area vs price** scatter (flat/house), **BHK pie**, **BHK price boxplot**, **price histograms** by property type.

### Q87. How is the map colored?
**Answer:** Sector aggregates: **mean price_per_sqft** (and size by built-up area) with lat/long from merged **`data_viz1.csv`**.

### Q88. What is `sector_features.pkl`?
**Answer:** Pickled **sector → list of amenity keywords** for word clouds—shows what facilities dominate each locality.

### Q89. Why Plotly over static matplotlib for the map?
**Answer:** **Interactive zoom/hover** and Mapbox integration—better UX for exploring Gurgaon sectors.

### Q90. What business insight can an investor get from analytics?
**Answer:** Compare **price per sqft across sectors**, BHK mix, and amenity themes to spot **relative value** or **premium localities** before using the price predictor on specific units.

---

## Section J: Recommender System (Q91–Q100)

### Q91. What type of recommender is this?
**Answer:** **Content-based filtering**—similarity from property/project attributes, **not** collaborative filtering (no user-item rating matrix).

### Q92. Explain the three cosine similarity matrices.
**Answer:** **sim1:** TF-IDF on text facilities; **sim2:** one-hot/categorical structure from **BHK/price/area** in PriceDetails JSON; **sim3:** **geo proximity** to landmarks encoded as distance features.

### Q93. Why combine similarities with weights 0.5, 0.8, 1.0?
**Answer:** **Hybrid ensemble**—tune relative importance of text vs configuration vs location; geo weighted highest in your formula to emphasize **landmark proximity** for Gurgaon projects.

### Q94. How does radius search work?
**Answer:** `location_distance.pkl` stores **distances in meters** from each project to landmarks; filter columns where distance **< radius × 1000**, sort, display in km.

### Q95. Why top 5 recommendations?
**Answer:** **Default UX** (`top_n=5`)—enough choice without overwhelming; configurable in `recommend_properties_with_scores`.

### Q96. Cold start problem?
**Answer:** **New projects** not in the 247-row matrix get **no recommendations** until matrix is rebuilt—production needs **incremental updates** when new projects launch.

### Q97. TF-IDF intuition for facilities text?
**Answer:** Highlights amenities **distinctive** to a project vs common words across all listings—cosine similarity finds projects with **similar facility profiles**.

### Q98. Difference between price model and recommender data?
**Answer:** Price model: **thousands of individual listings**, 12 tabular features. Recommender: **247 apartment projects**, rich JSON and text, **precomputed similarity matrices** for speed.

### Q99. How would you improve the recommender?
**Answer:** Learn weights by **validation**, add **user filters** (budget, BHK), use **embeddings** (sentence transformers) for text, add **collaborative** signals if user logs exist.

### Q100. If the interviewer asks “summarize everything in 30 seconds”—what do you say?
**Answer:** “I built a Gurgaon real estate platform: cleaned 99acres data, engineered luxury and furnishing features, trained a **Random Forest Pipeline** for price (~90% R²), deployed **three Streamlit modules**—prediction, Plotly analytics, and a **hybrid cosine recommender** with geo search—using offline notebooks and pickle artifacts for serving.”

---

## Bonus Rapid-Fire (Extra practice)

| # | Question | Short answer |
|---|----------|--------------|
| B1 | pandas vs NumPy? | pandas: labeled tables; NumPy: fast arrays—both used. |
| B2 | One-hot vs label encoding? | One-hot for nominal multi-class (sector); ordinal only when order matters. |
| B3 | What is leakage? | Using future/info not available at prediction time—e.g. price-derived features wrongly included. |
| B4 | SHAP purpose? | Explain **feature contribution** per prediction in experiments. |
| B5 | 99acres bias? | Listings ≠ all transactions; **selection bias** toward marketed inventory. |
| B6 | Crore vs Lac? | Indian units; model standardizes to **Crores**. |
| B7 | Why sectors not lat-long in model? | Sector captures **market microstructure**; lat-long used more in viz/geo recommender. |
| B8 | Gitignore pipeline.pkl why? | Large binary; use Drive/gdown instead. |
| B9 | Multicollinearity concern? | Trees handle it better than linear models; still checked in EDA. |
| B10 | Next feature you’d add? | **Distance to metro**, **builder brand**, **rera status**, fresh scrape dates. |

---

*Good luck at TCS. Rehearse Q1, Q11, Q41, Q51–Q54, Q66, Q91–Q93, and Q100 aloud.*
