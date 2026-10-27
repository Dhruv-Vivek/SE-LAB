# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing it to identify potential defects, security vulnerabilities, and style violations. It helps developers detect problems early, improve maintainability, and apply consistent coding practices.

## 2. What are the differences between Pylint, Bandit, and Flake8?

Pylint focuses on code quality, naming conventions, documentation, and potential programming mistakes. Bandit examines Python code for common security risks, such as unsafe shell execution and insecure functions. Flake8 checks style and formatting violations, including whitespace, indentation, and line length. Using all three provides complementary checks.

## 3. Which issues were most important, and how were they fixed?

The highest-severity finding was the use of `os.system()` to execute a command containing a server value. It was replaced with `subprocess.run()` using an argument list, validated input, and no shell invocation. The unsafe `tempfile.mktemp()` call was replaced with `NamedTemporaryFile()`. The hard-coded credential was removed, and `random.choice()` was replaced with `secrets.choice()`. Other improvements included correcting the mutable default argument, function naming, documentation, and formatting.

## 4. How did static analysis improve the program, and what are its limitations?

The initial Pylint score was 4.75/10. After corrections, it reached 10.00/10, and Flake8 reported no violations. Bandit reported no findings in the final run. These results show improvements in code quality, style, and the handling of identified security risks. However, static analysis does not prove that a program is entirely secure or correct. Findings must be reviewed in context, and testing is still necessary. The final Bandit result also includes targeted suppressions for reviewed subprocess usage.

