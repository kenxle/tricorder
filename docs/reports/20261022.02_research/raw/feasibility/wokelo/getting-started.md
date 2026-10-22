> ## Documentation Index
> Fetch the complete documentation index at: https://docs.wokelo.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Getting started

Access your API credentials from the [API Credentials page](https://app.wokelo.ai/dashboard/profile/api-credentials).

Authentication All API requests must be authenticated using a JWT token. Follow the steps below to generate your token:

* Use our authentication end point: `https://api.wokelo.ai/auth/token/`
* Use your Client ID and Client Secret obtained from the API credentials page. Add your email and password. Grant type should be “password”.
* This generates a JWT token.

```json cURL wrap theme={"system"}
curl --location 'https://api.wokelo.ai/auth/token/' \
--form 'username="sam@abconsulting.com"' \
--form 'password="password"' \
--form 'grant_type="password"' \
--form 'client_id="YOUR_CLIENT_ID"' \
--form 'client_secret="YOUR_CLIENT_SECRET"'
```

```json Python expandable wrap theme={"system"}
import requests

url = "https://api.wokelo.ai/auth/token/"

payload = {'username': 'sam@abconsulting.com',
'password': 'password',
'grant_type': 'password',
'client_id': 'YOUR_CLIENT_ID',
'client_secret': 'YOUR_CLIENT_SECRET'}
files=[

]
headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
```

**Make first API call**

Lets try using Market Map API.

```json cURL theme={"system"}
curl --location 'https://api.wokelo.ai/api/enterprise/market-map/enrich/' \
  --header 'Authorization: Bearer <YOUR_API_TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
    "topic": "AI-powered CRM software",
    "parameters": {
      "detailed_query": "B2B CRM tools leveraging AI for sales automation",
      "keywords": ["AI", "CRM", "sales automation"],
      "sample_companies": ["salesforce", "hubspot"],
      "geography": ["USA"],
      "company_type": "private"
    }
  }'
```

```json Python wrap theme={"system"}
import requests

response = requests.post(
    "https://api.wokelo.ai/api/enterprise/market-map/enrich/",
    headers={
        "Authorization": "Bearer <YOUR_API_TOKEN>",
        "Content-Type": "application/json"
    },
    json={
        "topic": "AI-powered CRM software",
        "parameters": {
            "detailed_query": "B2B CRM tools leveraging AI for sales automation",
            "keywords": ["AI", "CRM", "sales automation"],
            "sample_companies": ["salesforce", "hubspot"],
            "geography": ["USA"],
            "company_type": "private"
        }
    }
)
request_id = response.json()["request_id"]
print("Job submitted:", request_id)
```

A successful request should return a request\_id as shown below.

```text theme={"system"}
{
    "request_id": "98620177-6b1d-4cda-837b-2be844ec8d65",
    "status": "PENDING"
}
```

You can then use request result API to view the results.

```json expandable wrap theme={"system"}
{
  "request_id": "a57a9100-e7e1-4c6c-9b29-cdd064516ba7",
  "status": "COMPLETED",
  "result": [
    {
      "Permalink": "esub-construction-software",
      "Name": "eSUB Construction Software",
      "Website": "esub.com",
      "HQ City": "San Diego",
      "HQ Country": "United States",
      "Founded": "2008",
      "Type": "Private",
      "Operating Status": "Operating",
      "Product Category": "Construction Project Management Software",
      "Core Offering": "ESUB Construction Software provides cloud-based project management solutions specifically designed for subcontractors in the construction industry...",
      "Employees (Crunchbase)": "51-100",
      "Funding Stage": "Series B",
      "Total Funding": 22000000.0,
      "Last Funding Date": "2023-05-01",
      "Key Investors": ["Autodesk", "Revolution", "Catalyst Investors"],
      "Overall Score": 7.0,
      "Commentary": "eSUB Construction Software provides cloud-based project management and document control for commercial subcontractors, with mobile field reporting, timecards, RFIs, submittals, and change orders. The platform explicitly serves electrical and HVAC contractors in the United States, making it a strong direct fit for field service management workflows."
    },
    {
      "Permalink": "kloudgin",
      "Name": "KloudGin",
      "Website": "kloudgin.com",
      "HQ City": "Sunnyvale",
      "HQ Country": "United States",
      "Founded": "2014",
      "Type": "Private",
      "Product Category": "Field Service Asset Management Software",
      "Employees (Crunchbase)": "101-250",
      "Funding Stage": "Series A",
      "Total Funding": 8200000.0,
      "Overall Score": 7.0,
      "Commentary": "KloudGin provides cloud-based field service management software and asset management, automating work management processes with scheduling, dispatch, mobile work orders, and billing..."
    }
  ]
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.