# Agentic procurement automation for seamless business alignment and negotiation

## Local Setup

- .env file for using Google AI Studio
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- .env file for using Vertex AI
```
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=xxxxxxxxxxxxxxxxxxxx
GOOGLE_CLOUD_LOCATION=us-central1
```

- Set venv
```python -m venv env```

- Activate env Windows (Command Prompt)
```cmd
env\Scripts\activate
```

- Activate env macOS / Linux (bash/zsh)
```bash
source env/bin/activate
```
- Install dependencies
```pip install -r requirements.txt```

- Set auth for vertex AI
```gcloud auth application-default login```

- Setup procurement_agent backend
```uvicorn procurement_agent.agent:a2a_app --host localhost --port 8080```

- Run web adk
```adk web```

## Design diagram
[Draw.io](https://drive.google.com/file/d/1fT_bW_rGkJ4WmbiMt6gfOIk78Mv-F4Gk/view?usp=drive_link)
