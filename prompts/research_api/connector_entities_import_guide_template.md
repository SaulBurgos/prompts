# Entities Imported from {AI_FILL: API Name}

Official REST API website: {AI_FILL: API website}

- Base URL: https://{AI_FILL: base url}
- Endpoint Pattern: https://{AI_FILL: base url}/{AI_FILL: resource}/


# List of endpoints

## {AI_FILL: resource name}

*Note: {AI_FILL: important information related to this endpoint.}*

- Documentation Link: {AI_FILL: link to documentation}
- Endpoint URL: {AI_FILL: endpoint link}
- Method: {AI_FILL: method to use, ex: GET,POST, DELETE}

- API Version(s) Supported: {AI_FILL: e.g., v1, v2}
- Resource Version (this resource): {AI_FILL: e.g., v2.3 or 2024-08-01}
- Versioning Mechanism: {AI_FILL: Path (/v1)|Header (Accept/X-API-Version)|Query (?version=)}
- Version Header/Param Details: {AI_FILL: e.g., Accept: application/vnd.api+json;version=2}
- Changelog/Release Notes: {AI_FILL: link}

- Supports Pagination: {AI_FILL: Yes/No/Partial}
  - Details: {AI_FILL: type: cursor|offset; params: page|per_page|limit|cursor; max_page_size: N; envelope: data|items + meta.next}

- Supports Filters: {AI_FILL: Yes/No/Partial}
  - Details: {AI_FILL: params and operators; date format/timezone; inclusive/exclusive bounds}

- Supports Incremental Loading: {AI_FILL: Yes/No/Partial}
  - Details: {AI_FILL: field: created_at|updated_at|modifiedTime; format: ISO 8601; precision: s|ms; cache headers: ETag|If-Modified-Since}

- Supports Soft Delete: {AI_FILL: Yes/No/Partial}
  - Details: {AI_FILL: flag: deleted|archived; timestamp: deleted_at; included_by_default: true|false; tombstone endpoint: yes|no}

- Supports Partial Responses: {AI_FILL: Yes/No/Partial}
  - Details: {AI_FILL: param: fields|select; syntax: comma-separated; nesting: yes|no}

- Exposes Rate Limit Headers: {AI_FILL: Yes/No}
  - Details: {AI_FILL: X-RateLimit-Remaining|Retry-After|X-RateLimit-Reset; official limits; recommended backoff}

- Primary Key Defined Clearly: {AI_FILL: Yes/No}
  - Details: {AI_FILL: pk fields; composite: yes|no; type + stability; upsert key strategy}

Response Formats & Compression: {AI_FILL: JSON/CSV/XML; gzip/br}

### Properties to Import
- {AI_FILL: property name} ({AI_FILL: type}, {AI_FILL: nullability})
  - Maps to: {AI_FILL: protiv standard model}


#### Examples of properties: 

- id (string, non-null)
- updated_at (datetime, non-null)
- deleted_at (datetime, nullable)
- name (string, non-null)
  - Maps to: Protiv User.name
- is_active (boolean, non-null)
- address.city (string, nullable)

### Example of request
    curl -sS -H "Authorization: Bearer {AI_FILL: token}" \
      "{AI_FILL: baseUrl}/{AI_FILL: resource}?limit={AI_FILL: page_size}&{AI_FILL: updated_field}[gte]={AI_FILL: ISO8601_TIMESTAMP}"

### Example of response
    {
      "data": [{ "id": "{AI_FILL}", "...": "..." }],
      "meta": { "next": "{AI_FILL: cursor or null}" }
    }

### Example of error (rate limited)
    {
      "error": "rate_limited",
      "message": "Too many requests"
    }
