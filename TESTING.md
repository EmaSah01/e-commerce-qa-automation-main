# Testing Guide

Complete guide to running and understanding tests in this project.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_login.py

# Run specific test
pytest tests/test_login.py::TestLoginSuccess::test_login_success
```

## Test Organization

```
tests/
├── test_login.py              (18 tests) - Authentication & login validation
├── test_add_to_cart.py        - Product selection
├── test_cart_management.py    (7 tests) - Cart operations
├── test_checkout_flow.py      - End-to-end checkout
├── test_checkout_validation.py (7 tests) - Checkout form validation
├── test_sort_and_filter.py    - Sorting functionality
├── test_product_display.py    (12 tests) - Product display & interaction
└── test_ui_elements.py        - UI responsiveness
```

## Test Coverage

### Login Tests (18 tests)
- **Success Cases:** Valid login, account variations
- **Error Cases:** Wrong credentials, empty fields, locked account
- **Validation:** Input validation, error messages
- **UI Elements:** Form fields, button states

### Cart Management (7 tests)
- Single item addition
- Multiple items
- Cart badge count
- Item details in cart
- Empty cart handling
- Navigation persistence

### Checkout Validation (7 tests)
- Form validation (required fields)
- Special characters handling
- Navigation during checkout
- Order completion

### Product Display (12 tests)
- Product listing
- Product details (name, price, image, description)
- Sorting functionality
- Interaction (add to cart button states)

## Running Tests by Category

### Run Smoke Tests (Quick)
```bash
pytest -m smoke
```

### Run Regression Tests (Full)
```bash
pytest -m regression
```

### Run Specific Class
```bash
pytest tests/test_login.py::TestLoginSuccess
```

### Run in Parallel
```bash
# Auto-detect optimal number of workers
pytest -n auto

# Specify number of workers
pytest -n 4
```

## Advanced Options

### With HTML Report
```bash
pytest --html=report.html --self-contained-html
```

### With Verbose Output
```bash
pytest -v -s  # -s shows print statements
```

### With Debugging
```bash
pytest --pdb  # Drop into debugger on failure
```

### With Coverage
```bash
pytest --cov=src --cov-report=html
```

### Headed Mode (See Browser)
```bash
pytest --headed
```

### Keep Browser Open
```bash
pytest --keep-browser-open
```

### Custom Configuration
```bash
pytest --base-url https://staging.saucedemo.com \
       --browser firefox \
       --window-size 1920,1080 \
       --implicit-wait 3
```

## Environment Configuration

### Using .env file
```env
BASE_URL=https://www.saucedemo.com
BROWSER=chrome
IMPLICIT_WAIT=2
WINDOW_SIZE=1440,900
```

### Command-line Override
```bash
pytest --base-url https://custom.com --browser firefox
```

## Test Execution Examples

### Example 1: Quick Smoke Test
```bash
pytest -m smoke -v --html=report.html
```

### Example 2: Full Test Suite with Parallel Execution
```bash
pytest tests/ -n auto -v --html=report.html
```

### Example 3: Specific Features with Browser View
```bash
pytest tests/test_login.py tests/test_cart_management.py \
  --headed \
  -v \
  --html=report.html
```

### Example 4: Debug Failed Test
```bash
pytest tests/test_login.py::TestLoginErrors::test_login_empty_username \
  --headed \
  -vv \
  --pdb
```

## Understanding Test Results

### PASSED ✅
Test completed successfully

### FAILED ❌
Test did not pass - check error message and stack trace

### SKIPPED ⊘
Test was skipped (conditional or marked)

### ERROR ⚠️
Test encountered an error before running

## Debugging Failed Tests

### Check Error Message
```bash
pytest tests/test_file.py -v  # Look at the failure message
```

### Run in Headed Mode
```bash
pytest tests/test_file.py --headed -v
```

### Add Debug Output
```python
def test_example(driver):
    print("About to login")  # Will print with -s flag
    result = login()
    print(f"Login result: {result}")
```

Run with:
```bash
pytest -v -s tests/test_file.py
```

### Use Debugger
```bash
pytest tests/test_file.py --pdb
```

Then use standard Python debugger commands:
- `n` - Next line
- `s` - Step into
- `c` - Continue
- `p variable` - Print variable
- `l` - List code

### Check Screenshots
Failed tests may have screenshots in `screenshots/` directory

## CI/CD Integration

### GitHub Actions
Tests run automatically on:
- Push to `main` or `develop`
- Pull requests
- Scheduled daily runs

Check workflows in `.github/workflows/`

### Running Locally Like CI/CD
```bash
# Install requirements same as CI
pip install -r requirements.txt

# Run tests the same way
pytest tests/ -v --html=report.html

# Lint checks
flake8 src/ tests/
pylint src/ tests/
```

## Docker Execution

### Build and Run
```bash
docker build -t qa-tests .
docker run qa-tests
```

### Using Docker Compose
```bash
docker-compose up
```

### Mount Volumes for Live Reports
```bash
docker run -v $(pwd)/reports:/app/reports qa-tests
```

## Performance & Optimization

### Run in Parallel
```bash
pytest -n auto  # Much faster!
```

### Skip UI Tests, Run Only Logic
```bash
pytest -m "not ui"  # Custom marker needed
```

### Run Only Fast Tests
```bash
pytest -m smoke
```

### Limit Test Duration
```bash
pytest --timeout=60  # Requires pytest-timeout
```

## Generating Reports

### HTML Report
```bash
pytest --html=report.html --self-contained-html
```

### Allure Report
```bash
pytest --allure-dir=allure_results
allure serve allure_results
```

### JUnit XML (for CI/CD integration)
```bash
pytest --junit-xml=report.xml
```

## Fixtures

Available fixtures in `conftest.py`:

- `driver` - Selenium WebDriver instance
- `base_url` - Application URL
- `test_data` - Test data from users.json
- `browser_name` - Browser type (chrome, firefox)

### Using Fixtures
```python
def test_example(driver, base_url, test_data):
    login_page = LoginPage(driver, base_url)
    username = test_data["valid"]["username"]
```

## Test Data

Located in `src/data/users.json`:

### Predefined Users
- `valid` - Standard test user
- `locked` - Locked out user
- `problem` - Problem user
- `perf` - Performance glitch user

### Using Test Data
```python
def test_with_data(driver, base_url, test_data):
    username = test_data["valid"]["username"]
    products = test_data["products"]
    checkout_info = test_data["checkout_info"]
```

## Best Practices

✅ **Do:**
- Run tests frequently
- Keep tests independent
- Use descriptive names
- Test one thing per test
- Use parametrize for data-driven tests
- Run full suite before committing

❌ **Don't:**
- Test implementation details
- Rely on test execution order
- Use hard sleeps (use waits)
- Have tests dependent on each other
- Test third-party libraries
- Commit with failing tests

## Troubleshooting

### Timeout Issues
Increase implicit wait:
```bash
pytest --implicit-wait=5
```

### Stale Element Reference
Already handled in page objects, but if you see it:
- Refetch elements
- Use wait strategies
- Avoid caching elements

### Tests Pass Locally, Fail in CI/CD
- Ensure same Python version
- Check environment variables
- Verify network access
- Try running in Docker locally

### Browser Issues
Clear browser cache:
```bash
pytest --headed  # Manual cache clear
```

Or use private/incognito mode in tests (if needed)

## Support & Resources

- **Documentation:** README.md
- **Contributing:** CONTRIBUTING.md
- **Issues:** GitHub Issues
- **Test Data:** src/data/users.json
- **Page Objects:** src/pages/
- **Utilities:** src/utils/

---

For more information, see [README.md](README.md)
