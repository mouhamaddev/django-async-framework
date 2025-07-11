# [Django Async Framework](https://mouhamaddev.github.io/django-async-framework/)

[![pypi-version]][pypi]

Django Async Framework is a lightweight class-based view framework built on top of Django.

## Overview
Django is a powerful web framework, but its async support is still a work in progress. Some parts play well with async, others don’t. Django Async Framework aims to fill in those gaps by giving a fully async-first way to build with Django.

### Getting Started

1. Install it with pip:

```bash
pip install djangoasyncframework
```

2. Add it to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # your other apps...
    'async_framework',
]
```

### Why This Matters

Django deserves a modern async-first ecosystem, not just patches around old sync components. It provides a structured foundation for writing asynchronous code in Django without relying on sync-based workarounds.


### Project Status

This is an early-stage open-source project that’s still growing. We’d love your feedback, ideas, bug reports, and contributions.

<br>

Stay tuned, Djangonauts ❤️

[pypi-version]: https://img.shields.io/pypi/v/djangoasyncframework.svg
[pypi]: https://pypi.org/project/djangoasyncframework/
