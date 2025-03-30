#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Activating virtual environment..."
source venv/bin/activate

echo "Setting PYTHONPATH..."
export PYTHONPATH=$(pwd)/src

echo "Running tests..."
pytest tests/

echo "All tests passed!"