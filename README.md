# E-commerce QA Automation

Comprehensive automated QA test suite for the [SauceDemo](https://www.saucedemo.com) e-commerce application using industry-standard testing practices and tools.

## 🛠 Tech Stack

- **Python** 3.13+
- **Selenium WebDriver** 4.24.0 - Browser automation
- **Pytest** 8.3.2 - Test framework
- **pytest-xdist** 3.6.1 - Parallel test execution
- **pytest-html** 4.1.1 - HTML reporting
- **WebDriver Manager** 4.0.2 - Automatic driver management
- **python-dotenv** 1.0.1 - Environment configuration

## 📋 Features

### Test Coverage
- ✅ **18 comprehensive login tests** - authentication, error handling, validation
- ✅ **Add to Cart tests** - product selection and cart management
- ✅ **Checkout Flow tests** - complete end-to-end order process
- ✅ **Sorting & Filtering tests** - inventory organization features
- ✅ **UI Element tests** - responsiveness, visibility, accessibility
- ✅ **Negative scenarios** - invalid inputs, empty fields, error messages

### Architecture & Best Practices
- ✅ **Page Object Model (POM)** - Clean, maintainable code structure
- ✅ **Data-driven testing** - Centralized test data in `users.json`
- ✅ **Parallel execution** - Run tests simultaneously with pytest-xdist
- ✅ **HTML Reports** - Detailed test execution reports
- ✅ **Custom configurability** - Command-line options for flexibility
- ✅ **Wait strategies** - Smart waits for element visibility and readiness

## 📁 Project Structure

```
e-commerce-qa-automation/
├── src/
│   ├── pages/                    # Page Object Model classes
│   │   ├── base_page.py         # Base page with common locators & methods
│   │   ├── login_page.py        # Login page elements & actions
│   │   ├── inventory_page.py    # Product listing page
│   │   ├── cart_page.py         # Shopping cart page
│   │   ├── checkout_info_page.py     # User info checkout step
│   │   ├── checkout_overview_page.py # Order review step
│   │   └── checkout_complete_page.py # Order confirmation
│   ├── utils/                    # Utility functions
│   │   ├── screenshots.py       # Screenshot utilities
│   │   └── wait.py              # Custom wait strategies
│   └── data/
│       └── users.json           # Test credentials & data
├── tests/
│   ├── test_login.py            # Login test suite (18 tests)
│   ├── test_add_to_cart.py      # Cart functionality tests
│   ├── test_checkout_flow.py    # End-to-end checkout tests
│   ├── test_sort_and_filter.py  # Sorting feature tests
│   └── test_ui_elements.py      # UI responsiveness & visibility
├── conftest.py                  # Pytest configuration & fixtures
├── pytest.ini                   # Pytest settings
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.13 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/e-commerce-qa-automation.git
cd e-commerce-qa-automation
```

2. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env with your configuration
```

## ▶️ Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_login.py
```

### Run Specific Test Class
```bash
pytest tests/test_login.py::TestLoginSuccess
```

### Run Specific Test
```bash
pytest tests/test_login.py::TestLoginSuccess::test_login_success
```

### Run Tests with Specific Marker
```bash
# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression
```

### Run Tests in Parallel
```bash
pytest -n auto
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with HTML Report
```bash
pytest --html=report.html
```

### Run in Headed Mode (see browser)
```bash
pytest --headed
```

### Run with Different Browser
```bash
pytest --browser firefox
```

### Run with Custom Window Size
```bash
pytest --window-size 1920,1080
```

### Run with Custom Base URL
```bash
pytest --base-url https://www.saucedemo.com
```

## 📊 Test Suites Overview

### Login Tests (`test_login.py`) - 18 Tests ✅ All Passing

#### TestLoginSuccess (4 tests)
- `test_login_success` - Standard login with valid credentials
- `test_login_success_redirects_to_inventory` - Verify correct page redirect
- `test_login_with_problem_user` - Test problem_user account functionality
- `test_login_with_performance_user` - Test performance_glitch_user account

#### TestLoginErrors (7 tests)
- `test_login_locked_user_shows_error` - Locked out user receives error
- `test_login_invalid_credentials_wrong_password` - Valid user, wrong password
- `test_login_invalid_credentials_wrong_username` - Invalid username
- `test_login_empty_username` - Missing username validation
- `test_login_empty_password` - Missing password validation
- `test_login_empty_both_fields` - Both fields empty validation
- `test_login_error_message_visible` - Error message displays correctly

#### TestLoginPageElements (4 tests)
- `test_login_page_loads` - Login page loads successfully
- `test_username_field_exists` - Username input field present & visible
- `test_password_field_exists` - Password field is type="password"
- `test_login_button_exists` - Login button visible & enabled

#### TestLoginDataValidation (3 tests)
- `test_login_with_special_characters_in_password` - Special char handling
- `test_login_with_spaces_in_credentials` - Whitespace validation
- `test_login_username_case_sensitive` - Case sensitivity check

### Add to Cart Tests (`test_add_to_cart.py`)
- Add individual products to cart
- Verify cart updates
- Multiple product additions

### Checkout Flow Tests (`test_checkout_flow.py`)
- `test_full_checkout_flow` - Complete end-to-end checkout
- `test_checkout_with_multiple_items` - Bulk order processing

### Sort & Filter Tests (`test_sort_and_filter.py`)
- `test_inventory_sorting` - Parametrized sort verification (A-Z, Z-A, Price Low-High, Price High-Low)

### UI Element Tests (`test_ui_elements.py`)
- **Product Images** - Image loading & visibility
- **Responsiveness** - Viewport testing (Desktop, Tablet, Mobile)
- **UI Visibility** - Header, product details, buttons

## 🔧 Configuration

### Environment Variables (.env)
```env
BASE_URL=https://www.saucedemo.com
BROWSER=chrome
IMPLICIT_WAIT=2
WINDOW_SIZE=1440,900
```

### Test Data (src/data/users.json)
```json
{
  "valid": { "username": "standard_user", "password": "secret_sauce" },
  "locked": { "username": "locked_out_user", "password": "secret_sauce" },
  "problem": { "username": "problem_user", "password": "secret_sauce" },
  "perf": { "username": "performance_glitch_user", "password": "secret_sauce" },
  "checkout_info": { "first": "Ema", "last": "Tester", "zip": "71000" },
  "products": ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
}
```

## 🎯 Page Object Model

All pages inherit from `BasePage` which provides:
- Element waits (element visibility, clickability)
- Common actions (type, click, find elements)
- Navigation methods (open, go back)

### Base Page Methods
```python
def is_visible(self, locator) -> bool:
    """Check if element is visible"""

def click(self, locator):
    """Click element"""

def type(self, locator, text):
    """Type text into element"""

def text_of(self, locator) -> str:
    """Get element text"""
```

## 📈 Test Execution Examples

### Example 1: Run All Login Tests with Report
```bash
pytest tests/test_login.py -v --html=report.html
```

### Example 2: Run Smoke Tests in Parallel
```bash
pytest -m smoke -n auto --headed
```

### Example 3: Run with Custom Configuration
```bash
pytest tests/test_login.py \
  --base-url https://www.saucedemo.com \
  --browser chrome \
  --window-size 1920,1080 \
  --headed \
  -v
```

## ✅ Test Result Summary

**Latest Test Run:** 18/18 tests passed ✅
- **Duration:** ~2 minutes 54 seconds
- **Test Classes:** 5 (TestLoginSuccess, TestLoginErrors, TestLoginPageElements, TestLoginDataValidation)
- **Coverage:** Login authentication, validation, UI elements, data handling
- **Success Rate:** 100%

## 📝 Test Markers

Tests are marked with `@pytest.mark` for selective execution:

- `@pytest.mark.smoke` - Quick critical path tests
- `@pytest.mark.regression` - Comprehensive test coverage
- `@pytest.mark.parametrize` - Parameterized tests with multiple inputs

## 🐛 Debugging

### View Screenshots
Screenshots are automatically captured for failed tests in `screenshots/` directory.

### Run Single Test with Debugging
```bash
pytest tests/test_login.py::TestLoginSuccess::test_login_success -v -s --pdb
```

### Keep Browser Open After Test
```bash
pytest tests/test_login.py --keep-browser-open --headed
```

## 📚 Best Practices Implemented

1. **Page Object Model** - Separates test logic from UI element locators
2. **DRY Principle** - Reusable methods in BasePage
3. **Data-Driven Testing** - External data file for test inputs
4. **Clear Naming** - Descriptive test names following convention
5. **Error Handling** - Proper exception catching and reporting
6. **Wait Strategies** - Explicit waits for dynamic content
7. **Test Independence** - Each test is independent and reusable
8. **Documentation** - Docstrings for all test methods
9. **Test Organization** - Tests grouped into logical classes
10. **Negative Testing** - Invalid inputs, error scenarios covered

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/test-feature`
2. Add tests following existing patterns
3. Run tests: `pytest`
4. Commit: `git commit -m 'Add test for X'`
5. Push & create Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

E-commerce QA Automation Test Suite

## 🔗 Resources

- [SauceDemo](https://www.saucedemo.com) - Test application
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://selenium.dev/documentation/test_practices/encouraged/page_object_models/)

## 📞 Support

For issues, questions, or contributions, please create an issue in the repository.

---

**Last Updated:** February 19, 2026
**Test Suite Version:** 1.0.0
