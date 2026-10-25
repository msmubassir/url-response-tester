#!/usr/bin/env python3
"""Repeatedly request a URL and report status, response size, speed, and totals."""

import time
import urllib.error
import urllib.request


def fmt_bytes(value):
    """Format bytes using binary units."""
    value = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(value) < 1024 or unit == "TB":
            return f"{value:.2f} {unit}"
        value /= 1024


def normalize_url(value):
    value = value.strip()
    if not value:
        return ""

    # Accept URLs with or without a scheme; default to HTTPS if omitted.
    if not value.startswith(("http://", "https://")):
        value = "https://" + value

    return value


def main():
    print("URL Bandwidth / Response Tester")
    print("Enter an http:// or https:// URL (HTTPS is assumed if omitted).")
    url = normalize_url(input("URL: "))

    if not url:
        print("Error: URL cannot be empty.")
        return

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "Chrome/130.0.0.0 Safari/537.36"
        )
    }

    count = total = success = failed = 0
    start_all = time.perf_counter()

    print()
    print(
        "{:>5} | {:<8} | {:>10} | {:>12} | {:>9} | {:>12}".format(
            "REQ", "STATUS", "SIZE", "SPEED", "TIME", "TOTAL"
        )
    )
    print("-" * 82)

    try:
        while True:
            count += 1
            start = time.perf_counter()

            try:
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request, timeout=10) as response:
                    data = response.read()
                    elapsed = time.perf_counter() - start
                    size = len(data)
                    total += size
                    success += 1
                    speed = size / elapsed if elapsed else 0

                    print(
                        "{:5} | {:<8} | {:>10} | {:>12} | {:>8.3f}s | {:>12}".format(
                            count,
                            "HTTP " + str(response.status),
                            fmt_bytes(size),
                            fmt_bytes(speed) + "/s",
                            elapsed,
                            fmt_bytes(total),
                        ),
                        flush=True,
                    )

            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                failed += 1
                elapsed = time.perf_counter() - start
                message = str(exc).replace("\n", " ")
                print(
                    "{:5} | {:<8} | {:>10} | {:>12} | {:>8.3f}s | {}".format(
                        count, "FAILED", "-", "-", elapsed, message
                    ),
                    flush=True,
                )

    except KeyboardInterrupt:
        elapsed = time.perf_counter() - start_all
        print("\n\n--- SUMMARY ---")
        print(f"URL: {url}")
        print(f"Requests: {count} | Success: {success} | Failed: {failed}")
        print(f"Downloaded: {fmt_bytes(total)} | Elapsed: {elapsed:.2f}s")
        if elapsed:
            print(f"Average throughput: {fmt_bytes(total / elapsed)}/s")


if __name__ == "__main__":
    main()
