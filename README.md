# Welcome to Django Async Framework

Welcome to the lightweight, fully asynchronous class-based view framework built on top of Django.

<br>

DAF is a minimalistic framework designed to bring true async support to Django’s class-based views. It enforces the use of `async def` HTTP method handlers, enabling developers to write modern, non-blocking web APIs and services using Django.

## So.. Why DAF?

Django is powerful, but its async support is incomplete. Some parts are async-friendly, while others are still blocking (`ORM`, `serializers`, `middleware`). Django Async Framework aims to solve this by providing a fully async-first development experience, similar to how Django REST Framework (DRF) standardized API development.

## Setup and Installation

Getting started with DAF is quick and easy:

1. Install the package via pip:

```bash
pip install djangoasyncframework
```

2. **Add `async_framework` to your `INSTALLED_APPS`** in your Django project's `settings.py`:

```python
INSTALLED_APPS = [
    # other apps ...
    'async_framework',
]
```

## Status

DAF is an early-stage, open-source project currently under active development. It’s intended for developers who want to experiment with async Django or build async APIs while waiting for official Django async features to mature.

## Why This Matters
Django needs a true async-first framework, not just patches to existing sync-based components. DRF standardized API development, DAF aims to do the same for async Django.

<br>

Your feedback, bug reports, and contributions are very welcome.
<br>
Stay tuned Djangonauts ❤️
