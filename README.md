# E-commerce QA Automation

Automated QA tests for the [SauceDemo](https://www.saucedemo.com) application using:

- **Python 3.13**
- **Selenium WebDriver**
- **Pytest**
- **Page Object Model (POM)**
- **pytest-xdist** (parallel execution)
- **pytest-html** (reporting)

## 🛠 Features
- Login tests (valid, locked user, error validation)
- Add to Cart & Remove from Cart
- Full Checkout Flow (end-to-end)
- Sorting & Filtering of inventory
- Negative scenarios (empty checkout fields, invalid credentials)
- Page Object Model for clean maintainable code
- Data-driven testing via `users.json`
- Parallel test execution

## ▶️ How to Run
Clone the repo:
```bash
git clone https://github.com/TVOJ-USERNAME/e-commerce-qa-automation.git
cd e-commerce-qa-automation
