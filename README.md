# URL Response Tester

A lightweight Python command-line tool that repeatedly requests a website and reports HTTP status, response size, per-request download speed, request duration, and cumulative downloaded data. Enter either an `http://` or `https://` URL when the program starts.

> **Important:** This measures the response body returned by one URL. It is useful for observing website response/download performance, but it is **not** a reliable measure of your internet connection's maximum bandwidth. Results depend on the page size, server, network latency, caching, and other factors.

## Features

- Prompts for a URL at startup; supports both HTTP and HTTPS.
- If you enter a domain without a scheme, HTTPS is tried by default.
- Repeats requests until you stop it with `Ctrl+C`.
- Displays the HTTP status code, response-body size, approximate per-request throughput, elapsed time, and cumulative downloaded bytes.
- Formats sizes automatically as B, KB, MB, GB, or TB.
- Prints a summary with request count, successes, failures, total downloaded data, elapsed time, and average throughput.
- Uses only the Python standard library—no third-party dependencies.

## Requirements

- Python 3.8 or newer is recommended.
- An internet connection and access to the target URL.

## Run

Clone the repository:

```bash
git clone https://github.com/msmubassir/url-response-tester.git
cd url-response-tester
```

Run the script:

```bash
python url_response_tester.py
```

Example URL input:

```text
URL Response Tester
Enter an http:// or https:// URL (HTTPS is assumed if omitted).
URL: https://example.com/
```

You can also enter a plain domain, such as `example.com`; the tool will prepend `https://`.

Stop the test with **Ctrl+C**. A summary will be printed when the loop is interrupted.

## Example output

```text
  REQ | STATUS   |       SIZE |        SPEED |      TIME |        TOTAL
----------------------------------------------------------------------------------
    1 | HTTP 200 |    5.12 KB |    120.40 KB/s |   0.043s |      5.12 KB
    2 | HTTP 200 |    5.12 KB |    118.76 KB/s |   0.044s |     10.24 KB
```

Values above are illustrative only; actual values depend on the URL and network. Columns may extend when a server returns a long error message.

## What the numbers mean

| Field | Meaning |
| --- | --- |
| `REQ` | Request number, including failed attempts |
| `STATUS` | HTTP response status, or `FAILED` if the request did not complete |
| `SIZE` | Number of bytes in the response body read by Python |
| `SPEED` | Response body size divided by that request's elapsed time |
| `TIME` | Time taken for the request and body read |
| `TOTAL` | Sum of response-body bytes for successful requests in this run |

Sizes use binary units (1 KB = 1,024 bytes, 1 MB = 1,024 KB, and so on). The displayed speed is a rough application-level measurement and includes request/response overhead; it does not equal raw link throughput.

## Notes and limitations

- The script reads the full response body into memory before calculating its size.
- The reported size is the body delivered by `urllib`, not all network overhead such as TCP/IP, TLS, or HTTP headers.
- A URL can return a valid HTTP error status (for example, `403` or `404`); such responses are reported as HTTP responses rather than transport failures.
- Some websites may rate-limit repetitive requests, block automated traffic, require authentication, or redirect to another page.
- Use a reasonable test target and avoid sending high-frequency traffic to services you do not own or have permission to test.
- If a bare domain's HTTPS endpoint is unavailable, enter the full `http://` URL explicitly to test HTTP instead.

## Troubleshooting

### `HTTP 403` or `HTTP 429`

The server may be blocking automated requests or rate-limiting repeated traffic. This tool does not bypass those restrictions.

### `FAILED` with a timeout or connection error

Check the URL, DNS resolution, internet connection, and whether the server is reachable. For HTTP-only services, type the complete `http://` URL.

### Column alignment

The output uses fixed-width fields for readable columns. Very long error messages can extend beyond the table width.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
