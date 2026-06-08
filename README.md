# Archify Backend

Archify Backend is a high-performance API built with **FastAPI** designed for managing and exporting software architecture projects. It serves as the core engine for the Archify platform, allowing architects and developers to design diagrams, persist complex architectural configurations, and automatically generate ready-to-use boilerplate code structures.

The project strictly follows the **Hexagonal Architecture (Ports and Adapters)** pattern to ensure that core business logic remains decoupled from external infrastructure, such as Supabase and FastAPI.

## Features

- **Robust Identity Management**: Deep integration with Supabase Auth for secure registration, login, and JWT-based session validation.
- **Domain-Driven User Profiles**: Support for roles (Admin/User), custom metadata, and avatar management.
- **Architecture Design CRUD**: Manage complex architecture schemas including nodes, edges, connections, and pattern configurations.
- **Advanced Storage Handling**: Integration with Supabase Storage for managing assets (icons, screenshots) with support for both public access and secure signed URLs.
- **Automated Code Export Engine**: A specialized service that transforms architectural diagrams into a downloadable ZIP package containing:
    - A dynamically generated `README.md` documenting the architecture components.
    - A `src/` directory structure with Python boilerplate code for every component.
    - Automatic slugification and normalization of component names for clean file systems.
- **Security First**: Strict input sanitization via `bleach`, validation using Pydantic v2, and Row Level Security (RLS) enforcement at the database level.

## Tech Stack

- **Language**: Python 3.13+ (configured in `pyproject.toml`)
- **Framework**: FastAPI
- **Dependency Management**: uv
- **Validation**: Pydantic v2
- **BaaS**: Supabase (PostgreSQL, GoTrue Auth, Storage)
- **Architecture**: Hexagonal (Ports and Adapters)

## Security Model

Authentication and session management are delegated to Supabase using GoTrue. The backend does not implement a custom auth system; instead, it relies on Supabase Auth for:

- user registration and login
- JWT issuance and validation
- secure session lifecycle management
- role metadata attached to user profiles

The application uses Supabase as the source of truth for identity, and backend endpoints assume valid JWT tokens or authenticated requests. This separation keeps the backend focused on business logic, while Supabase handles user authentication, password flows, and secure token management.

## Architecture Overview

The system is organized into three distinct layers:

1.  **API Layer (`app/api`)**: Responsible for handling HTTP requests, defining FastAPI routers, and managing dependency injection.
2.  **Domain Layer (`app/domain`)**: The "Pure" logic layer. It contains the business rules, Pydantic models (Entities), and Port interfaces. It is entirely independent of Supabase or FastAPI.
3.  **Infrastructure Layer (`app/infrastructure`)**: Contains the concrete implementations (Adapters) of the domain ports, such as Supabase repositories and storage handlers.

## Project Structure

```text
app/
├── api/
│   ├── dependencies.py    # DI for Services and Repositories
│   └── endpoints/         # FastAPI Routers (projects, users, images, etc.)
├── domain/
│   ├── architectures/     # Logic for architectural diagrams
│   ├── auth/              # Domain-specific authentication logic
│   ├── code_languages/    # Programming language metadata
│   ├── images/            # Image asset management and metadata
│   ├── patterns/          # Design pattern definitions
│   ├── patterns_code/     # Code generation logic for specific patterns
│   ├── projects/          # Project CRUD and the ZIP Export Engine
│   └── users/             # User profile entities and roles
└── infrastructure/
    └── supabase/          # Concrete adapters for Supabase services
```

## Setup and Installation

Before anything else, you must have a Supabase account. If you do not already have one, register at https://supabase.com and create a new project before continuing.

### 1. Supabase Initialization
If you have Docker and Node installed locally, use the files in `database_dump/` to create and populate the database automatically:

```bash
cd database_dump
npm install
npx supabase init
npx supabase start
```

This will create the local Supabase database and apply the migrations and seed data for you.

If you do not have Docker installed, initialize the database through the Supabase web interface instead:

- Open your Supabase project dashboard.
- Run the SQL scripts in `database_dump/supabase/migrations/*` in order.
- Then run `database_dump/supabase/seed.sql` to populate the database with seed data.

### 2. Environment Variables
Create a `.env` file in the root directory with your Supabase credentials:
```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_project_api_key
SUPABASE_STORAGE_BUCKET=archify
SUPABASE_STORAGE_PUBLIC=true
```

### 3. Dependency Installation
This project uses `uv` for dependency management.

**If you do not have `uv` installed**, install it with one of the following commands:

- **Windows (PowerShell):**
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **macOS / Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

Once installed, synchronize the project:
```bash
uv sync
```

### 4. Running the Application
```bash
uvicorn app.main:app --reload
```

Once running, you can access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.
