name: Tetris Game with Play Button

on:
  push:
    branches:
      - main  # Run when code is pushed to the main branch
  workflow_dispatch:  # Allow manual triggering from the GitHub Actions UI

jobs:
  run-tetris:
    runs-on: ubuntu-latest

    steps:
    # Step 1: Checkout the repository
    - name: Checkout code
      uses: actions/checkout@v3

    # Step 2: Set up Python
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9  # Specify the Python version

    # Step 3: Install dependencies
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    # Step 4: Run the Tetris script
    - name: Run Tetris Game
      run: python tetris_with_play.py
