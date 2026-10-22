> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Login

> Obtain a JSON Web Token (JWT) for subsequent API authentication

All API requests must be authenticated using a JWT token. Follow the steps below to generate your token:

## Overview

Obtain a JSON Web Token (JWT) ffor subsequent API authentication

## Endpoint Details

* **Method:** POST
* **Endpoint:** `/auth/token/`

## Request

### Request Parameters

Submit the following parameters as form-data in the request body:

**client\_id** `string` *required*

Unique identifier for your organization, obtained from the [API Credentials page](https://app.wokelo.ai/dashboard/profile/api-credentials)

**client\_secret** `string` *required*

Secret key for your organization, obtained from the [API Credentials page](https://app.wokelo.ai/dashboard/profile/api-credentials)

**username** `string` *required*

Your email address used for Wokelo login

**password** `string` *required*

Your account password used for Wokelo login

**grant\_type** `string` *required*

Type of grant being requested (use `"password"` for credential-based authentication)

## Response

### Response Fields

On successful authentication (HTTP 200), the response will contain:

**access\_token** `string`

JWT for authenticated API access

**expires\_in** `integer`

Token validity duration in seconds

**token\_type** `string`

Type of authentication token

**scope** `string`

Authorization scope of the token

**refresh\_token** `string`

Token used to obtain a new access token

* Ensure the `client_id` and `client_secret` are kept confidential
* Any token returned by the API is sensitive and should be stored securely. Wokelo tokens are long-lasting and should never be exposed on the client side.
* The access token is time-limited; use the refresh token to obtain a new access token when it expires
* Use HTTPS for all authentication requests

```json 200 theme={"system"}
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 2628288,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.