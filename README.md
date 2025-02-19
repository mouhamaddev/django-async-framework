# [Django Async Framework (DAF)](https://github.com/mouhamaddev/django-async-framework)

## 📢 About DAF

Django is powerful, but its async support is incomplete. Some parts are async-friendly (`ASGI`, `async views`), while others are still blocking (`ORM`, `serializers`, `middleware`). The **Django Async Framework (DAF)** aims to solve this by providing a **fully async-first development experience**, similar to how Django REST Framework (DRF) standardized API development.

This is a project I'll be working on to bring native async support to Django in a structured way.

## Goals
✅ Provide a **non-blocking async ORM** for Django.
✅ Standardize **async views, serializers, and middleware**.
✅ Remove the confusion around what is async-safe and what isn't.
✅ Reduce the need for Celery by enabling native async background tasks.
✅ Improve Django's performance for I/O-heavy applications.

## Contributing
Since this is an experimental project, contributions, feedback, and discussions are welcome! Feel free to open issues or PRs.

## License
TBD

## Why This Matters
Django needs a true **async-first** framework, not just patches to existing sync-based components. **DRF standardized API development—DAF aims to do the same for async Django.**

Stay tuned Djangonauts!
