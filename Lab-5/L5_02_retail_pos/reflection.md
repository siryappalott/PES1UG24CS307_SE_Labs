# Lab 5: Reflection

*(The handout did not print the questions; these are the standard four for this lab.)*

**1. Which issues were easiest and hardest to fix?**
Easiest were the mechanical ones: unused imports, blank lines (E302/E305), docstrings and renaming `printSales`. Hardest was the `eval()` finding (Bandit B307), because deleting `eval` is easy but keeping promo codes like `total * 0.9` working needed a small safe expression evaluator built on `ast`. The bare `except` was also tricky: removing it exposed real bad inputs, so I had to decide what to do with them (reject the bill vs. skip the item).

**2. Did the tools report any false positives?**
Mostly no. Bandit B311 (`random`) is arguably a false positive here, since a receipt number is not a security token, but switching to `secrets` costs nothing. Pylint's "too general exception" and Bandit's try/except/pass were genuine. The tools also **missed** real bugs: negative quantities, a string quantity, a negative tax rate and unknown items. I only found those by running the program and reading the output, so static analysis complements testing rather than replacing it.

**3. How would you integrate these tools into a real workflow?**
Run Flake8 and Pylint as a pre-commit hook and in CI on every pull request, fail the build on Bandit medium/high findings and on a Pylint score below a threshold (e.g. 9.5), and keep a short `.pylintrc` / `# nosec` policy with a written reason for every suppression.

**4. What improvements did you see after the fixes?**
Pylint went from 5.65 to 10.00, Bandit from 3 findings to 0 and Flake8 from 12 to 0. More importantly the program is safer (no code injection through the promo prompt) and more correct (no negative bills, no silent zero bills, no shared default list, no leaked file handle). It is also easier to read and test now that `main()` only runs when the script is executed directly.
