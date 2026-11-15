# SARIMAX fit: detailed walkthrough

```python
order = (4, 1, 0)
seasonal_order = (1, 1, 0, 24)

model = SARIMAX(endog=train, order=order, seasonal_order=seasonal_order)
results = model.fit()

print(results.summary())
```

## 1. Model specification

The model is written as $\text{SARIMA}(p,d,q)\times(P,D,Q)_s$, here $(4,1,0)\times(1,1,0)_{24}$.

| Part | Value | Meaning |
|---|---|---|
| `p = 4` | AR order | The current value depends on the last 4 hours. |
| `d = 1` | Differencing | Takes the first difference $y_t - y_{t-1}$ to remove the trend. |
| `q = 0` | MA order | No moving-average terms. |
| `P = 1` | Seasonal AR | The current value depends on the value 24 hours ago. |
| `D = 1` | Seasonal differencing | Takes $y_t - y_{t-24}$ to remove the daily pattern. |
| `Q = 0` | Seasonal MA | None. |
| `s = 24` | Period | Hourly data with a daily cycle, so 24 steps per season. |

The model equation is:

$$
\phi_4(L)\,\tilde\phi_1(L^{24})\,\Delta\,\Delta_{24}\,y_t = \zeta_t
$$

- $L$ is the lag operator.
- $\Delta$ is the first difference and $\Delta_{24}$ is the seasonal difference.
- $\zeta_t$ is white noise.

With `q = 0` and `Q = 0` there are no MA terms (`k_ma_params = 0`).

## 2. Constructing `SARIMAX(...)`

`__init__` does the following:

1. **Builds a `SARIMAXSpecification`**, which validates `endog`, `order` and `seasonal_order`.
2. **Stores the orders** and `seasonal_periods = 24`.
3. **Counts the parameters:** `k_ar_params = 4`, `k_seasonal_ar_params = 1`, plus the variance `sigma2`. That gives `k_params = 6`.
4. **Calculates the state size.** Differencing is placed inside the state vector, because `simple_differencing=False` by default:
   - `_k_order = max(k_ar + k_seasonal_ar, k_ma + k_seasonal_ma + 1)`. The AR polynomials multiply to a reduced degree of $4 + 24 = 28$, so `_k_order = 28`.
   - `k_states = 28 + 24*1 + 1 = 53`.

   Large state dimensions like this are the main reason fitting is slow.
5. **Calls `MLEModel.__init__`** and fills in the state-space matrices (`design`, `transition`, `selection`).
6. **Calls `initialize_default()`.** Differenced states get a diffuse initialization and the ARMA part a stationary one. The `loglikelihood_burn` is set so that diffuse states are excluded from the likelihood.

## 3. `model.fit()`

`fit()` runs maximum likelihood estimation using the Kalman filter. Defaults:

- `method='lbfgs'`: limited-memory BFGS optimizer from SciPy.
- `maxiter=50`: at most 50 iterations.
- `disp=5`: prints convergence messages.
- `cov_type='opg'`: standard errors from the outer product of gradients.

Steps:

1. **Start parameters.** `start_params` is computed with conditional sum of squares: the data is differenced, then OLS is used to get initial AR coefficients. If these are non-stationary, they are replaced by zeros with a warning.
2. **Untransform.** Parameters are mapped to an unconstrained space. The AR parameters are constrained to be stationary and the variance to be positive, so the optimizer works freely.
3. **Optimization.** `super().fit(...)` maximizes the log-likelihood. Each evaluation calls `update()`, which writes the parameters into the matrices, then runs the Kalman filter. Because `lbfgs` is used without `optim_score`, the gradient is approximated numerically (`approx_grad=True`, `epsilon=1e-5`).
4. **Smoothing and results.** `self.smooth(...)` is called with the best parameters. It returns a `SARIMAXResults` object with `mlefit`, `mle_retvals` and `mle_settings` attached.

## 4. `print(results.summary())`

`summary()` returns a table with:

- **Model info:** observation count, log-likelihood, AIC, BIC, HQIC.
- **Coefficients:** `ar.L1` to `ar.L4`, `ar.S.L24` and `sigma2`, each with standard error, z-value, p-value and confidence interval.
- **Diagnostics:** Ljung-Box (residual autocorrelation), Jarque-Bera (normality) and heteroskedasticity tests.

## Gotchas

- **Slow fitting.** With a period of 24 the state space is large. `maxiter=50` may stop before convergence, so look for a `ConvergenceWarning`. If it appears, try `model.fit(maxiter=200)`.
- **Differencing losses.** The first $d + sD = 25$ observations are used to initialize the differencing states and do not contribute to the likelihood.
- **`train` index.** A DatetimeIndex with a set frequency avoids warnings. Set it with `train.index.freq = "h"` if needed.
- **No MA terms.** The `q=0, Q=0` choice should come from ACF/PACF analysis or a grid search, not guesswork.
- **`print` is optional** in a notebook, but it gives a plain-text rendering rather than the rich output of a bare `results.summary()`.

## Optional improvements

```python
results = model.fit(maxiter=200, disp=False)  # more iterations, quiet output
print(results.summary())
```
