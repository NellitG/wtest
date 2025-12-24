# Copilot / AI agent instructions

Purpose: provide concise, actionable guidance so an AI coding agent can be immediately productive in this repository.

- **Repo type:** Django project template (minimal). See [README.md](../README.md). The repo currently contains a template README and `requirements.txt`.
- **Activate environment (Windows):** `env\\Scripts\\activate` (README shows the virtualenv is already created).
- **Install deps:** `pip install -r requirements.txt` (or `pip install django` per README when starting from scratch).

- **Common commands you'll need:**
  - Create project (as in README): `django-admin startproject project name .`
  - Create app: `python manage.py startapp appname`
  - Run migrations: `python manage.py migrate`
  - Run dev server: `python manage.py runserver`

- **Project-specific conventions discovered:**
  - The README instructs adding `'restframework'` and the app name to `INSTALLED_APPS` in `settings.py`. When modifying `INSTALLED_APPS`, follow the same placement and naming style used in the README.
  - File locations: `settings.py` (standard Django layout) is the canonical place for app registration and configuration.

- **What to look for when changing code:**
  - Confirm `manage.py` commands succeed locally (migrations, runserver).
  - When adding APIs or serializers, prefer the `restframework` / DRF-style patterns implied by the README.

- **Debugging / testing notes:**
  - There are no tests in the template. If you add tests, run them with `python manage.py test`.

- **Merge guidance (for other AI agents):**
  - Keep changes minimal and Django-idiomatic. Prefer editing `settings.py`, `urls.py`, and `apps.py` in their usual locations.
  - If adding dependencies, update `requirements.txt` and include the install command in PR descriptions.

- **Files to inspect for context:**
  - `README.md` — primary setup instructions and the source of several repository conventions.
  - `requirements.txt` — dependency list used for environment setup.

If any of the above assumptions are incorrect (for example, the intended `INSTALLED_APPS` entry is `rest_framework` rather than `restframework`), ask the maintainers before making large changes.

---
Please review — tell me any missing integration points or commands to include (e.g., CI rules, database setup, or preferred app layout).
