# Trade the service account's key file for a one-hour Google sign-in token (OAuth 2), as the SDK does itself.
import google.auth
import google.auth.transport.requests

credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())
print(credentials.token)
