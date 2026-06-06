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

from typing import Optional

def greet(name: str, times: int = 1) -> str:
    return (name + " ") * times

def find_user(user_id: int) -> Optional[str]:
    users = {1: "Taher", 2: "Ali"}
    return users.get(user_id)  # returns str or None

# ... block 2 code

def process(nums: list[int]) -> dict[str, int]:
    return {"sum": sum(nums), "count": len(nums)}

def merge(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {**a, **b}

def parse(value: str | int | None) -> str:
    if value is None:
        return "nothing"
    return str(value)

UserID = int
UserMap = dict[UserID, str]

def get_users() -> UserMap:
    return {1: "Taher", 2: "Ali"}

# --- Block 3: Classes ---

class User:
    # class variable — shared by ALL instances
    total_users: int = 0

    def __init__(self, name: str, age: int) -> None:
        # instance variables — unique to each instance
        self.name = name
        self.age = age
        User.total_users += 1

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, age={self.age})"

    def __str__(self) -> str:
        return f"{self.name}, age {self.age}"

    def greet(self) -> str:
        return f"Hi, I'm {self.name}"

u1 = User("Taher", 20)
u2 = User("Ali", 22)
print(repr(u1))          # User(name='Taher', age=20)
print(str(u1))           # Taher, age 20
print(User.total_users)  # 2

# ... block 3 code

class User:
    total: int = 0

    def __init__(self, name: str) -> None:
        self.name = name
        User.total += 1

    def instance_method(self) -> str:
        # has access to self (the instance)
        return f"I am {self.name}"

    @classmethod
    def class_method(cls) -> str:
        # has access to cls (the class itself)
        return f"Total users: {cls.total}"

    @staticmethod
    def static_method() -> str:
        # no access to instance or class
        return "I'm just a function that lives here"


class AdminUser(User):
    def __init__(self, name: str, level: int) -> None:
        super().__init__(name)   # call parent __init__
        self.level = level

    def instance_method(self) -> str:
        return f"Admin {self.name} (level {self.level})"


admin = AdminUser("Taher", 5)
print(admin.instance_method())  # Admin Taher (level 5)
print(admin.class_method())     # Total users: 1
print(admin.static_method())    # I'm just a function that lives here

# --- Block 4: Decorators ---

def outer(x: int):
    def inner(y: int) -> int:
        return x + y      # inner "closes over" x
    return inner          # returns the function itself

add5 = outer(5)
print(add5(3))   # 8
print(add5(10))  # 15

# ... block 4 code

import time
from functools import wraps
from typing import Callable, Any

def timer(func: Callable) -> Callable:
    @wraps(func)               # preserves original function metadata
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)   # call the original function
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total

result = slow_function(1_000_000)
# slow_function took 0.0821s

def repeat(times: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello(name: str) -> None:
    print(f"Hello {name}")

say_hello("Taher")
# Hello Taher
# Hello Taher
# Hello Taher

# --- Block 5: BankAccount (write this yourself) ---

from typing import Any, Callable, TypeVar, ParamSpec
import functools

# Type variables for decorator signature preservation
P = ParamSpec("P")
R = TypeVar("R")

def validate_positive(func: Callable[P, R]) -> Callable[P, R]:
    """
    Decorator that raises a ValueError if any numeric argument (int or float)
    passed to the function is less than or equal to zero.
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # Check positional arguments
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError("Numeric arguments must be strictly positive (greater than 0).")
                
        # Check keyword arguments
        for key, value in kwargs.items():
            if isinstance(value, (int, float)) and value <= 0:
                raise ValueError("Numeric arguments must be strictly positive (greater than 0).")
                
        return func(*args, **kwargs)
    return wrapper


class BankAccount:
    # Class variable tracking total accounts created
    total_accounts: int = 0

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner: str = owner
        self.balance: float = balance
        BankAccount.total_accounts += 1

    @validate_positive
    def deposit(self, amount: float) -> None:
        """Adds a positive amount to the account balance."""
        self.balance += amount

    @validate_positive
    def withdraw(self, amount: float) -> bool:
        """
        Deducts a positive amount from the account balance.
        Returns False if there are insufficient funds, otherwise True.
        """
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"

    def __str__(self) -> str:
        return f"Account Owner: {self.owner} | Balance: ${self.balance:,.2f}"


# --- Quick Smoke Test Verification ---
if __name__ == "__main__":
    acc = BankAccount("Alice", 100.0)
    print(acc)  # Account Owner: Alice | Balance: $100.00
    
    # Test valid actions
    acc.deposit(50.50)
    assert acc.balance == 150.50
    
    assert acc.withdraw(200.0) is False  # Insufficient funds
    assert acc.withdraw(50.50) is True   # Success
    
    # Test decorator enforcement
    try:
        acc.deposit(-10)
    except ValueError as e:
        print(f"Caught expected error on negative deposit: {e}")
        
    try:
        acc.withdraw(0)
    except ValueError as e:
        print(f"Caught expected error on zero withdrawal: {e}")
        
    print(f"Total accounts tracked: {BankAccount.total_accounts}")

# ... your code here