{% if cookiecutter.project_variant == "REST_API_client" %}
"""Client bindings to a REST API"""


import httpx

ApiHeaders = dict[str, str]
Secret = str


API_BASEURL = "http://example.com/api/v1"


def api_get(headers: ApiHeaders):
    """HTTP Get the /status endpoint, validating credentials"""
    url = f"{API_BASEURL}/status"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()  # Raise exception on non-OK HTTP status code
    return response.json()


def prep_headers(token: Secret) -> ApiHeaders:
    """Prepare the required API Headers"""
    return {
        "Authorization": f"Bearer {token}",
        # "User-Agent": "cool user agent",
    }


def get_from_api(token: Secret) -> dict:
    """Get the info from API"""
    headers = prep_headers(token)
    api_response = api_get(headers)
    return api_response
{% else %}
{# Cookiecutter doesn't include files conditionally, but CAN set sentinel
 # string and use post-gen hooks to delete the file themselves #}
DELETE THIS FILE DURING POST_GEN HOOK
{% endif %}
