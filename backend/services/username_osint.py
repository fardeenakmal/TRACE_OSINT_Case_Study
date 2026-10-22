import asyncio
import time
import httpx
from datetime import datetime

SOURCES = [
    {
        "name": "GitHub",
        "category": "Developer / Code",
        "url_template": "https://github.com/{}",
        "check_type": "status_code"
    },
    {
        "name": "GitLab",
        "category": "Developer / DevOps",
        "url_template": "https://gitlab.com/{}",
        "check_type": "gitlab_redirect"
    },
    {
        "name": "DockerHub",
        "category": "Containers / Tech",
        "url_template": "https://hub.docker.com/v2/users/{}",
        "check_type": "status_code"
    },
    {
        "name": "Dev.to",
        "category": "Developer Community",
        "url_template": "https://dev.to/{}",
        "check_type": "status_code"
    },
    {
        "name": "HackerNews",
        "category": "Tech Forum",
        "url_template": "https://news.ycombinator.com/user?id={}",
        "check_type": "hn_body"
    },
    {
        "name": "Reddit",
        "category": "Social / Forums",
        "url_template": "https://www.reddit.com/user/{}/about.json",
        "check_type": "reddit_json"
    },
    {
        "name": "Gravatar",
        "category": "Avatar / Identity",
        "url_template": "https://en.gravatar.com/{}.json",
        "check_type": "status_code"
    },
    {
        "name": "Keybase",
        "category": "Cryptography / Identity",
        "url_template": "https://keybase.io/{}",
        "check_type": "status_code"
    },
    {
        "name": "Medium",
        "category": "Blogging / Publishing",
        "url_template": "https://medium.com/@{}",
        "check_type": "status_code"
    },
    {
        "name": "Pinterest",
        "category": "Media / Visual",
        "url_template": "https://www.pinterest.com/{}/",
        "check_type": "status_code"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

async def check_single_source(client: httpx.AsyncClient, source: dict, username: str) -> dict:
    url = source["url_template"].format(username)
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = {
        "source": source["name"],
        "category": source["category"],
        "url": url,
        "timestamp": timestamp,
        "status": "CHECK_FAILED",
        "status_code": None,
        "response_time_ms": 0,
        "verified": False,
        "detail": ""
    }
    
    try:
        resp = await client.get(url, headers=HEADERS, timeout=4.0, follow_redirects=False)
        elapsed_ms = int((time.time() - start_time) * 1000)
        result["response_time_ms"] = elapsed_ms
        result["status_code"] = resp.status_code
        
        if source["check_type"] == "gitlab_redirect":
            if resp.status_code == 200:
                result["status"] = "FOUND"
                result["verified"] = True
                result["detail"] = "GitLab public profile exists"
            elif resp.status_code in (301, 302):
                loc = resp.headers.get("Location", "")
                if "sign_in" in loc or "users/sign_in" in loc:
                    result["status"] = "NOT_FOUND"
                    result["detail"] = "Redirected to login (User not registered)"
                else:
                    result["status"] = "FOUND"
                    result["detail"] = f"Profile redirected to {loc}"
            elif resp.status_code == 404:
                result["status"] = "NOT_FOUND"
                result["detail"] = "Profile does not exist (HTTP 404)"
            else:
                result["status"] = "INCONCLUSIVE"
                result["detail"] = f"Received HTTP {resp.status_code}"
                
        elif source["check_type"] == "hn_body":
            if resp.status_code == 200:
                if "No such user." in resp.text:
                    result["status"] = "NOT_FOUND"
                    result["detail"] = "User does not exist on HackerNews"
                else:
                    result["status"] = "FOUND"
                    result["verified"] = True
                    result["detail"] = "Active user profile confirmed"
            elif resp.status_code == 404:
                result["status"] = "NOT_FOUND"
                result["detail"] = "Account does not exist (HTTP 404)"
            else:
                result["status"] = "NOT_FOUND"
                result["detail"] = f"Profile inactive or not found (HTTP {resp.status_code})"
                
        elif source["check_type"] == "reddit_json":
            if resp.status_code == 200:
                data = resp.json()
                if "data" in data and "name" in data["data"]:
                    result["status"] = "FOUND"
                    result["verified"] = True
                    result["detail"] = f"Reddit user confirmed (karma: {data['data'].get('total_karma', 0)})"
                else:
                    result["status"] = "NOT_FOUND"
                    result["detail"] = "User not found or suspended"
            elif resp.status_code == 404:
                result["status"] = "NOT_FOUND"
                result["detail"] = "Account does not exist"
            elif resp.status_code in (403, 429):
                result["status"] = "INCONCLUSIVE"
                result["detail"] = f"Platform rate limited / Cloudflare challenge (HTTP {resp.status_code})"
            else:
                result["status"] = "CHECK_FAILED"
                result["detail"] = f"Unexpected response HTTP {resp.status_code}"
                
        else:
            if resp.status_code == 200:
                result["status"] = "FOUND"
                result["verified"] = True
                result["detail"] = "Profile page exists and is publicly accessible"
            elif resp.status_code == 404:
                result["status"] = "NOT_FOUND"
                result["detail"] = "Profile does not exist (HTTP 404)"
            elif resp.status_code in (403, 429):
                result["status"] = "INCONCLUSIVE"
                result["detail"] = f"Access restricted or rate limited (HTTP {resp.status_code})"
            elif resp.status_code in (301, 302):
                loc = resp.headers.get("Location", "")
                if any(x in loc for x in ["login", "search", "signup", "sign_in"]):
                    result["status"] = "NOT_FOUND"
                    result["detail"] = f"Redirected to login/landing ({resp.status_code})"
                else:
                    result["status"] = "FOUND"
                    result["detail"] = f"Profile redirected to {loc}"
            else:
                result["status"] = "INCONCLUSIVE"
                result["detail"] = f"Server returned HTTP {resp.status_code}"
                
    except httpx.TimeoutException:
        result["response_time_ms"] = int((time.time() - start_time) * 1000)
        result["status"] = "CHECK_FAILED"
        result["detail"] = "Connection timed out after 4.0s"
    except httpx.ConnectError:
        result["response_time_ms"] = int((time.time() - start_time) * 1000)
        result["status"] = "CHECK_FAILED"
        result["detail"] = "Network connection failed or DNS lookup failed"
    except Exception as e:
        result["response_time_ms"] = int((time.time() - start_time) * 1000)
        result["status"] = "CHECK_FAILED"
        result["detail"] = f"Error during check: {type(e).__name__}"
        
    return result

async def investigate_username(username: str) -> dict:
    clean_username = username.strip().lower()
    async with httpx.AsyncClient(verify=False) as client:
        tasks = [check_single_source(client, src, clean_username) for src in SOURCES]
        results = await asyncio.gather(*tasks)
        
    found_count = sum(1 for r in results if r["status"] == "FOUND")
    not_found_count = sum(1 for r in results if r["status"] == "NOT_FOUND")
    inconclusive_count = sum(1 for r in results if r["status"] == "INCONCLUSIVE")
    failed_count = sum(1 for r in results if r["status"] == "CHECK_FAILED")
    
    return {
        "target": clean_username,
        "investigation_type": "username",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_sources": len(SOURCES),
        "found_count": found_count,
        "not_found_count": not_found_count,
        "inconclusive_count": inconclusive_count,
        "failed_count": failed_count,
        "findings": results
    }
