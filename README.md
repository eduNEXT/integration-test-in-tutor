# Open edX Plugin Integration Tests with Tutor

A GitHub Action to test your Open edX plugin (Django app) in Tutor (Open edX distribution). This action automates the setup of a Tutor environment, installs your plugin, runs migrations, and executes your integration tests in an isolated environment.

## Example Usage

```yaml
name: Integration Tests
on: [pull_request]

jobs:
  integration-test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        tutor_version: ["<17.0.0", "==17.0.3", "<18.0.0", "nightly"]

    steps:
      - name: Checkout Plugin Code
        uses: actions/checkout@v4
        with:
          path: my-plugin

      - name: Run Integration Tests
        uses: your-github-username/your-action-repo@v1
        with:
          app_name: "my-plugin"
          tutor_version: ${{ matrix.tutor_version }}
          shell_file_to_run: "tests/integration.sh"
          openedx_extra_pip_requirements: "package1==1.0 package2>=2.0"
          fixtures_file: "fixtures/test_data.json"
          openedx_imports_test_file_path: "tests/import_tests.py"
          openedx_imports_test_function_name: "test_openedx_imports"
```

## Inputs

### `app_name`

**Required**  
The name of your plugin/application to test. This should match the directory name of your plugin.  
*Example*: `"my-plugin"`

### `tutor_version`

**Required**  
The version of Tutor to use. You can specify:

- A specific version number (e.g., `"==17.0.3"`).
- A comparison operator with a version (e.g., `"<18.0.0"`).
- The string `"nightly"` to use the latest development version.

**Special Note on Using `"nightly"`**:  
When you specify `"nightly"` for `tutor_version`, the action will clone the latest code from Tutor's `nightly` branch. This allows you to test your plugin against the most recent changes in Tutor, which might not yet be released in a stable version.

*Examples*:

- `"==17.0.3"`
- `"<18.0.0"`
- `"nightly"`

### `shell_file_to_run`

**Required**  
The path to the shell script that runs your integration tests. This path is relative to your plugin directory.  
*Example*: `"tests/integration.sh"`

### `openedx_extra_pip_requirements`

**Optional**  
Extra pip requirements to install in Open edX. These are additional Python packages your plugin depends on. Provide them as a space-separated string.  
*Default*: `""` (empty string)  
*Example*: `"package1==1.0 package2>=2.0"`

### `fixtures_file`

**Optional**  
The path to the fixtures file of your plugin to load initial data for the tests. This path is relative to your plugin directory.  
*Example*: `"fixtures/test_data.json"`

### `openedx_imports_test_file_path`

**Optional**  
The path to the Python file in your plugin that contains the test function for validating Open edX imports. This path is relative to your plugin directory.  
*Example*: `"tests/import_tests.py"`

### `openedx_imports_test_function_name`

**Optional**  
The name of the function in the specified file that executes the import tests for Open edX.  
*Example*: `"test_openedx_imports"`

## Description

This GitHub Action automates the process of setting up a Tutor Open edX environment to test your plugin. It performs the following steps:

1. **Checkout Plugin Code**: Checks out your plugin code into a directory specified by `app_name`.

2. **Set Tutor Environment Variables**: Sets necessary environment variables for Tutor.

3. **Install and Prepare Tutor**: Installs the specified version of Tutor and launches the Open edX platform. If `tutor_version` is set to `"nightly"`, the action clones the latest code from Tutor's `nightly` branch.

4. **Configure Caddyfile and Open edX Settings**: Configures the Caddyfile and Open edX settings using `patches.yml`.

5. **Add Mount for Plugin**: Mounts your plugin into the LMS and CMS containers.

6. **Install Plugin as an Editable Package**: Installs your plugin in editable mode inside the LMS container.

7. **Install Extra Requirements**: Installs any extra pip requirements specified in `openedx_extra_pip_requirements`.

8. **Run Migrations**: Runs database migrations for both LMS and CMS and restarts Tutor services.

9. **Import Demo Course**: Imports the Open edX demo course for testing purposes.

10. **Test Open edX Imports in Plugin** *(Optional)*: Runs a test function to validate Open edX imports in your plugin if `openedx_imports_test_file_path` and `openedx_imports_test_function_name` are provided.

11. **Load Initial Data for the Tests** *(Optional)*: Loads initial data from a fixtures file into the LMS if `fixtures_file` is provided.

12. **Check LMS Heartbeat**: Verifies that the LMS is running by hitting the heartbeat endpoint.

10. **Set `DEMO_COURSE_ID` Environment Variable**:  
    Sets the `DEMO_COURSE_ID` environment variable based on the Tutor version. This variable allows you to refer to the demo course in your tests, which can be helpful when you need to interact with course content during testing.

    **Usage in Your Tests**:  
    In your test code, you can access the `DEMO_COURSE_ID` environment variable to get the identifier of the demo course. For example:

    ```python
    import os

    DEMO_COURSE_ID = os.environ.get("DEMO_COURSE_ID")
    # Use DEMO_COURSE_ID in your tests
    ```

14. **Run Integration Tests**: Creates a virtual environment and runs your integration tests using the specified shell script.

## Notes

- **Using the `"nightly"` Version of Tutor**:  
  The `"nightly"` option allows you to test your plugin against the latest development code of Tutor. This is useful for ensuring compatibility with upcoming features or changes. Be aware that the nightly version may be less stable and could introduce breaking changes. When using `"nightly"`, the action clones the Tutor repository from the `nightly` branch and builds the Docker images locally, which may increase the execution time of the workflow.

- **Paths**: Ensure that the paths provided in the inputs are relative to your plugin directory.

- **Optional Steps**: Steps involving `openedx_imports_test_file_path`, `openedx_imports_test_function_name`, and `fixtures_file` are optional and will only run if the corresponding inputs are provided.

- **Tutor Versions**: Use the matrix strategy to test your plugin against multiple Tutor versions, including the nightly build.

- **Dependencies**: If your integration tests require additional dependencies, specify them in `openedx_extra_pip_requirements` or handle them within your `shell_file_to_run`.

- **Permissions**: Ensure your `shell_file_to_run` is executable. The action sets executable permissions before running it.
