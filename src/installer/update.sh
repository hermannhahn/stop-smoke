#!/bin/bash

project_version=$(grep -oP 'Project-Id-Version:\s*\K[0-9.]+' ../locales/en/LC_MESSAGES/stop-smoke.po)
project_version=$(echo "$project_version" | tr -d '\0')
sed -i "s/\(#define MyAppVersion \)\"[^\"]*\"/\1\"$project_version\"/" stop-smoke.iss

ISCC.exe stop-smoke.iss
