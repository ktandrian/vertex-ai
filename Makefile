include .env

install:
	@ python -m venv .venv
	@ source .venv/bin/activate && pip install -r requirements.txt

run:
	@ streamlit run Home.py

deploy:
	@ gcloud run deploy fyber-vertex --region=asia-southeast2 --source=. --project=${PROJECT_ID}
