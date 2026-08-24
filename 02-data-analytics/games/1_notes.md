**1. Modules**
- *Evidence:* "Uses a separate file called `trade_math.py`."
- *Why it fits:* Any `.py` file is automatically a module - code split into its own file so it can be reused elsewhere.

**2. Importing (`import` / `from...import`)**
- *Evidence:* "Imports functionality from that file."
- *Why it fits:* To use code from `trade_math.py` in another file, you must bring it in with `import trade_math` or `from trade_math import classify_trade`.

**3. Docstrings**
- *Evidence:* "Contains documentation for the module and its functions."
- *Why it fits:* Python's built-in way to document a module or function is a docstring - a string literal right under the `def`/module top, accessible via `.__doc__` or `help()`.

**4. Default parameter values**
- *Evidence:* "Has a trade classification function with a default threshold of 20,000."
- *Why it fits:* A default argument like `def classify_trade(amount, threshold=20000):` lets the function be called without always specifying threshold.

**5. Built-in exception types**
- *Evidence:* "Encounters invalid types, invalid values, missing list items, missing dictionary keys, division by zero, missing names, missing attributes, missing files, import problems, and invalid syntax."
- *Why it fits:* Each phrase maps directly to a specific built-in exception:
  - invalid types → `TypeError`
  - invalid values → `ValueError`
  - missing list items → `IndexError`
  - missing dictionary keys → `KeyError`
  - division by zero → `ZeroDivisionError`
  - missing names → `NameError`
  - missing attributes → `AttributeError`
  - missing files → `FileNotFoundError`
  - import problems → `ImportError`
  - invalid syntax → `SyntaxError`

**6. Multiple `except` blocks**
- *Evidence:* "Has mechanisms to handle problems differently."
- *Why it fits:* A single `try` can be followed by several `except SpecificError:` blocks, each responding differently depending on which exception type occurred.

**7. `else` clause on try/except**
- *Evidence:* "Has a path that runs when nothing goes wrong."
- *Why it fits:* The `else:` block in a try statement executes only if no exception was raised.

**8. `finally` clause**
- *Evidence:* "Performs one action regardless of whether something goes wrong."
- *Why it fits:* `finally:` always runs, whether an exception occurred or not - commonly used for cleanup (closing files, releasing resources).

**9. Raising a custom/deliberate exception**
- *Evidence:* "Deliberately creates a special error for an invalid trade."
- *Why it fits:* This is a `raise` statement - likely raising a custom exception class (e.g., `class InvalidTradeError(Exception):`) to signal a specific business-rule violation.

**10. Exception chaining (`raise ... from ...`)**
- *Evidence:* "Passes an error upward while preserving its original cause."
- *Why it fits:* `raise NewError("...") from original_error` re-raises a new exception while keeping the original traceback/cause attached - Python shows this as "The above exception was the direct cause of...".

**11. `continue` statement**
- *Evidence:* "Skips a bad trade and continues processing."
- *Why it fits:* Inside a loop over trades, `continue` skips the rest of the current iteration and moves to the next trade without stopping the whole loop.

**12. `if __name__ == "__main__":` guard**
- *Evidence:* "Contains instructions that should run only when the file is executed directly."
- *Why it fits:* This is the standard Python idiom ensuring code runs only when the script is executed directly, not when it's imported as a module elsewhere.

## How the concepts connect

The story is a single coherent program lifecycle:
- `trade_math.py` is a **module** with **docstrings**, containing a classification **function** with a **default argument** (threshold=20,000).
- The main program **imports** it.
- When processing trades, various **built-in exceptions** occur.
- A `try` block wraps the risky code, with **multiple except blocks** handling each exception type differently.
- If a trade is invalid by business logic (not a Python error), the code **raises a custom exception deliberately**.
- That error may be **re-raised with chaining** so the original cause isn't lost as it propagates up.
- If a trade fails, `continue` **skips it** and the loop moves to the next one.
- If nothing goes wrong, the `else` block runs the success path.
- Regardless of outcome, `finally` guarantees cleanup always happens.
- All of this only executes when the script is run directly, thanks to the `__main__` guard - so importing the module elsewhere doesn't trigger it.

Together this tells the story of a trading script that reads trades, classifies them against a $20,000 threshold, and has to survive a gauntlet of real-world data problems (bad types, missing files, zero division, etc.) without crashing - using structured exception handling to isolate, report, and recover from each failure.