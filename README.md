# Welcome to Django Async Framework

Welcome to the lightweight, fully asynchronous class-based view framework built on top of Django.

<br>

Django Async Framework is a lightweight library that adds true asynchronous support to Django’s class-based views, allowing developers to build non-blocking web APIs and services.

## So.. Why Async Framework?

Django is powerful, but its async support is incomplete. Some parts are async-friendly, while others are still blocking (ORM, serializers, middleware). Django Async Framework aims to solve this by providing a fully async-first development experience, similar to how Django REST Framework standardized API development.

## Setup and Installation

Getting started with Async Framework is quick and easy:

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

Django Async Framework is an early-stage open-source project currently under active development. It’s intended for developers who want to use Django’s async capabilities and support the ongoing development of a reliable and stable async framework.

## Why This Matters
Django needs a true async-first framework, not just patches to existing sync-based components. DRF standardized API development, DAF aims to do the same for async Django.

Your feedback, bug reports, and contributions are very welcome.
<br>
Stay tuned Djangonauts ❤️
