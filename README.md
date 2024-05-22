# Integration Test in Tutor

A Github action to test your Django Apps in Tutor (Open edX distribution).

## Example usage

``` 
name: Integration
on: [pull_request]

jobs:
  integration-test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        tutor_version: ["<17.0.0", "==17.0.3", "<18.0.0"]

    steps:
      - uses: actions/checkout@v4
        with:
          path: eox-hooks

      - uses: eduNEXT/integration-test-in-tutor
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
