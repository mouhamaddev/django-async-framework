Date: 15-5-2025

Today I Learned:
- dispatch() is the method that routes the request to get(), post(), or whatever the method was.
- If I want to handle something no matter what HTTP method is used then I should overrite dispatch().
- View class (django.views) does two core thigs:
    - as_view() Method: Converts a class into a callable view function to be used in urls.py.
    - dispatch(): Routes request to the correct HTTP method.


Date: 16-5-2025

Today I Learned:
- Learned how to write a simple function-based middleware.


Date: 17-5-2025

Today I Learned:
- That feeling overwhelmed while building something like this is completely normal, in fact, it’s a sign that I’m working on something meaningful :D.


Date: 20-5-2025

Today I Learned:
- Django’s built-in throttling (via DRF) is sync-based and tied to DRF.


Date: 21-5-2025

Today I Learned:
- That integrating throttling into AsyncAPIView requires hooking into the dispatch() method before the actual view handler is called to ensure rate limits being enforced before any expensive logic runs.