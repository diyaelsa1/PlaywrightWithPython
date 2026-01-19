# Playwright With Python - Twitch tv Search Functionality Test

This project demonstrates a Playwright-based automation framework built with Python, following the Page Object Model (POM) design pattern. The framework automates test scenarios related to Twitch TV, covering both UI and API testing, and is designed to be scalable, maintainable, and easy to extend.

## Framework Structure

The automation framework is organized into the following components:

### pages
Contains Python modules for each page (or tab) of the web application. Following the POM approach, all web elements and page-specific actions are encapsulated within their respective page classes.

### tests
Holds the test scripts. The tests are organized into two subfolders to clearly separate UI and API test cases.

### factory
Manages Playwright-specific setup and configuration, including browser initialization, context creation, and device configuration.

### reports
Stores the generated HTML execution reports after test runs.

### screenshots
Captures and stores screenshots during test execution, typically used for debugging or failure analysis.

### testdata
Contains input files (such as Excel files) used to drive test data and support data-driven testing.

### utils
Includes reusable helper utilities such as Excel readers, common functions, and shared logic used across the framework.

### conftest.py
Defines Pytest fixtures and manages test setup and teardown logic.

### pytest.ini
Stores global Pytest configuration, including default execution options and reporting settings.

## Demo
![demo](https://github.com/user-attachments/assets/fcaf4dc5-3fc4-41a1-b933-266d70dd4f81)






