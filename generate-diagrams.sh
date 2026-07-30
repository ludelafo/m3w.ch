#!/usr/bin/env bash
set -euo pipefail

## Variables
WORKDIR=$(pwd)
PLANTUML_DOCKER_IMAGE="plantuml/plantuml:1.2026.2"

## Script
# Check if PlantUML is available locally
if [ -f "/opt/plantuml.jar" ]; then
    echo "PlantUML installed locally, using it..."
    PLANTUML_CMD=(java -jar /opt/plantuml.jar)
elif command -v docker &>/dev/null; then
    echo "PlantUML not installed, using its Docker image..."
    PLANTUML_CMD=(
        docker run --rm
        --volume="${WORKDIR}:/data"
        --user "$(id -u):$(id -g)"
        --env _JAVA_OPTIONS="-Duser.home=/tmp"
        "$PLANTUML_DOCKER_IMAGE"
    )
else
    echo "Error: neither PlantUML nor Docker is available." >&2
    exit 1
fi

# Enable for recursive globbing
shopt -s globstar nullglob

# Convert diagrams (enable multipart output if applicable)
PLANTUML_ARGS=(
    -tsvg
    -nbthread auto
    --progress
)

echo "Converting diagrams to SVG files..."
"${PLANTUML_CMD[@]}" -DMULTI_PART=1 "${PLANTUML_ARGS[@]}" "**/*.puml"

multipart_svg_files=(**/*_001.svg)
multipart_files=()

if [ ${#multipart_svg_files[@]} -ne 0 ]; then
    echo "Renaming multipart SVG files..."
    for multipart_svg_file in "${multipart_svg_files[@]}"; do
        base_name="${multipart_svg_file%_001.svg}"
        source_name="${base_name}.puml"

        # Add to list of multipart files
        multipart_files+=("$source_name")

        # Rename base file to -01.svg
        mv "${base_name}.svg" "${base_name}-01.svg"

        # Rename all remaining multipart files
        counter=2
        for numbered_file in "${base_name}"_*.svg; do
            new_file_name="$(printf '%s-%02d.svg' "$base_name" "$counter")"

            mv "$numbered_file" "$new_file_name"

            counter=$((counter + 1))
        done
    done

    echo "Regenerating single-page SVG files for multipart diagrams..."
    "${PLANTUML_CMD[@]}" "${PLANTUML_ARGS[@]}" "${multipart_files[@]}"
fi

echo "All diagrams processed successfully!"

