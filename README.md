# Open edX Plugin Integration Tests with Tutor

A GitHub Action to test your Open edX plugin (Django app) within Tutor (Open edX distribution). This action automates the setup of a Tutor environment, installs your plugin, runs migrations, and executes your integration tests in an isolated environment.

## Example Usage

```yaml
name: Integration Tests
on: [pull_request]

jobs:
  integration-test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        tutor_version: ["<18.0.0", "==18.0.3", "<19.0.0", "nightly"]

    steps:
      - name: Run Integration Tests
        uses: eduNEXT/integration-test-in-tutor@main
        with:
          app_name: "eox-test"
          tutor_version: ${{ matrix.tutor_version }}
          tutor_plugins: "plugin1 plugin2"
          shell_file_to_run: "tests/integration.sh"
          openedx_extra_pip_requirements: "package1==1.0 package2>=2.0"
          fixtures_file: "fixtures/test_data.json"
          openedx_imports_test_file_path: "eox_test/edxapp_wrapper/test_backends.py"
```

## Inputs

### `app_name`

**Required**  
The name of your plugin/application to test. This should match the directory name of your plugin.  
* *Example*: `"eox-tenant"`

### `tutor_version`

**Required**  
The version of Tutor where you want to run the integration tests. You can specify:

* A specific version number (e.g., `"==18.0.3"`).
* A comparison operator with a version (e.g., `"<18.0.0"`).
* The string `"nightly"` to use the latest development version.

> [!IMPORTANT]
> This action is officially supported and tested with Tutor versions corresponding to the current and immediate previous Open edX releases, as well as the nightly build. Using other Tutor versions is not guaranteed to be supported.

### `python_version`

**Optional**  
The python version to run the integration tests with. Make sure to use a version fully supported by the plugin.

### `tutor_plugins`

