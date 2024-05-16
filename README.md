# Integration Test in Tutor

A Github action to test your plugin in Tutor (Open edX distribution).

![](https://img.shields.io/badge/current_version-v0.0.0-blue)

## Example usage

``` 
name: Integration
on: [pull_request]

jobs:
  integration-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        tutor_version: ["<18.0.0"]
    steps:
      - uses: actions/checkout@v4
        with:
          path: eox-hooks
      - uses: eduNEXT/integration-test-in-tutor@mfmz/github-action
        with:
          tutor_version: ${{ matrix.tutor_version }}
          app_name: "eox-hooks"
          shell_file_to_run: "eox_hooks/tests/tutor/integration.sh"
```

## Inputs

### `app_name`

**Required** Application name to test. E.g., eox-tenant.

### `tutor_version`

**Required** The tutor version matrix to use.

### `shell_file_to_run`

(Optional) The path of the shell file to run the integration tests.
