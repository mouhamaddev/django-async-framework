<h1 style="vertical-align: middle;">
  Welcome to Django Async Framework
  <svg xmlns="http://www.w3.org/2000/svg" width="30" viewBox="0 0 24 24" 
       style="vertical-align: middle; fill: #757575;">
    <path d="M19.14 7.5A2.86 2.86 0 0 1 22 10.36v3.78A2.86 2.86 0 0 1 19.14 17H12c0 .39.32.96.71.96H17v1.68a2.86 2.86 0 0 1-2.86 2.86H9.86A2.86 2.86 0 0 1 7 19.64v-3.75a2.85 2.85 0 0 1 2.86-2.85h5.25a2.85 2.85 0 0 0 2.85-2.86V7.5zm-4.28 11.79c-.4 0-.72.3-.72.89s.32.71.72.71a.71.71 0 0 0 .71-.71c0-.59-.32-.89-.71-.89m-10-1.79A2.86 2.86 0 0 1 2 14.64v-3.78A2.86 2.86 0 0 1 4.86 8H12c0-.39-.32-.96-.71-.96H7V5.36A2.86 2.86 0 0 1 9.86 2.5h4.28A2.86 2.86 0 0 1 17 5.36v3.75a2.85 2.85 0 0 1-2.86 2.85H8.89a2.85 2.85 0 0 0-2.85 2.86v2.68zM9.14 5.71c.4 0 .72-.3.72-.89s-.32-.71-.72-.71c-.39 0-.71.12-.71.71s.32.89.71.89" />
  </svg>
</h1>


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

## Useful Links

<p>
  <a target="_blank" href="https://github.com/mouhamaddev/django-async-framework" style="text-decoration:none;">
    <button style="padding:10px 15px; font-size:14px; color:white; background-color:#24292e; border:none; border-radius:5px; cursor:pointer;">
      GitHub Repository
    </button>
  </a>
</p>

<p>
  <a target="_blank" href="https://pypi.org/project/djangoasyncframework/" style="text-decoration:none;">
    <button style="padding:10px 15px; font-size:14px; color:white; background-color:#2094F3; border:none; border-radius:5px; cursor:pointer;">
      PyPI Package
    </button>
  </a>
</p>

<br>

Your feedback, bug reports, and contributions are very welcome.
<br>
Stay tuned Djangonauts ❤️