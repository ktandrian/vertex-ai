# Vertex AI Showcase

Demo application built to showcase Vertex AI and Gemini model capabilities. This demo is powered by Streamlit and Langchain.

## Getting Started

1. Install Python to your machine.
2. Run `./scripts/setup.sh` to create a Python virtual environment and install packages.
3. Run `./scripts/devserver.sh` to run Streamlit server in development.
4. Access the application from [http://localhost:8501](http://localhost:8501).

## Lint Application

Run `./scripts/lint.sh` to lint the application.

## Deploying to Cloud Run

Run this command to deploy to Jakarta region with service name `vertex`.

```
gcloud run deploy vertex --region asia-southeast2 --source .
```

Add `--allow-unauthenticated` flag to enable public access.

## Contact

For any inquiries, feel free to contact the creator through [kentandrian@google.com](mailto:kentandrian@google.com).

##

&copy; KenTandrian 2024.
