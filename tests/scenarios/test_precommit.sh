#!/bin/bash
# Test: Pre-commit hooks

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/helpers.sh"

TEST_NAME="Pre-commit Hooks"
PROJECT_NAME="Test Precommit"
PROJECT_SLUG="test-precommit"
PROJECT_DIR="$TEST_DIR/$PROJECT_SLUG"

print_test_header "$TEST_NAME"

# Cleanup before test
cleanup_project "$PROJECT_DIR"
mkdir -p "$TEST_DIR"

# Run test
(
    set -e
    create_project "$PROJECT_NAME" \
        docker="yes" \
        data_dir="none" \
        cluster="no" \
        examples="no" \
        bsd="yes" \
        ann="yes"
    
    build_docker "$PROJECT_DIR"
    test_precommit "$PROJECT_DIR" "$PROJECT_SLUG"
    
    print_test_success "$TEST_NAME"
) || {
    print_test_failure "$TEST_NAME"
    cleanup_project "$PROJECT_DIR"
    exit 1
}

# Cleanup after success
cleanup_project "$PROJECT_DIR"

