# プロジェクト構造

- **.vscode/**
  - launch.json
- **backend/**
  - **app/**
    - **api/**
      - __init__.py
      - chat.py
      - settings.py
    - **core/**
      - config.py
      - db.py
      - events.py
    - **exceptions/**
      - __init__.py
      - base.py
      - handlers.py
      - http.py
    - **models/**
      - documents.py
      - files.py
      - uploaded_file.py
    - **routers/**
      - __init__.py
      - base.py
      - chat.py
      - files.py
      - settings.py
    - **schemas/**
      - auth.py
      - chat.py
      - data.py
      - settings.py
    - **services/**
      - embedding.py
      - storage.py
    - **utils/**
      - files.py
      - llm_util.py
    - main.py
  - **tests/**
  - **uploads/**
  - requirements.txt
- **docker/**
  - backend.Dockerfile
  - frontend.Dockerfile
- **frontend/**
  - **assets/**
  - **components/**
    - __init__.py
    - chat.py
    - settings.py
  - **utils/**
    - __init__.py
    - api.py
  - app.py
- **memory/**
  - api_docs.md
  - features.md
  - last_update.md
  - project_structure.md
  - setup_guide.md
  - tech_stack.md
- **requirements/**
  - backend.txt
  - base.txt
  - frontend.txt
  - requirements.txt
- **tasks/**
  - README_RE_WRITE.md
- .env
- .env.example
- .gitignore
- .python-version
- docker-compose.yml
- pyproject.toml
- README.md
