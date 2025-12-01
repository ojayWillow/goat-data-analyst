# SYSTEM OVERVIEW

High-level view of GOAT Data Analyst backend and tooling.

## Start Here (Core Pipeline)

- `app.py`  |  Layer: `frontend_streamlit`  |  AI analysis failed: 'list' object has no attribute 'message'
- `backend\analytics\ai_insights.py`  |  Layer: `analytics_engine`  |  AI analysis failed: 'list' object has no attribute 'message'
- `backend\analytics\insights_engine.py`  |  Layer: `analytics_engine`  |  AI analysis failed: 'list' object has no attribute 'message'
- `backend\data_processing\profiler.py`  |  Layer: `other`  |  AI analysis failed: 'list' object has no attribute 'message'
- `backend\domain_detection\__init__.py`  |  Layer: `analytics_engine`  |  AI analysis failed: 'list' object has no attribute 'message'
- `backend\domain_detection\ai_domain_detector.py`  |  Layer: `analytics_engine`  |  AI analysis failed: 'list' object has no attribute 'message'
- `backend\domain_detection\domain_detector.py`  |  Layer: `analytics_engine`  |  AI analysis failed: 'list' object has no attribute 'message'
- `backend\domain_detection\patterns.py`  |  Layer: `analytics_engine`  |  AI analysis failed: 'list' object has no attribute 'message'
- `backend\export_engine\ultimate_report.py`  |  Layer: `export_report_layer`  |  AI analysis failed: 'list' object has no attribute 'message'
- `main.py`  |  Layer: `api_backend`  |  AI analysis failed: 'list' object has no attribute 'message'
- `sample_data\app.py`  |  Layer: `frontend_streamlit`  |  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99386, Requested 692. Please try again in 1m7.391999999s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
- `test_ai_domains.py`  |  Layer: `other`  |  AI analysis failed: 'list' object has no attribute 'message'
- `tests\app.py`  |  Layer: `frontend_streamlit`  |  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99987, Requested 244. Please try again in 3m19.584s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}

## Layers

The project is roughly organized into these layers:

### Frontend (Streamlit UI) (`frontend_streamlit`)

- `app.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `sample_data\app.py`  →  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99386, Requested 692. Please try again in 1m7.391999999s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
- `tests\app.py`  →  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99987, Requested 244. Please try again in 3m19.584s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}

### Other / Misc (`other`)

- `backend\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\ai_engine\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\analyzers\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\api\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\connectors\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\connectors\csv_handler.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\data_processing\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\data_processing\profiler.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `performance_test.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `test_ai_domains.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `test_app_and_api.py`  →  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99987, Requested 1061. Please try again in 15m5.472s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
- `test_live_deployment.py`  →  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99987, Requested 1044. Please try again in 14m50.784s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
- `tests\__init__.py`  →  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99987, Requested 246. Please try again in 3m21.312s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
- `tests\integration\__init__.py`  →  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99987, Requested 248. Please try again in 3m23.04s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}
- `tests\unit\__init__.py`  →  AI analysis failed: Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01kb7mt506e9pat70nm4fycb5b` service tier `on_demand` on tokens per day (TPD): Limit 100000, Used 99987, Requested 248. Please try again in 3m23.04s. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}

### Analytics / Insights Engine (`analytics_engine`)

- `backend\analytics\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\analytics\ai_insights.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\analytics\insights_engine.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\analytics\simple_analytics.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\analytics\visualizations.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\domain_detection\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\domain_detection\ai_domain_detector.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\domain_detection\domain_detector.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\domain_detection\patterns.py`  →  AI analysis failed: 'list' object has no attribute 'message'

### Export / Report Generation (`export_report_layer`)

- `backend\export_engine\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\export_engine\quality_report.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\export_engine\ultimate_report.py`  →  AI analysis failed: 'list' object has no attribute 'message'

### Tooling / Monitoring / Docs (`tooling_monitoring`)

- `backend\monitoring\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\monitoring\ai_code_reader.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\monitoring\doc_generator.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\monitoring\file_watcher.py`  →  AI analysis failed: 'list' object has no attribute 'message'

### Visualization / Charts (`visualization_layer`)

- `backend\visualizations\__init__.py`  →  AI analysis failed: 'list' object has no attribute 'message'
- `backend\visualizations\universal_charts.py`  →  AI analysis failed: 'list' object has no attribute 'message'

### API Backend (FastAPI) (`api_backend`)

- `main.py`  →  AI analysis failed: 'list' object has no attribute 'message'

## Dependency Hotspots

Modules that are imported the most (higher = more critical / central).

- No imports detected.
