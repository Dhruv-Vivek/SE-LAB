# Lab 5: Static Code Analysis — Issue Documentation

Target file: `tournament_scoreboard.py`

## Identified Issues

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command injection risk (B605) | Security — High | 71 | `os.system()` executes a command assembled using the server value. | Validate the server identifier and use `subprocess.run()` with an argument list and no shell. |
| Unsafe temporary filename (B306) | Security — Medium | 66 | `tempfile.mktemp()` can create a race condition because the file is not securely created. | Use `tempfile.NamedTemporaryFile()` with `delete=False`. |
| Hard-coded password (B105) | Security — Low | 6 | A referee password is stored directly in source code and is unused. | Remove the unused hard-coded credential. |
| Insecure random generator (B311) | Security — Low | 61 | The standard `random` generator is unsuitable for security-sensitive randomness. | Use `secrets.choice()` for the coin toss. |
| Mutable default argument (W0102) | Code quality | 11 | `players=[]` can share a mutable list between calls. | Use `None` as the default and initialize a new list inside the function. |
| Missing module and function docstrings (C0114/C0116) | Code quality | Multiple | Functions and the module lack documentation. | Add descriptive docstrings. |
| Non-standard naming (C0103) | Code quality | Multiple | Function and parameter names use camelCase instead of snake_case. | Rename functions and parameters using snake_case. |
| Unnecessary `elif` after `return` (R1705) | Code quality | 17 | An `elif` is unnecessary after the preceding branch returns. | Use a separate `if` and a final `return`. |
| Redundant top-two comparisons (R1714) | Code quality | 58 | Two equality checks can be simplified. | Use membership in the first two league-table entries. |
| Whitespace before dictionary colon (E203) | Style | 5 | Inconsistent dictionary formatting. | Remove the space before the colon. |
| Missing blank lines (E302) | Style | 60 | A function definition lacks the required separation. | Add the required blank lines between top-level functions. |
| Incorrect comment indentation and excessive line length (E114/E501) | Style | 86 | An inline comment is incorrectly indented and exceeds the configured line length. | Move the explanation to a separate, properly indented line. |
| Missing whitespace after comma (E231) | Style | 79 | Function arguments are not consistently separated by spaces. | Add the required whitespace. |
| Inline comment spacing (E261) | Style | 87 | An inline comment lacks sufficient preceding whitespace. | Correct the comment spacing or move it to its own line. |

## Verification

- Original Pylint score: 4.75/10
- Final Pylint score: 10.00/10
- Final Flake8 run: no reported violations
- Final Bandit run: no reported findings

Note: Line numbers refer to the original script and may differ after corrections. The Bandit report uses targeted suppressions for reviewed subprocess usage; these should be disclosed when interpreting the final result.
