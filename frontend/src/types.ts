export interface SourceFinding {
  source: string;
  category: string;
  url: string;
  timestamp: string;
  status: 'FOUND' | 'NOT_FOUND' | 'INCONCLUSIVE' | 'CHECK_FAILED';
  status_code: number | null;
  response_time_ms: number;
  verified: boolean;
  detail: string;
}

export interface UsernameResult {
  id: number;
  target: string;
  investigation_type: string;
  timestamp: string;
  total_sources: number;
  found_count: number;
  not_found_count: number;
  inconclusive_count: number;
  failed_count: number;
  findings: SourceFinding[];
  summary: string;
  status: string;
}

export interface DomainResult {
  id: number;
  target: string;
  investigation_type: string;
  timestamp: string;
  primary_ip: string;
  dns_records: {
    A: string[];
    AAAA: string[];
    MX: string[];
    NS: string[];
    TXT: string[];
    SOA: string[];
  };
  registration: {
    domain_name: string;
    registrar: string;
    creation_date: string;
    expiration_date: string;
    updated_date: string;
    status: string[];
    nameservers: string[];
    source: string;
  };
  geolocation: {
    ip: string;
    country: string;
    city: string;
    isp: string;
    org: string;
    asn: string;
  };
  security_posture: {
    has_spf: boolean;
    mx_configured: boolean;
    nameservers_count: number;
    ipv6_supported: boolean;
  };
  summary: string;
  status: string;
}

export interface HistoryItem {
  id: number;
  inv_type: 'username' | 'domain';
  target: string;
  timestamp: string;
  status: string;
  summary: string;
}

export interface DashboardStats {
  total_investigations: number;
  total_usernames: number;
  total_domains: number;
  recent_activity: HistoryItem[];
  supported_sources_count: number;
}
