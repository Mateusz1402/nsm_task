#!/bin/bash

# Detect Docker/Podman
if command -v docker >/dev/null 2>&1; then
    RUNTIME="docker"
elif command -v podman >/dev/null 2>&1; then
    RUNTIME="podman"
else
    echo "Error: no docker and no podman"
    exit 1
fi

#Args
INPUT_DIR=""
OUTPUT_FILE=""
OTHER_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -input_dir)
            INPUT_DIR="$2"
            shift 2
            ;;
        -output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        *)
            OTHER_ARGS+=("$1")
            shift
            ;;
    esac
done

if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: $0 -input_dir <path>  -output <file> [other_args]"
    exit 1
fi

ABS_INPUT_DIR=$(readlink -f "$INPUT_DIR")

$RUNTIME run --rm \
    -v "$ABS_INPUT_DIR":/data:ro \
    -v "$(pwd)":/output \
    nms-manifest-tool \
    -input_dir /data \
    -output "/output/manifest.txt" \
    "${OTHER_ARGS[@]}"