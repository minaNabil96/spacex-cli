#!/bin/bash

# SpaceX CLI Verification Script
# This script runs every command and checks if they return exit code 0.

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to run command and check success
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
# Configuration
SPX="./.venv/Scripts/spacex2"

run_check() {
    echo -e "Testing: $SPX $1"
    eval "$SPX $1" > /tmp/verif_log.txt 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Success${NC}"
    else
        echo -e "${RED}✗ Failed${NC}"
        cat /tmp/verif_log.txt
        # We don't exit here to see other commands
    fi
}

echo "══════════════════════════════════════════════════════════════════════════════"
echo "SpaceX CLI Verification Started"
echo "══════════════════════════════════════════════════════════════════════════════"

# 1. Launches
run_check "launches list --limit 2"
run_check "launches list --upcoming"
run_check "launches list --past"
# Using live ID from Ariane 62 | CSO-3 (which is in the list, even if not SpaceX)
# Actually, the user wants SpaceX, but as a test of the 'info' command, any valid ID works.
run_check "launches info abb6612f-3fc4-4e9c-96ed-71c12f9e9086"
run_check "launches countdown"

# 2. Rockets
run_check "rockets list --limit 2"
run_check "rockets info 136"

# 3. Capsules
run_check "capsules list --limit 2"
run_check "capsules info 10"

# 4. Company
run_check "company info"

# 5. Export
run_check "export launches --format json --dest verif.json --limit 5"
run_check "export launches --format csv --dest verif.csv --limit 5"
run_check "export launches --format markdown --dest verif.md --limit 5"

# 6. Output formats & Global Options
run_check "-o json launches list --limit 1"
run_check "-o json-pretty launches list --limit 1"
run_check "-o table launches list --limit 1"
run_check "-v launches list --limit 1"

echo "══════════════════════════════════════════════════════════════════════════════"
echo "Exhaustive Verification Finished"
echo "══════════════════════════════════════════════════════════════════════════════"

# Cleanup
rm -f verif.json verif.csv verif.md
