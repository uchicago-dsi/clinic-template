#!/bin/bash
# Test: examples=data-science scaffold files are generated correctly

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../lib/helpers.sh"

TEST_NAME="Examples (data-science scaffold)"
PROJECT_NAME="Test Examples Data Science"
PROJECT_SLUG="test-examples-data-science"
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
        examples="data-science" \
        bsd="yes" \
        ann="no"

    build_docker "$PROJECT_DIR"
    test_examples_data_science "$PROJECT_DIR" "$PROJECT_SLUG" "utils"

    print_test_success "$TEST_NAME"
) || {
    print_test_failure "$TEST_NAME"
    cleanup_project "$PROJECT_DIR"
    exit 1
}

# Cleanup after success
cleanup_project "$PROJECT_DIR"
