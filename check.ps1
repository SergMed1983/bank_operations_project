# check.ps1 - script for running all checks
# Usage: .\check.ps1

$ErrorActionPreference = "Stop"

function Write-Step($message) {
    Write-Host ""
    Write-Host "===> $message" -ForegroundColor Cyan
}

Write-Step "Black: format check"
poetry run black --check src/ tests/

Write-Step "Isort: import order check"
poetry run isort --check-only src/ tests/

Write-Step "Flake8: style and syntax check"
poetry run flake8 src/ tests/

Write-Step "Mypy: type check"
poetry run mypy src/

Write-Step "Pytest: tests with coverage"
poetry run pytest --cov=src tests/

Write-Host ""
Write-Host "All checks passed!" -ForegroundColor Green
