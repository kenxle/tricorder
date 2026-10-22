> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Company Jobs

## Overview

The Get Company Jobs API fetches the currently listed job postings for a given company. Each posting includes the title, location, work arrangement, any disclosed salary metadata, and a `job_id`. Results are returned synchronously in the API response and paginated using `page` and `page_size`.

To retrieve the full posting — complete description, structured requirements, and resolved metadata — pass the `job_id` from this response to the Get Job Details API.

## Endpoint Details

* **Method:** GET
* **Endpoint:** `api/enterprise/company/jobs/`

## Authentication requirements

* Include a valid JWT token in your request header
* If you don't have a token yet, you can get one from the `/auth/token/` endpoint first.

## Request

### Request Parameters

#### Header Parameters

**token** `string` *required*

JWT token obtained from the Authentication request

### URL Parameters

**company** `string` *required*

Company permalink or a valid company URL for which job postings need to be fetched (e.g., `tesla` or `https://www.tesla.com/`)

**page** `integer`

The page number to retrieve. Used together with `page_size` to paginate through results.

Default = 1

**page\_size** `integer`

Number of job results to return per page.

Default = 50

Max value = 500

## Response

#### Successful Response Fields

Returns a JSON object with the following structure:

**status** `string`

`"success"` if the request was processed successfully.

**data** `array`

List of job postings for the requested page. Each object contains the fields below.

**Job object**

**job\_id** `string`

Unique identifier for the posting. Pass this to the Get Job Details API to retrieve the full posting.

**title** `string`

Job title as listed.

**url** `string`

Canonical URL of the original job posting.

**location** `string`

Location of the role (city, region, country). May be empty for fully remote roles.

**description** `string`

Short description of the role when available. Often empty in the listing — use Get Job Details for the full text.

**type** `string`

Employment type (e.g. full-time, part-time, contract). Empty string when not specified.

**remote\_allow** `boolean`

`true` when the role permits remote work.

**salary\_display** `string`

Human-readable salary string as shown on the posting. Empty when not disclosed.

**salary\_details** `object`

Structured salary breakdown when available. Empty object when not disclosed.

**min\_salary** `number`

Lower bound of the salary range. `null` when not disclosed.

**max\_salary** `number`

Upper bound of the salary range. `null` when not disclosed.

**compensation\_type** `string`

Compensation basis (e.g. base salary, hourly). Empty string when not specified.

**pay\_period** `string`

Pay period the salary refers to (e.g. yearly, hourly). Empty string when not specified.

**currency\_code** `string`

ISO 4217 currency code of the salary figures (e.g. `USD`). Empty string when not disclosed.

**job\_functions** `array`

Functional categories for the role. Empty array when not classified.

**industries** `array`

Industries associated with the role. Empty array when not classified.

**experience\_level** `string`

Seniority/experience level (e.g. entry, mid, senior). Empty string when not specified.

**skills** `array`

Skills associated with the role. Empty array when not detected.

**benefits** `array`

Listed benefits. Empty array when none specified.

**listed\_at\_date** `string`

Date the posting was listed. `null` when not available.

**original\_listed\_date** `string`

Date the posting was originally listed. `null` when not available.

**expire\_at** `string`

Expiry date of the posting. `null` when no expiry is set.

```javascript JavaScript - Fetch theme={"system"}
const myHeaders = new Headers();
myHeaders.append("Authorization", "Bearer Token");
myHeaders.append("Content-Type", "application/json");

const requestOptions = {
  method: "GET",
  headers: myHeaders,
  redirect: "follow"
};

fetch("{{path}}/api/enterprise/company/jobs/?company=tesla&page=1&page_size=50", requestOptions)
  .then((response) => response.text())
  .then((result) => console.log(result))
  .catch((error) => console.error(error));
```

```python Python theme={"system"}
import requests

url = "{{path}}/api/enterprise/company/jobs/"

headers = {
    "Authorization": "Bearer Token",
    "Content-Type": "application/json"
}

params = {
    "company": "tesla",
    "page": 1,
    "page_size": 50
}

response = requests.get(url, headers=headers, params=params)
print(response.json())
```

```bash cURL theme={"system"}
curl --location '{{path}}/api/enterprise/company/jobs/?company=tesla&page=1&page_size=50' \
  --header 'Authorization: Bearer Token' \
  --header 'Content-Type: application/json'
```

```go Go theme={"system"}
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	url := "{{path}}/api/enterprise/company/jobs/?company=tesla&page=1&page_size=50"

	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Add("Authorization", "Bearer Token")
	req.Header.Add("Content-Type", "application/json")

	res, _ := http.DefaultClient.Do(req)
	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)
	fmt.Println(string(body))
}
```

```java Java theme={"system"}
OkHttpClient client = new OkHttpClient();

Request request = new Request.Builder()
  .url("{{path}}/api/enterprise/company/jobs/?company=tesla&page=1&page_size=50")
  .get()
  .addHeader("Authorization", "Bearer Token")
  .addHeader("Content-Type", "application/json")
  .build();

Response response = client.newCall(request).execute();
System.out.println(response.body().string());
```

```json 200 theme={"system"}
{
    "status": "success",
    "data": [
        {
            "job_id": "4426093115",
            "title": "大阪【自動運転テストドライバー】",
            "url": "https://www.linkedin.com/jobs/view/4426093115",
            "location": "Osaka, Osaka, Japan",
            "description": "",
            "type": "",
            "remote_allow": true,
            "salary_display": "",
            "salary_details": {},
            "min_salary": null,
            "max_salary": null,
            "compensation_type": "",
            "pay_period": "",
            "currency_code": "",
            "job_functions": [],
            "industries": [],
            "experience_level": "",
            "expire_at": null,
            "listed_at_date": null,
            "original_listed_date": null,
            "skills": [],
            "benefits": []
        },
        {
            "job_id": "4426101005",
            "title": "Service Advisor, Oakleigh",
            "url": "https://www.linkedin.com/jobs/view/4426101005",
            "location": "Oakleigh South, Victoria, Australia",
            "description": "",
            "type": "",
            "remote_allow": true,
            "salary_display": "",
            "salary_details": {},
            "min_salary": null,
            "max_salary": null,
            "compensation_type": "",
            "pay_period": "",
            "currency_code": "",
            "job_functions": [],
            "industries": [],
            "experience_level": "",
            "expire_at": null,
            "listed_at_date": null,
            "original_listed_date": null,
            "skills": [],
            "benefits": []
        }
    ]
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.