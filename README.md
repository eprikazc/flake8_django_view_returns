# flake8_django_view_returns

A flake8 plugin that warns when Django view returns None or implicit None

**Example:**

```python
# views.py
def home(request):  # Triggers: DJV001 Django view-like callable returns None
    return None
```
