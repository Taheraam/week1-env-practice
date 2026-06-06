# ============================================================
# Day 2 — Python reboot
# ============================================================

# --- Block 1: Functions ---

def func(*args, **kwargs):
    print(args)    # tuple of positional args
    print(kwargs)  # dict of keyword args

func(1, 2, 3, name="Taher", age=20)
# (1, 2, 3)
# {'name': 'Taher', 'age': 20}

# ... rest of block 1 code

def func(positional, /, normal, *, keyword_only):
    pass

# / means: everything before me must be positional
# * means: everything after me must be keyword-only

def bad(items=[]):       # NEVER do this
    items.append(1)
    return items

def good(items=None):    # always do this
    if items is None:
        items = []
    items.append(1)
    return items

def square(x: int) -> int:
    return x ** 2

def apply(func, value):   # passing a function as argument
    return func(value)

result = apply(square, 5)  # 25

# --- Block 2: Type hints ---

# ... block 2 code

# --- Block 3: Classes ---

# ... block 3 code

# --- Block 4: Decorators ---

# ... block 4 code

# --- Block 5: BankAccount (write this yourself) ---

# ... your code here