## Making DRS Requests

The DRS implementation is responsible for defining and enforcing an authorization policy that determines which users are allowed to make which requests. GA4GH recommends that DRS implementations use an OAuth 2.0 [bearer token](https://oauth.net/2/bearer-tokens/), although they can choose other mechanisms if appropriate.

## Fetching DRS Objects

The DRS API allows implementers to support a variety of different content access policies, depending on what `AccessMethod` records they return:

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

DRS implementers should ensure their solutions restrict access to targets as much as possible, detect attempts to exploit through log monitoring, and they are prepared to take action if an exploit in their DRS implementation is detected.
