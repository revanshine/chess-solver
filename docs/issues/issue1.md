Here are the current test failures and their causes:

1. **test_settings_missing_secret_key_raises_error**:
   - The test expects a `ValueError` if `secret_key` is missing, but no error is raised.
   - This is because `secret_key` has a default value in your `Settings` model, so it is never "missing".

2. **test_get_settings_returns_settings_instance** and **test_get_settings_cache_can_be_cleared**:
   - These tests expect the `secret_key` to be set from the environment, but the default value is always used.
   - This is because the `Settings` model's `secret_key` field has a default, so environment variables are ignored unless the default is removed.

3. **test_app_creation**:
   - The test expects the app title to be `"Test Codex Template"`, but it is `"Codex Template"`.
   - This is because the `settings` instance is created at import time and does not use the test settings.

4. **test_async_health_endpoint**:
   - The test tries to call `await async_client.get("/health")`, but `async_client` is an async generator, not an `AsyncClient` instance.

Would you like to:
- Make `secret_key` a required field (no default) so tests and security are correct?
- Refactor how settings are injected/mocked for tests?
- Fix the async client fixture usage?

Let me know if you want all of these fixed, or only specific ones.