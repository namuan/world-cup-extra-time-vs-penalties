"""Download RSSSF match-result pages for the included World Cups."""

import sys
import time
from pathlib import Path

import requests
from requests.exceptions import RequestException

from world_cup_penalties.config import (
    INVENTORY_PATH,
    RAW_DIR,
    RSSSF_DIR,
    RSSSF_URLS,
)


def download_page(url: str, save_path: Path, timeout: int = 30) -> bool:
    """Download a single URL to a file. Returns True on success."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_bytes(resp.content)
        return True
    except RequestException as exc:
        print(f"  FAILED: {url} — {exc}", file=sys.stderr)
        return False


def write_inventory(entries: list[dict]) -> None:
    """Write a CSV inventory of downloaded sources."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["year,url,local_path,status"]
    for entry in entries:
        lines.append(
            f"{entry['year']},{entry['url']},{entry['local_path']},{entry['status']}"
        )
    INVENTORY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Inventory written → {INVENTORY_PATH}")


def main() -> None:
    """Download all RSSSF pages and write the source inventory."""
    RSSSF_DIR.mkdir(parents=True, exist_ok=True)

    entries: list[dict] = []
    all_ok = True

    for year in sorted(RSSSF_URLS):
        url = RSSSF_URLS[year]
        filename = f"world_cup_{year}.html"
        save_path = RSSSF_DIR / filename

        print(f"[{year}] {url}")
        ok = download_page(url, save_path)
        entries.append(
            {
                "year": year,
                "url": url,
                "local_path": str(save_path.relative_to(RAW_DIR.parent)),
                "status": "ok" if ok else "error",
            }
        )
        if not ok:
            all_ok = False

        # Be polite — don't hammer the server
        time.sleep(1.0)

    write_inventory(entries)

    if all_ok:
        print("\nAll pages downloaded successfully.")
    else:
        print("\nSome downloads FAILED. See inventory for details.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
