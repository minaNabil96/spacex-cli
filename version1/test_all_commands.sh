#!/usr/bin/env bash
# SpaceX CLI — Full README Command Test Script
# Run from: version1/ directory
set -e

PASS=0
FAIL=0
RESULTS=""

test_cmd() {
    local desc="$1"
    shift
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "TEST: $desc"
    echo "CMD:  $*"
    echo "───────────────────────────────────────────────────────────────"
    if eval "$@" 2>&1; then
        echo "✅ PASS"
        PASS=$((PASS + 1))
        RESULTS="${RESULTS}\n✅ PASS: $desc"
    else
        local ec=$?
        echo "❌ FAIL (exit code $ec)"
        FAIL=$((FAIL + 1))
        RESULTS="${RESULTS}\n❌ FAIL: $desc (exit $ec)"
    fi
}

test_exit_code() {
    local desc="$1"
    local expected="$2"
    shift 2
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "TEST: $desc (expect exit $expected)"
    echo "CMD:  $*"
    echo "───────────────────────────────────────────────────────────────"
    set +e
    eval "$@" 2>&1
    local actual=$?
    set -e
    if [ "$actual" -eq "$expected" ]; then
        echo "✅ PASS (exit code $actual as expected)"
        PASS=$((PASS + 1))
        RESULTS="${RESULTS}\n✅ PASS: $desc"
    else
        echo "❌ FAIL (expected exit $expected, got $actual)"
        FAIL=$((FAIL + 1))
        RESULTS="${RESULTS}\n❌ FAIL: $desc (expected $expected, got $actual)"
    fi
}

echo "🚀 SpaceX CLI — Testing All README Commands"
echo "============================================="

# 1. Help
test_cmd "spacex --help" "spacex --help"

# 2. Launches list (default)
test_cmd "spacex launches list" "spacex launches list"

# 3. Launches list --upcoming --limit 5
test_cmd "spacex launches list --upcoming --limit 5" "spacex launches list --upcoming --limit 5"

# 4. JSON output: launches list --past
test_cmd "spacex -o json launches list --past" "spacex -o json launches list --past"

# 5. Launch info by ID
test_cmd "spacex launches info <id>" "spacex launches info 5eb87cd9ffd86e000604b32a"

# 6. Launches countdown (skip — interactive, would block)
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "⏭️ SKIP: spacex launches countdown (interactive — would block)"
echo "═══════════════════════════════════════════════════════════════"
RESULTS="${RESULTS}\n⏭️ SKIP: spacex launches countdown (interactive)"

# 7. Rockets list
test_cmd "spacex rockets list" "spacex rockets list"

# 8. Rockets list JSON-pretty
test_cmd "spacex -o json-pretty rockets list" "spacex -o json-pretty rockets list"

# 9. Rocket info by ID
test_cmd "spacex rockets info <id>" "spacex rockets info 5e9d0d95eda69973a809d1ec"

# 10. Capsules list --limit 5
test_cmd "spacex capsules list --limit 5" "spacex capsules list --limit 5"

# 11. Capsule info by ID
test_cmd "spacex capsules info <id>" "spacex capsules info 5e9e2c5bf35918ed873b2664"

# 12. Company info (table)
test_cmd "spacex company info" "spacex company info"

# 13. Company info (JSON)
test_cmd "spacex -o json company info" "spacex -o json company info"

# 14. Export JSON
test_cmd "spacex export launches --dest ./out.json --format json --limit 20" \
    "spacex export launches --dest ./out.json --format json --limit 20"

# 15. Export CSV
test_cmd "spacex export launches --dest ./out.csv --format csv" \
    "spacex export launches --dest ./out.csv --format csv"

# 16. Export Markdown
test_cmd "spacex export launches --dest ./out.md --format markdown" \
    "spacex export launches --dest ./out.md --format markdown"

# 17. Verbose flag
test_cmd "spacex --verbose launches list" "spacex --verbose launches list --limit 2"

# 18. Error handling — bad launch ID should exit 1
test_exit_code "Error: bad launch ID → exit 1" 1 "spacex launches info nonexistent-bad-id"

# 19. Verify exported files exist
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST: Verify exported files exist and have content"
echo "───────────────────────────────────────────────────────────────"
ALL_EXIST=true
for f in out.json out.csv out.md; do
    if [ -s "./$f" ]; then
        echo "  ✅ $f exists ($(wc -c < ./$f) bytes)"
    else
        echo "  ❌ $f missing or empty"
        ALL_EXIST=false
    fi
done
if $ALL_EXIST; then
    echo "✅ PASS"
    PASS=$((PASS + 1))
    RESULTS="${RESULTS}\n✅ PASS: Exported files exist and have content"
else
    echo "❌ FAIL"
    FAIL=$((FAIL + 1))
    RESULTS="${RESULTS}\n❌ FAIL: Some exported files missing"
fi

# 20. Run pytest
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "TEST: pytest (all tests pass)"
echo "───────────────────────────────────────────────────────────────"
if pytest 2>&1; then
    echo "✅ PASS"
    PASS=$((PASS + 1))
    RESULTS="${RESULTS}\n✅ PASS: pytest all tests pass"
else
    echo "❌ FAIL"
    FAIL=$((FAIL + 1))
    RESULTS="${RESULTS}\n❌ FAIL: pytest had failures"
fi

# Cleanup exported files
rm -f ./out.json ./out.csv ./out.md

# Summary
echo ""
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           SPACEX CLI — TEST RESULTS SUMMARY                 ║"
echo "╠═══════════════════════════════════════════════════════════════╣"
echo -e "$RESULTS"
echo ""
echo "───────────────────────────────────────────────────────────────"
echo "  Total: $((PASS + FAIL)) tested, $PASS passed, $FAIL failed, 1 skipped (countdown)"
echo "╚═══════════════════════════════════════════════════════════════╝"
