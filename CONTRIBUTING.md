# Contributing

Thank you for your interest in contributing to the E-commerce QA Automation project!

## Getting Started

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/e-commerce-qa-automation.git
   cd e-commerce-qa-automation
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Code Standards

- **Style Guide:** Follow PEP 8
- **Naming:** Use descriptive names for tests and variables
- **Comments:** Document complex logic with comments
- **Docstrings:** Add docstrings to classes and functions

### Running Linters

Before committing, run:

```bash
# Flake8
flake8 src/ tests/

# Pylint
pylint src/ tests/
```

## Writing Tests

### Test Structure
- Use `test_` prefix for test functions
- Organize tests into classes by feature
- One assertion per test (or related assertions)
- Use descriptive test names

### Example Test
```python
@pytest.mark.regression
def test_feature_description(self, driver, base_url, test_data):
    """Test that feature X works correctly"""
    # Setup
    page = LoginPage(driver, base_url).open_login()
    
    # Action
    page.login(test_data["valid"]["username"], test_data["valid"]["password"])
    
    # Assert
    assert InventoryPage(driver, base_url).is_loaded()
```

### Test Markers
- `@pytest.mark.smoke` - Critical path tests (quick)
- `@pytest.mark.regression` - Comprehensive coverage (longer)
- `@pytest.mark.parametrize` - Data-driven tests

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run with marker
pytest -m smoke

# Parallel execution
pytest -n auto

# With HTML report
pytest --html=report.html
```

## Page Object Model Guidelines

- Create separate page classes in `src/pages/`
- Inherit from `BasePage`
- Define locators as class variables
- Use descriptive method names
- Keep logic separate from assertions

Example:
```python
class LoginPage(BasePage):
    _username = (By.ID, "user-name")
    
    def login(self, username: str, password: str):
        self.type(self._username, username)
        return self
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`

Example:
```
test(login): add validation tests for empty fields

Added tests for empty username and password fields
to ensure proper form validation

Closes #123
```

## Pull Request Process

1. Update README.md with any new features
2. Add/update tests for new functionality
3. Ensure all tests pass: `pytest`
4. Run linters: `flake8 src/ tests/`
5. Create PR with clear description
6. Wait for CI/CD pipeline to pass

## Issue Reporting

Report bugs using the following format:

```
**Describe the bug**
Clear description of the issue

**Steps to reproduce**
1. Step 1
2. Step 2

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Screenshots**
If applicable, add screenshots

**Environment**
- Python version: 
- Pytest version: 
- OS: 
```

## Code Review

- Comment on specific lines
- Be constructive and respectful
- Suggest solutions, not problems
- Acknowledge good practices

## Testing Best Practices

1. **Independence** - Each test runs independently
2. **Clarity** - Test purpose is obvious
3. **Repeatability** - Tests pass consistently
4. **Speed** - Tests run efficiently
5. **Coverage** - Meaningful coverage, not high percentages

## Docker Development

```bash
# Build image
docker build -t qa-tests .

# Run tests
docker run qa-tests

# Using docker-compose
docker-compose up
```

## Questions & Support

- Create an issue for questions
- Check existing issues first
- Be specific and detailed
- Include relevant logs/screenshots

---

Thank you for contributing!
