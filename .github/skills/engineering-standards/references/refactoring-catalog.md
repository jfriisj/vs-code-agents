# Engineering Catalogs: Refactoring & Design

This document serves as a reference for agents to transform code from "smelly" or rigid states into clean, maintainable, and standard-compliant structures.

## Triad of Truth Documentation Protocol
When performing a refactoring or implementing a design pattern:
1. **Markdown (`agent-output/`)**: Document the "Before" vs. "After" state in your implementation artifact.
2. **Obsidian (`workflows/`)**: Create a `WF-[ID]` node if the refactoring changes a system-wide boundary or architecture.
3. **Planka**: Add specific checklist items to the Epic card (e.g., "Extract validation logic to separate class").

---

## 1. Refactoring Catalog

### Extract Method
**When:** A code block can be grouped with a descriptive name to improve readability or SRP.
```python
# Before
def process():
    if not x: raise Error
    if not y: raise Error
    result = complex_operation()

# After
def process():
    validate_input(x, y)
    result = complex_operation()

def validate_input(x, y):
    if not x: raise Error
    if not y: raise Error

```

### Extract Class

**When:** A class has multiple responsibilities (violating SRP).

```python
# Before
class Order:
    def calculate_total(self): ...
    def format_invoice(self): ...
    def send_email(self): ...

# After
class Order:
    def calculate_total(self): ...

class InvoiceFormatter:
    def format(self, order): ...

class OrderNotifier:
    def send_email(self, order): ...

```

### Replace Conditional with Polymorphism

**When:** A switch/case or if/else chain checks types to determine behavior (violating OCP).

```python
# Before
def calculate_pay(employee):
    if employee.type == "hourly":
        return hours * rate
    elif employee.type == "salary":
        return annual / 12

# After
class HourlyEmployee:
    def calculate_pay(self):
        return self.hours * self.rate

class SalariedEmployee:
    def calculate_pay(self):
        return self.annual / 12

```

### Introduce Parameter Object

**When:** The same group of parameters consistently appear together in multiple functions.

```python
# Before
def search(start_date, end_date, min_price, max_price): ...

# After
@dataclass
class SearchCriteria:
    start_date: date
    end_date: date
    min_price: float
    max_price: float

def search(criteria: SearchCriteria): ...

```

### Guard Clause

**When:** Deeply nested conditionals obscure the primary "happy path" (violating KISS).

```python
# Before
def process(x):
    if x:
        if x.valid:
            if x.ready:
                return do_work(x)
    return None

# After
def process(x):
    if not x: return None
    if not x.valid: return None
    if not x.ready: return None
    return do_work(x)

```

