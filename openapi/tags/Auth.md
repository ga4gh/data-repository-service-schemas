## Making DRS Requests

The DRS implementation is responsible for defining and enforcing an authorization policy that determines which users are allowed to make which requests. GA4GH recommends that DRS implementations use an OAuth 2.0 [bearer token](https://oauth.net/2/bearer-tokens/) or a [GA4GH Passport](https://github.com/ga4gh-duri/ga4gh-duri.github.io/tree/master/researcher_ids), although they can choose other mechanisms if appropriate.

## Fetching DRS Objects

The DRS API allows implementers to support a variety of different content access policies, depending on what `AccessMethod` records they return.  Implementers have a choice to make the
GET /objects/{object_id} and GET /objects/{object_id}/access/{access_id} calls open or requiring a Basic, Bearer, or Passport token (Passport requiring a POST).  The following describes the
various access approaches following a successful GET/POST /objects/{object_id} request in order to them obtain access to the bytes for a given object ID/access ID:

* public content:
    * server provides an `access_url` with a `url` and no `headers`
    * caller fetches the object bytes without providing any auth info
* private content that requires the caller to have out-of-band auth knowledge (e.g. service account credentials):
    * server provides an `access_url` with a `url` and no `headers`
    * caller fetches the object bytes, passing the auth info they obtained out-of-band
* private content that requires the caller to pass an Authorization token:
    * server provides an `access_url` with a `url` and `headers`
    * caller fetches the object bytes, passing auth info via the specified header(s)
* private content that uses an expensive-to-generate auth mechanism (e.g. a signed URL):
    * server provides an `access_id`
    * caller passes the `access_id` to the `/access` endpoint
    * server provides an `access_url` with the generated mechanism (e.g. a signed URL in the `url` field)
    * caller fetches the object bytes from the `url` (passing auth info from the specified headers, if any)

In the approaches above [GA4GH Passports](https://github.com/ga4gh-duri/ga4gh-duri.github.io/tree/master/researcher_ids) are not mentioned and that is on purpose.  A DRS server may return a Bearer token or other platform-specific token in a header in response to a valid Bearer token or GA4GH Passport (Option 3 above).  But it is not the responsibility of a DRS server to return a Passport, that is the responsibility of a Passport Broker and outside the scope of DRS.

DRS implementers should ensure their solutions restrict access to targets as much as possible, detect attempts to exploit through log monitoring, and they are prepared to take action if an exploit in their DRS implementation is detected.

## Authentication

### Discovery

The APIs to fetch [DrsObjects](#tag/DrsObjectModel) and [AccessURLs](#tag/AccessURLModel) may require authorization. The authorization mode may vary between DRS objects hosted by a service. The authorization mode may vary between the APIs to fetch a [DrsObject](#tag/DrsObjectModel) and an associated [AccessURL](#tag/AccessURLModel). Implementers should indicate how to authenticate to fetch a [DrsObject](#tag/DrsObjectModel) by implementing the [OptionsObject](#operation/OptionsObject) API. Implementers should indicate how to authenticate to fetch an [AccessURL](#tag/AccessURLModel) within a [DrsObject](#tag/DrsObjectModel). 

### Modes

#### BasicAuth

A valid authorization token must be passed in the 'Authorization' header, e.g. "Basic ${token_string}"

| Security Scheme Type | HTTP |
|----------------------|------|
| **HTTP Authorization Scheme** | basic |

#### BearerAuth

A valid authorization token must be passed in the 'Authorization' header, e.g. "Bearer ${token_string}"

| Security Scheme Type | HTTP |
|----------------------|------|
| **HTTP Authorization Scheme** | bearer |

#### PassportAuth

A valid authorization [GA4GH Passport](https://github.com/ga4gh-duri/ga4gh-duri.github.io/tree/master/researcher_ids) token must be passed in the body of a POST request

| Security Scheme Type | HTTP |
|----------------------|------|
| **HTTP POST** | tokens[] |
