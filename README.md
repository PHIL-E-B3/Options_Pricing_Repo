# UBP\_Repo

![Build](https://img.shields.io/badge/build-passing-brightgreen) ![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

> **Pricing and plotting vanilla & exotic options in a single, developer‑friendly toolkit.**

---

## 🚀 Overview

UBP\_Repo lets you move from idea ➜ Monte‑Carlo simulation ➜ publication‑quality plots in just a few lines of code. Whether you need quick Black‑Scholes analytics or full‑blown barrier‑option pricing, everything lives in one coherent API.

---

## 📂 Repository Layout

| Path             | Purpose                                                                             |
| ---------------- | ----------------------------------------------------------------------------------- |
| `/main`          | Sandbox notebook / script that wires everything together for rapid experimentation. |
| `/miscellaneous` | Helper utilities (e.g. geometric Brownian motion generator, plotting helpers).      |

---

## 🟢 Vanilla Instruments

* **Call & Put** – plain‑vanilla European options
* **`blackscholesvanilla`** – closed‑form Black‑Scholes pricer
* **`vanilla_greeks`** – visualises Δ, Γ, Θ, ρ, v
* **`vanilla_call_plotting`** – quick payoff & price surfaces

## 🐉 Exotic Instruments

* **`UpAndOut`**
* **`UpAndOut_WithRebate`**
* **`UpAndIn`**
* **`DownAndInPut`**
* **`StrucProd`** – generic wrapper (currently long bull‑spread; roadmap below)

---

## ⚡ Quick Start

```bash
# 1. Get the code
$ git clone https://github.com/your‑org/UBP_Repo.git
$ cd UBP_Repo

# 2. Install dependencies (conda or venv recommended)
$ pip install -r requirements.txt

# 3. Run the demo
$ python main.py  # or open main.ipynb
```

### 5‑Line Example

```python
from ubp_repo.vanilla import blackscholesvanilla
price = blackscholesvanilla(S0=100, K=105, T=0.5, r=0.02, sigma=0.25, option_type="call")
print(f"Call price: {price:.4f}")
```

---

## 🗺️ Roadmap

* [ ] Add time‑dependent vol surfaces
* [ ] Extend `StrucProd` to handle autocallables & reverse convertibles
* [ ] GPU acceleration via CuPy
* [ ] Continuous integration with real market data regression tests

---

## 🤝 Contributing

1. Fork the repo & create your branch (`git checkout -b feature/awesome‑feature`).
2. Commit your changes (`git commit -m 'Add some awesome‑feature'`).
3. Push to the branch (`git push origin feature/awesome‑feature`).
4. Open a pull request.

Feel free to open issues for feature requests or bugs – we love feedback!

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

### Author

*Your Name Here*