**Optional**  
The list of Tutor Index plugins to install. Refer to the [official Tutor documentation](https://docs.tutor.edly.io/reference/cli/plugins.html#tutor-plugins-install). Only plugins available in the official Tutor plugin index can be installed using this option. Provide them as a space-separated string.
* *Example*: `"plugin1 plugin2"`

### `shell_file_to_run`

**Optional**  
The path to the shell script that runs your integration tests. This path is relative to your plugin directory. 
* *Default*: `"scripts/execute_integration_tests.sh"`
* *Example*: `"tests/integration.sh"`

### `openedx_extra_pip_requirements`

**Optional**  
Extra pip requirements to install in Open edX. These are additional Python packages your plugin depends on. Provide them as a space-separated string.  
* *Example*: `"package1==1.0 package2>=2.0"`

### `fixtures_file`

**Optional**  
The path to the fixtures file of your plugin to load initial data for the tests. This path is relative to your plugin directory.  
* *Example*: `"fixtures/test_data.json"`

### `openedx_imports_test_file_path`

**Optional**  
The path to the Python file in your plugin that contains the test function for validating Open edX imports. This path is relative to your plugin directory.  
* *Example*: `"eox_test/edxapp_wrapper/test_backends.py"`

## Overview

This GitHub Action automates the process of setting up a Tutor Open edX environment to test your plugin. It performs the following steps:

1. **Set up Python version**: Configures the Python version to ensure that tests are executed in an environment fully supported by our plugins.

2. **Checkout Plugin Code**: Checks out your plugin code into a directory specified by `app_name`.

3. **Adjust Permissions**: Modifies file permissions to ensure that all files and directories are accessible, preventing permission-related errors during Tutor operations.

4. **Set Tutor Environment Variables**: Sets necessary environment variables for Tutor.

5. **Create Virtual Environments**: Creates isolated Python virtual environments for installing Tutor and for running the integration tests.

6. **Install and Prepare Tutor**: Installs the specified version of Tutor.
   
   - If `tutor_version` is set to `"nightly"`, clones the Tutor repository from the `nightly` branch.
   - Saves Tutor configuration.

7. **Install and Enable Tutor Plugins**: Installs and enables the specified Tutor plugins
specified in `tutor_plugins`.

8. **Configure Caddyfile and Open edX Settings**: Configures the web server and Open edX settings using Tutor plugins, to enable running integration tests from the plugin with multiple sites.

9. **Launch Tutor**: Launches the Open edX platform using Tutor with the specified configuration.

10. **Add Mount for Plugin**: Mounts your plugin into the LMS and CMS containers.

11. **Restart Tutor Services**: Stops and starts Tutor services to apply the new mounts.

12. **Install Open edX Plugin as an Editable Package**: Installs your plugin in editable mode inside both LMS and CMS containers.

13. **Install Extra Requirements**: Installs any additional Python packages specified in `openedx_extra_pip_requirements`.

14. **Run Migrations and Restart Services**: Applies database migrations and restarts Tutor services.

15. **Import Demo Course**: Imports the Open edX demo course for testing purposes.

16. **Test Open edX Imports in Plugin** *(Optional)*: Runs pytest to validate Open edX imports in your plugin if `openedx_imports_test_file_path` is provided. The only two dependencies installed to run these tests are `pytest` and `pytest-django`, so ensure that your import tests do not require any extra packages that are not in the plugin's base requirements.

17. **Load Initial Data for the Tests** *(Optional)*: Loads initial data from a fixtures file into the LMS if `fixtures_file` is provided.

18. **Check LMS Heartbeat**: Verifies that the LMS is running by hitting the heartbeat endpoint.

19. **Set `DEMO_COURSE_ID` Environment Variable**:  
    Sets the `DEMO_COURSE_ID` environment variable based on the Tutor version. This variable allows you to refer to the demo course in your tests, which can be helpful when you need to interact with course content during testing.
    
    **Usage in Your Tests**:  
    In your test code, you can access the `DEMO_COURSE_ID` environment variable to get the identifier of the demo course. For example:
    
    ```python
    import os

    DEMO_COURSE_ID = os.environ.get("DEMO_COURSE_ID")
    # Use DEMO_COURSE_ID in your tests
    ```

20. **Run Integration Tests**: Activates the test virtual environment and runs your integration tests using the specified shell script.

## Notes

- **Using the `"nightly"` Version of Tutor**:  
  The `"nightly"` option allows you to test your plugin against the latest development code of Tutor. This is useful for ensuring compatibility with upcoming features or changes. Be aware that the nightly version may be less stable and could introduce breaking changes. When using `"nightly"`, the action clones the Tutor repository from the `nightly` branch and uses pre-built Tutor images that are published daily to Docker Hub. These images include the latest changes from the master branch at the time of the build. This approach significantly reduces the execution time and conserves the runner's resources by eliminating the overhead of building images during the workflow.

- **Paths**: Ensure that the paths provided in the inputs are relative to your plugin directory.

- **Optional Steps**: Steps involving `openedx_imports_test_file_path` and `fixtures_file` are optional and will only run if the corresponding inputs are provided.

- **Tutor Versions**: Use the matrix strategy to test your plugin against multiple Tutor versions, including the nightly build.

- **Dependencies**: If your integration tests require additional dependencies, specify them in `openedx_extra_pip_requirements` or handle them within your `shell_file_to_run`.

- **Maintaining Python Versions**:

  It's crucial to align the Python version in your virtual environments with the versions supported by the specified Tutor versions. Mismatched Python versions can lead to unexpected errors during Tutor operations and plugin integrations.

  If you need to specify a Python version different from the default provided by the runner, you can add an input to set the desired Python version. For example:

  ```yaml
  - name: Run Integration Tests
    uses: eduNEXT/integration-test-in-tutor@main
    with:
      app_name: 'eox-test'
      tutor_version: ${{ matrix.tutor_version }}
      python-version: '3.X'  # Specify the required Python version here
  ```

  If you're testing against multiple Tutor versions that require different Python versions, you can consider expanding your matrix to include Python versions. For example:

  ```yaml
  strategy:
    matrix:
      include:
        - tutor_version: '<18.0.0'
          python_version: '3.8'
        - tutor_version: '<19.0.0'
          python_version: '3.9'
        - tutor_version: 'nightly'
          python_version: '3.10'
  ```

  Then, adjust the step to use both `matrix.tutor_version` and `matrix.python_version`.

  ```yaml
  steps:
    - name: Run Integration Tests
      uses: eduNEXT/integration-test-in-tutor@main
      with:
        app_name: 'eox-test'
        tutor_version: ${{ matrix.tutor_version }}
        python_version: ${{ matrix.python_version }}  # Utilize matrix.
  ```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.
