#!/bin/bash

# Ensure the script is run with an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Take from arguments, but remove the trailing slash if present
EXER_DIR="${1%/}"

declare -i counter=0
declare -i expected_count=21

# Helper function to check permissions
check_permissions() {
    local path=$1
    local expected_perms=$2

    if [[ -e "$path" ]]; then
        # Get actual permissions in a format comparable to expected (e.g., -rw-rw-r--)
        actual_perms=$(stat -c "%A" "$path")

        if [[ "$actual_perms" == "$expected_perms" ]]; then
            printf "[OK] %s has correct permissions (%s)\n" "$path" "$actual_perms"
            counter=$((counter + 1))
        else
            printf "[ERROR] %s has incorrect permissions (expected %s, got %s)\n" "$path" "$expected_perms" "$actual_perms"
        fi
    else
        printf "[ERROR] %s does not exist\n" "$path"
    fi
}

# Directory structure and expected permissions
check_permissions "$EXER_DIR" "drwxrwxr-x"
check_permissions "$EXER_DIR/multifile" "drwxrwxr-x"

for i in {01..10}; do
    check_permissions "$EXER_DIR/multifile/file_$i" "-rw-rw-r--"
done

check_permissions "$EXER_DIR/very" "drwx---r-x"
check_permissions "$EXER_DIR/very/nested" "drwx---r-x"
check_permissions "$EXER_DIR/very/nested/a" "drwx---r-x"
check_permissions "$EXER_DIR/very/nested/a/b" "drwx---r-x"
check_permissions "$EXER_DIR/very/nested/a/b/c" "drwx---r-x"
check_permissions "$EXER_DIR/very/nested/a/b/c/d" "drwx---r-x"
check_permissions "$EXER_DIR/very/nested/a/b/c/d/myprog" "-rwxrwxr--"
check_permissions "$EXER_DIR/very/nested/a/.iamhidden" "-rw-rw-r--"
check_permissions "$EXER_DIR/very/nested/a/.metoo" "-rw-rw-r--"

# Print summary
echo "Summary:"
echo "  $counter/$expected_count correct"
