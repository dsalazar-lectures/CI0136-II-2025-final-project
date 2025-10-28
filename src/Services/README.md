# Retry Pattern Implementation – Menu Email Delivery

## Functionality Using the Pattern

This pattern is applied in the feature that **sends the menu PDF via email** to users.  
It is implemented in the following components:

- `emailPdf()` — controls retry attempts when sending.
- `sendMenu()` — performs the actual SMTP email sending and reports error status codes.

## Pattern Applied

### Retry Pattern

## Pattern Description

The **Retry Pattern** is used when an operation might fail temporarily, but is likely to succeed if attempted again after a short delay.  
This is particularly useful for external dependencies such as:

- Email / SMTP servers
- Remote APIs
- Network services
- External databases

Instead of failing immediately, the system retries the operation before returning an error, which improves **resilience**, **fault tolerance** and **overall user experience**.

## Motivation

Email sending relies on an external SMTP server, which may respond with **temporary failure codes**, for example:

| Error Code | Meaning |
|-----------|---------|
| 450       | Mailbox busy - try again later |
| 454       | Temporary authentication failure |

These failures are usually **temporary**, meaning retrying after a short delay greatly increases the chance of success.

The Retry Pattern helps prevent false failures and improves system reliability.

## Implementation

### Retry Logic in `emailPdf()`

```python
retryDelay = 3

for x in range(3):
    error = sendMenu(recipientEmail, adapter)
    if error == 450 or error == 454:
        break  # Stop retrying if temporary condition is resolved or successful
    time.sleep(retryDelay)
```

### Error Handling in sendMenu()

```python
except smtplib.SMTPResponseException as error:
    print(f"Error: {error.smtp_error}")
    return error.smtp_code
```

This ensures the retry logic knows which failures are temporary and can act accordingly.

## Benefits

| Benefit | Description |
|--------|-------------|
| **Resilience** | The system keeps functioning even when facing temporary external failures. |
| **Better User Experience** | Reduces unnecessary "email failed" situations. |
| **Maintainability** | Centralizes retry logic for clarity and easier updates. |
| **Reusability** | The pattern can be applied to other external service interactions. |

## Reusable Retry Function

The retry logic can be applied to any operation that might fail temporarily (email sending, API calls, etc.). Simply pass the function, number of attempts, delay, and the errors that should trigger a retry:

```python
def retry(operation, attempts=3, delay=3, retry_errors=[]):
    for _ in range(attempts):
        result = operation()
        if result not in retry_errors:
            return result
        time.sleep(delay)
```

### Example

```python
retry(
    operation=lambda: sendMenu(recipientEmail, adapter),
    attempts=3,
    delay=3,
    retry_errors=[450, 454]
)
```

### This will:

- Retry up to 3 times if the email fails with 450 or 454.
- Wait 3 seconds between attempts.
- Stop immediately if a different error occurs or if the operation succeeds.
