#!/usr/bin/env bash
set -euo pipefail

app_name="$1"
inline_folder="$2"

source .tutor_venv/bin/activate
cp -r "${app_name}/${inline_folder}"/. plugins/

for plugin_file in plugins/*; do
  plugin_name="$(basename "$plugin_file" | cut -f1 -d '.')"
  tutor plugins enable "$plugin_name"
done
