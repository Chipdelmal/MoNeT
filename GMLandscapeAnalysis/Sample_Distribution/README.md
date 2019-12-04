# Sampling Population from Distributions
*Sample from truncated exponential/gamma distribution and write to csv files.*

First-time users:
1. Open terminal.
2. Activate your MoNeT virtual environment.
3. Open R interpreter.
4. Install R packages `truncdist` and `pracma` .
```
install.packages("truncdist")
install.packages("pracma")
```

You should now be able to run code from `sample_dist.py` or  `sample_dist_coordinates.py` as expected.

Steps:

Open `sample_dist.py` or `sample_dist_coordinates.py`.

Edit parameters and file path as necessary (in particular, set `EXP` to `True` for the truncated exponential and `False` for the truncated gamma).

Run code body of file.

Run `main()` at bottom of file.
