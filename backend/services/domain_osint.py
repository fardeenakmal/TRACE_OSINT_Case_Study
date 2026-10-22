import asyncio
import socket
import subprocess
import httpx
from datetime import datetime
import dns.resolver

async def resolve_dns_records(domain: str) -> dict:
    records = {
        "A": [],
        "AAAA": [],
        "MX": [],
        "NS": [],
        "TXT": [],
        "SOA": []
    }
    
    resolver = dns.resolver.Resolver()
    resolver.timeout = 3.0
    resolver.lifetime = 3.0
    
    for rtype in ["A", "AAAA", "MX", "NS", "TXT", "SOA"]:
        try:
            answers = resolver.resolve(domain, rtype)
            for rdata in answers:
                records[rtype].append(str(rdata).strip('"'))
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
            pass
        except Exception:
            pass
            
    # Fallback for A record if dnspython missed it
    if not records["A"]:
        try:
            ip = socket.gethostbyname(domain)
            records["A"].append(ip)
        except Exception:
            pass
            
    return records

async def fetch_rdap_data(client: httpx.AsyncClient, domain: str) -> dict:
    rdap_info = {
        "domain_name": domain,
        "registrar": "Not available",
        "creation_date": "Not available",
        "expiration_date": "Not available",
        "updated_date": "Not available",
        "status": [],
        "nameservers": [],
        "source": "RDAP / WHOIS"
    }
    
    # 1. Try public RDAP
    try:
        url = f"https://rdap.org/domain/{domain}"
        resp = await client.get(url, timeout=4.0, follow_redirects=True)
        if resp.status_code == 200:
            data = resp.json()
            rdap_info["domain_name"] = data.get("ldhName", domain)
            
            # Events (creation, expiration, etc.)
            for ev in data.get("events", []):
                action = ev.get("eventAction", "")
                date_val = ev.get("eventDate", "")
                if action == "registration":
                    rdap_info["creation_date"] = date_val
                elif action == "expiration":
                    rdap_info["expiration_date"] = date_val
                elif action == "last changed":
                    rdap_info["updated_date"] = date_val
                    
            # Entities (Registrar)
            for ent in data.get("entities", []):
                roles = ent.get("roles", [])
                if "registrar" in roles:
                    vcard = ent.get("vcardArray", [])
                    if len(vcard) > 1:
                        for item in vcard[1]:
                            if item[0] == "fn":
                                rdap_info["registrar"] = item[3]
                                
            # Status
            rdap_info["status"] = data.get("status", [])
            
            # Nameservers
            for ns in data.get("nameservers", []):
                rdap_info["nameservers"].append(ns.get("ldhName", ""))
                
            return rdap_info
    except Exception:
        pass
        
    # 2. Fallback to CLI whois
    try:
        proc = await asyncio.create_subprocess_exec(
            "whois", domain,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=3.0)
        out_text = stdout.decode("utf-8", errors="ignore")
        
        for line in out_text.splitlines():
            line_str = line.strip()
            if "Registrar:" in line_str and rdap_info["registrar"] == "Not available":
                rdap_info["registrar"] = line_str.split(":", 1)[1].strip()
            elif "Creation Date:" in line_str and rdap_info["creation_date"] == "Not available":
                rdap_info["creation_date"] = line_str.split(":", 1)[1].strip()
            elif "Registry Expiry Date:" in line_str and rdap_info["expiration_date"] == "Not available":
                rdap_info["expiration_date"] = line_str.split(":", 1)[1].strip()
            elif "Domain Status:" in line_str:
                status_val = line_str.split(":", 1)[1].strip().split()[0]
                if status_val not in rdap_info["status"]:
                    rdap_info["status"].append(status_val)
            elif "Name Server:" in line_str:
                ns_val = line_str.split(":", 1)[1].strip()
                if ns_val not in rdap_info["nameservers"]:
                    rdap_info["nameservers"].append(ns_val)
                    
        rdap_info["source"] = "WHOIS CLI"
    except Exception:
        pass
        
    return rdap_info

async def fetch_ip_geolocation(client: httpx.AsyncClient, ip: str) -> dict:
    geo = {
        "ip": ip,
        "country": "Unknown",
        "city": "Unknown",
        "isp": "Unknown",
        "org": "Unknown",
        "asn": "Unknown"
    }
    if not ip or ip.startswith("127.") or ip.startswith("10.") or ip.startswith("192.168."):
        return geo
        
    try:
        resp = await client.get(f"http://ip-api.com/json/{ip}", timeout=3.0)
        if resp.status_code == 200:
            d = resp.json()
            if d.get("status") == "success":
                geo["country"] = d.get("country", "Unknown")
                geo["city"] = d.get("city", "Unknown")
                geo["isp"] = d.get("isp", "Unknown")
                geo["org"] = d.get("org", "Unknown")
                geo["asn"] = d.get("as", "Unknown")
    except Exception:
        pass
        
    return geo

async def investigate_domain(domain: str) -> dict:
    clean_domain = domain.strip().lower()
    if clean_domain.startswith("http://"):
        clean_domain = clean_domain[7:]
    if clean_domain.startswith("https://"):
        clean_domain = clean_domain[8:]
    clean_domain = clean_domain.split("/")[0].split(":")[0]
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Resolve DNS records
    dns_records = await resolve_dns_records(clean_domain)
    
    # 2. Query RDAP / WHOIS and IP Geolocation concurrently
    async with httpx.AsyncClient(verify=False) as client:
        primary_ip = dns_records["A"][0] if dns_records["A"] else ""
        rdap_task = fetch_rdap_data(client, clean_domain)
        geo_task = fetch_ip_geolocation(client, primary_ip)
        
        rdap_info, geo_info = await asyncio.gather(rdap_task, geo_task)
        
    # Analyze SPF / DMARC records
    has_spf = any("v=spf1" in txt for txt in dns_records["TXT"])
    
    return {
        "target": clean_domain,
        "investigation_type": "domain",
        "timestamp": timestamp,
        "primary_ip": primary_ip,
        "dns_records": dns_records,
        "registration": rdap_info,
        "geolocation": geo_info,
        "security_posture": {
            "has_spf": has_spf,
            "mx_configured": len(dns_records["MX"]) > 0,
            "nameservers_count": len(dns_records["NS"]) or len(rdap_info["nameservers"]),
            "ipv6_supported": len(dns_records["AAAA"]) > 0
        }
    }

if __name__ == "__main__":
    res = asyncio.run(investigate_domain("example.com"))
    print("Domain investigation for 'example.com':")
    print("  Primary IP:", res["primary_ip"])
    print("  Registrar :", res["registration"]["registrar"])
    print("  Geo       :", res["geolocation"]["city"], res["geolocation"]["country"])
    print("  DNS A     :", res["dns_records"]["A"])
