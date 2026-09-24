name: Substack Sunday Production Pipeline

on:
  schedule:
    # Runs every Sunday at 9:00 AM EDT (13:00 UTC)
    - cron: '0 13 * * 0'
  workflow_dispatch:
    inputs:
      character:
        description: 'Select Character (or Auto Rotate)'
        required: true
        default: 'auto'
        type: choice
        options:
          - 'auto'
          - 'mom'
          - 'dad'
          - 'son'
          - 'red_twin'
          - 'blue_twin'

jobs:
  sunday-production:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          ref: main
          fetch-depth: 0
          persist-credentials: true

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Python Dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          else
            pip install requests google-api-python-client google-auth-httplib2 google-auth-oauthlib
          fi

      - name: Ensure Directories Exist
        run: |
          mkdir -p output/substack stills/portraits config scripts

      - name: Execute Sunday Content Generator
        run: |
          CHARACTER_ARG="${{ github.event.inputs.character || 'auto' }}"
          echo "=== Running Sunday Bundle Generator for: $CHARACTER_ARG ==="
          if [ -f "scripts/generate_pasture_content.py" ]; then
            python scripts/generate_pasture_content.py --character "$CHARACTER_ARG"
          elif [ -f "generate_pasture_content.py" ]; then
            python generate_pasture_content.py --character "$CHARACTER_ARG"
          else
            echo "[!] Error: generate_pasture_content.py not found."
            exit 1
          fi

      - name: Inspect Output Bundle
        run: |
          echo "=== Generated Files in output/substack/ ==="
          ls -la output/substack/

      - name: Upload Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: sunday-pasture-bundle-${{ github.run_number }}
          path: output/substack/
          if-no-files-found: warn

      - name: Commit and Push Output to Repository
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          git pull origin main --rebase || true
          git add -f output/substack/
          
          if git diff --staged --quiet; then
            echo "[*] No new changes to commit."
          else
            git commit -m "Auto-generate Sunday Pasture bundle [$(date +'%Y-%m-%d')]"
            git push origin HEAD:main
          fi

      - name: Sync Output to Google Drive (Optional)
        if: env.GDRIVE_CREDENTIALS != ''
        env:
          GDRIVE_CREDENTIALS: ${{ secrets.GDRIVE_CREDENTIALS }}
          GDRIVE_FOLDER_ID: ${{ secrets.GDRIVE_FOLDER_ID }}
        run: |
          echo "$GDRIVE_CREDENTIALS" > gdrive_credentials.json
          if [ -f "scripts/sync_to_gdrive.py" ]; then
            python scripts/sync_to_gdrive.py
          fi
          rm -f gdrive_credentials.json
