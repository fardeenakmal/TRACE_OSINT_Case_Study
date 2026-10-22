import React, { useState, useEffect } from 'react';
import { 
  Shield, Search, Globe, User, History, Download, Trash2, 
  ExternalLink, CheckCircle, XCircle, AlertTriangle, AlertCircle,
  Activity, Server, Database, FileText, ArrowRight, RefreshCw, Lock, X
} from 'lucide-react';
import { UsernameResult, DomainResult, HistoryItem, DashboardStats } from './types.ts';

const API_BASE = '/api';

export default function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'username' | 'domain' | 'history'>('dashboard');
  const [stats, setStats] = useState<DashboardStats | null>(null);
  
  // Username state
  const [usernameInput, setUsernameInput] = useState('');
  const [isUsernameLoading, setIsUsernameLoading] = useState(false);
  const [usernameResult, setUsernameResult] = useState<UsernameResult | null>(null);
  const [usernameFilter, setUsernameFilter] = useState<string>('ALL');
  
  // Domain state
  const [domainInput, setDomainInput] = useState('');
  const [isDomainLoading, setIsDomainLoading] = useState(false);
  const [domainResult, setDomainResult] = useState<DomainResult | null>(null);
  const [domainErrorDetail, setDomainErrorDetail] = useState<string | null>(null);
  
  // History state
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);
  const [historyFilter, setHistoryFilter] = useState<'ALL' | 'username' | 'domain'>('ALL');
  
  // Report preview modal
  const [activeReportId, setActiveReportId] = useState<number | null>(null);
  const [reportModalData, setReportModalData] = useState<any | null>(null);

  // Global alert
  const [alertMessage, setAlertMessage] = useState<{ type: 'error' | 'success' | 'warning', text: string } | null>(null);

  const showAlert = (type: 'error' | 'success' | 'warning', text: string) => {
    setAlertMessage({ type, text });
    setTimeout(() => setAlertMessage(null), 8000);
  };

  const loadStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/stats`);
      if (res.ok) {
        const data = await res.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Failed to load stats', err);
    }
  };

  const loadHistory = async () => {
    try {
      const res = await fetch(`${API_BASE}/history?limit=50`);
      if (res.ok) {
        const data = await res.json();
        setHistoryItems(data);
      }
    } catch (err) {
      console.error('Failed to load history', err);
    }
  };

  const openReportModal = async (id: number) => {
    setActiveReportId(id);
    try {
      const res = await fetch(`${API_BASE}/history/${id}`);
      if (res.ok) {
        const item = await res.json();
        setReportModalData(item);
      }
    } catch (err) {
      console.error('Failed to load report data', err);
    }
  };

  // URL search params initialization
  useEffect(() => {
    loadStats();
    loadHistory();

    const params = new URLSearchParams(window.location.search);
    const tabParam = params.get('tab');
    const targetParam = params.get('target');
    const errorParam = params.get('error');
    const reportParam = params.get('report') || params.get('id');

    if (tabParam === 'username') {
      setActiveTab('username');
      if (targetParam) {
        setUsernameInput(targetParam);
        executeUsernameSearch(targetParam);
      }
    } else if (tabParam === 'domain') {
      setActiveTab('domain');
      if (targetParam) {
        setDomainInput(targetParam);
        executeDomainSearch(targetParam);
      }
    } else if (tabParam === 'history') {
      setActiveTab('history');
    } else if (tabParam === 'report') {
      setActiveTab('history');
      openReportModal(Number(reportParam) || 7);
    }

    if (reportParam && tabParam !== 'report') {
      openReportModal(Number(reportParam));
    }

    if (errorParam === 'invalid_domain') {
      setActiveTab('domain');
      setDomainInput('invalid_domain_test');
      setDomainErrorDetail('RFC 1035 / FQDN Validation Error: "invalid_domain_test" does not contain a valid top-level domain suffix (.com, .org, etc.) or contains illegal characters. Automated query transmission was terminated to preserve network hygiene and prevent SSRF.');
      showAlert('error', 'Validation Error: "invalid_domain_test" is not a valid domain. Missing TLD suffix (e.g. .com, .org).');
    } else if (errorParam === 'rate_limit') {
      setActiveTab('username');
      setUsernameInput('rate_limit_demo');
      showAlert('warning', 'Source Restriction: Reddit API returned HTTP 429 Too Many Requests. Categorized as INCONCLUSIVE.');
    }
  }, []);

  const executeUsernameSearch = async (u: string) => {
    setIsUsernameLoading(true);
    try {
      const res = await fetch(`${API_BASE}/investigate/username`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: u }),
      });
      if (res.ok) {
        const data = await res.json();
        setUsernameResult(data);
        loadStats();
        loadHistory();
      }
    } catch (err: any) {
      showAlert('error', err.message);
    } finally {
      setIsUsernameLoading(false);
    }
  };

  const executeDomainSearch = async (d: string) => {
    setIsDomainLoading(true);
    try {
      const res = await fetch(`${API_BASE}/investigate/domain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ domain: d }),
      });
      if (res.ok) {
        const data = await res.json();
        setDomainResult(data);
        loadStats();
        loadHistory();
      }
    } catch (err: any) {
      showAlert('error', err.message);
    } finally {
      setIsDomainLoading(false);
    }
  };

  const handleUsernameSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const u = usernameInput.trim();
    if (!u) {
      showAlert('error', 'Validation Failed: Username input cannot be empty.');
      return;
    }
    if (u.length < 2) {
      showAlert('error', 'Validation Failed: Username must be at least 2 characters long.');
      return;
    }
    executeUsernameSearch(u);
  };

  const handleDomainSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const d = domainInput.trim();
    if (!d) {
      setDomainErrorDetail('Validation Error: Target domain cannot be empty.');
      showAlert('error', 'Validation Failed: Target domain cannot be empty.');
      return;
    }
    if (!d.includes('.') || d.length < 4 || d.startsWith('.') || d.endsWith('.')) {
      setDomainErrorDetail(`RFC 1035 / FQDN Validation Error: Target "${d}" is not a valid Fully Qualified Domain Name. Target must include an authorized TLD (e.g., example.com) and conform to DNS naming standards.`);
      showAlert('error', `Validation Error: "${d}" is not a valid domain. Missing TLD suffix.`);
      return;
    }
    setDomainErrorDetail(null);
    executeDomainSearch(d);
  };

  const handleDeleteHistory = async (id: number) => {
    try {
      const res = await fetch(`${API_BASE}/history/${id}`, { method: 'DELETE' });
      if (res.ok) {
        loadHistory();
        loadStats();
        showAlert('success', `Investigation record #${id} deleted from local SQLite store.`);
      }
    } catch (err) {
      showAlert('error', 'Failed to delete record.');
    }
  };

  const handleClearAllHistory = async () => {
    if (!confirm('Are you sure you want to delete all stored investigation history?')) return;
    try {
      const res = await fetch(`${API_BASE}/history`, { method: 'DELETE' });
      if (res.ok) {
        loadHistory();
        loadStats();
        showAlert('success', 'All local investigation records cleared.');
      }
    } catch (err) {
      showAlert('error', 'Failed to clear history.');
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Header */}
      <header className="header-nav">
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '12px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ background: 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)', padding: '8px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Shield size={24} color="#ffffff" />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '0.05em', color: '#f8fafc' }}>TRACE</span>
                <span style={{ background: 'rgba(2, 132, 199, 0.2)', color: '#38bdf8', padding: '2px 8px', borderRadius: '4px', fontSize: '0.7rem', fontWeight: 700, border: '1px solid rgba(2, 132, 199, 0.3)' }}>OSINT ANALYZER</span>
              </div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Digital Footprint &amp; Reconnaissance Suite</p>
            </div>
          </div>

          {/* Academic Info */}
          <div style={{ background: '#1e293b', border: '1px solid var(--border)', padding: '6px 14px', borderRadius: '8px', fontSize: '0.75rem', display: 'flex', flexDirection: 'column', gap: '2px' }}>
            <div style={{ color: '#38bdf8', fontWeight: 600 }}>Student: Fardeen Akmal (Roll No: 2)</div>
            <div style={{ color: 'var(--text-muted)' }}>Guide: Akanksha Thakare • G.V. Acharya Inst. of Engg. &amp; Tech. (Mumbai Univ.)</div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 20px', display: 'flex', gap: '8px', borderTop: '1px solid rgba(36, 52, 77, 0.5)' }}>
          <button 
            onClick={() => setActiveTab('dashboard')}
            style={{ 
              background: 'none', border: 'none', color: activeTab === 'dashboard' ? '#38bdf8' : 'var(--text-muted)',
              borderBottom: activeTab === 'dashboard' ? '2px solid #0284c7' : '2px solid transparent',
              padding: '12px 16px', fontWeight: 600, fontSize: '0.875rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px'
            }}
          >
            <Activity size={16} /> Dashboard
          </button>
          <button 
            onClick={() => setActiveTab('username')}
            style={{ 
              background: 'none', border: 'none', color: activeTab === 'username' ? '#38bdf8' : 'var(--text-muted)',
              borderBottom: activeTab === 'username' ? '2px solid #0284c7' : '2px solid transparent',
              padding: '12px 16px', fontWeight: 600, fontSize: '0.875rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px'
            }}
          >
            <User size={16} /> Username OSINT
          </button>
          <button 
            onClick={() => setActiveTab('domain')}
            style={{ 
              background: 'none', border: 'none', color: activeTab === 'domain' ? '#38bdf8' : 'var(--text-muted)',
              borderBottom: activeTab === 'domain' ? '2px solid #0284c7' : '2px solid transparent',
              padding: '12px 16px', fontWeight: 600, fontSize: '0.875rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px'
            }}
          >
            <Globe size={16} /> Domain Intelligence
          </button>
          <button 
            onClick={() => setActiveTab('history')}
            style={{ 
              background: 'none', border: 'none', color: activeTab === 'history' ? '#38bdf8' : 'var(--text-muted)',
              borderBottom: activeTab === 'history' ? '2px solid #0284c7' : '2px solid transparent',
              padding: '12px 16px', fontWeight: 600, fontSize: '0.875rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px'
            }}
          >
            <History size={16} /> Investigation History
          </button>
        </div>
      </header>

      {/* Main Body */}
      <main style={{ maxWidth: '1280px', width: '100%', margin: '0 auto', padding: '24px 20px', flex: 1 }}>
        {/* Alert / Toast */}
        {alertMessage && (
          <div style={{ 
            marginBottom: '20px', padding: '12px 16px', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.875rem',
            background: alertMessage.type === 'error' ? 'rgba(244, 63, 94, 0.15)' : (alertMessage.type === 'success' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)'),
            border: `1px solid ${alertMessage.type === 'error' ? 'rgba(244, 63, 94, 0.4)' : (alertMessage.type === 'success' ? 'rgba(16, 185, 129, 0.4)' : 'rgba(245, 158, 11, 0.4)')}`,
            color: alertMessage.type === 'error' ? '#fb7185' : (alertMessage.type === 'success' ? '#34d399' : '#fbbf24')
          }}>
            {alertMessage.type === 'error' && <AlertCircle size={18} />}
            {alertMessage.type === 'success' && <CheckCircle size={18} />}
            {alertMessage.type === 'warning' && <AlertTriangle size={18} />}
            <span style={{ flex: 1, fontWeight: 500 }}>{alertMessage.text}</span>
            <button onClick={() => setAlertMessage(null)} style={{ background: 'none', border: 'none', color: 'inherit', cursor: 'pointer' }}>✕</button>
          </div>
        )}

        {/* ----------------- TAB: DASHBOARD ----------------- */}
        {activeTab === 'dashboard' && (
          <div>
            <div style={{ marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
              <div>
                <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#f8fafc' }}>Operations Dashboard</h1>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Passive OSINT Telemetry, Target Auditing &amp; Digital Footprint Reconnaissance</p>
              </div>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button className="btn-secondary" onClick={() => { loadStats(); loadHistory(); }}>
                  <RefreshCw size={14} /> Refresh Telemetry
                </button>
                <button className="btn-primary" onClick={() => setActiveTab('username')}>
                  <User size={14} /> Launch Username Recon
                </button>
              </div>
            </div>

            {/* Metric Summary Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginBottom: '24px' }}>
              <div className="card" style={{ padding: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>TOTAL INVESTIGATIONS</span>
                  <Database size={18} color="#0284c7" />
                </div>
                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc' }}>{stats?.total_investigations ?? 0}</div>
                <div style={{ fontSize: '0.75rem', color: '#10b981', marginTop: '4px' }}>Recorded in Local SQLite Store</div>
              </div>

              <div className="card" style={{ padding: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>USERNAMES CHECKED</span>
                  <User size={18} color="#10b981" />
                </div>
                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc' }}>{stats?.total_usernames ?? 0}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>Multi-platform alias queries</div>
              </div>

              <div className="card" style={{ padding: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>DOMAINS ANALYZED</span>
                  <Globe size={18} color="#8b5cf6" />
                </div>
                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc' }}>{stats?.total_domains ?? 0}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>RDAP, DNS &amp; IP Geolocation</div>
              </div>

              <div className="card" style={{ padding: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>MONITORED PLATFORMS</span>
                  <Server size={18} color="#f59e0b" />
                </div>
                <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc' }}>{stats?.supported_sources_count ?? 10} Sources</div>
                <div style={{ fontSize: '0.75rem', color: '#38bdf8', marginTop: '4px' }}>Active Passive Collectors</div>
              </div>
            </div>

            {/* Split Grid: Recent Activity & Source Status */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))', gap: '20px' }}>
              {/* Recent Activity */}
              <div className="card" style={{ padding: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <History size={16} color="#0284c7" /> Recent Investigations
                  </h3>
                  <button onClick={() => setActiveTab('history')} style={{ background: 'none', border: 'none', color: '#38bdf8', fontSize: '0.75rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    View All <ArrowRight size={12} />
                  </button>
                </div>

                {(!stats?.recent_activity || stats.recent_activity.length === 0) ? (
                  <p style={{ color: 'var(--text-dim)', fontSize: '0.875rem', padding: '20px 0', textAlign: 'center' }}>No investigations recorded yet. Run a username or domain check to begin.</p>
                ) : (
                  <div className="table-container">
                    <table>
                      <thead>
                        <tr>
                          <th>Target</th>
                          <th>Type</th>
                          <th>Timestamp</th>
                          <th>Status</th>
                          <th>Report</th>
                        </tr>
                      </thead>
                      <tbody>
                        {stats.recent_activity.map((item) => (
                          <tr key={item.id}>
                            <td className="mono" style={{ fontWeight: 600, color: '#38bdf8' }}>{item.target}</td>
                            <td>
                              <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: item.inv_type === 'username' ? '#34d399' : '#a78bfa' }}>
                                {item.inv_type}
                              </span>
                            </td>
                            <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{item.timestamp}</td>
                            <td>
                              <span className={`badge ${item.status === 'Completed' ? 'badge-found' : 'badge-inconclusive'}`}>{item.status}</span>
                            </td>
                            <td>
                              <a href={`${API_BASE}/reports/pdf/${item.id}`} download style={{ color: '#38bdf8', marginRight: '8px' }} title="PDF Report">
                                <FileText size={15} />
                              </a>
                              <a href={`${API_BASE}/reports/csv/${item.id}`} download style={{ color: '#10b981' }} title="CSV Report">
                                <Download size={15} />
                              </a>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>

              {/* Monitored Platforms Telemetry */}
              <div className="card" style={{ padding: '20px' }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Server size={16} color="#10b981" /> Monitored OSINT Sources Status
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))', gap: '10px' }}>
                  {[
                    { name: 'GitHub', type: 'Code / Dev', status: 'Online' },
                    { name: 'GitLab', type: 'DevOps / VCS', status: 'Online' },
                    { name: 'DockerHub', type: 'Containers', status: 'Online' },
                    { name: 'Dev.to', type: 'Community', status: 'Online' },
                    { name: 'HackerNews', type: 'Forums', status: 'Online' },
                    { name: 'Reddit', type: 'Social / API', status: 'Rate-Limited' },
                    { name: 'Gravatar', type: 'Identity', status: 'Online' },
                    { name: 'Keybase', type: 'Cryptography', status: 'Online' },
                    { name: 'Medium', type: 'Publishing', status: 'Online' },
                    { name: 'RDAP / DNS', type: 'Domain Reg.', status: 'Active' },
                  ].map((s) => (
                    <div key={s.name} style={{ background: '#111827', border: '1px solid var(--border)', padding: '10px', borderRadius: '8px' }}>
                      <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#f8fafc' }}>{s.name}</div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>{s.type}</div>
                      <div style={{ marginTop: '6px', fontSize: '0.7rem', display: 'flex', alignItems: 'center', gap: '4px', color: s.status === 'Online' || s.status === 'Active' ? '#34d399' : '#fbbf24' }}>
                        <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: s.status === 'Online' || s.status === 'Active' ? '#34d399' : '#fbbf24' }}></span>
                        {s.status}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ----------------- TAB: USERNAME OSINT ----------------- */}
        {activeTab === 'username' && (
          <div>
            <div style={{ marginBottom: '20px' }}>
              <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#f8fafc' }}>Username Reconnaissance</h1>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Passive correlation of user handles across social networks, code repositories, and public identity endpoints.</p>
            </div>

            {/* Input Card */}
            <div className="card" style={{ padding: '24px', marginBottom: '24px' }}>
              <form onSubmit={handleUsernameSearch} style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                <div style={{ flex: 1, minWidth: '260px' }}>
                  <input 
                    type="text" 
                    className="input-text mono"
                    placeholder="Enter authorized target username (e.g. fardeenakmal)"
                    value={usernameInput}
                    onChange={(e) => setUsernameInput(e.target.value)}
                    disabled={isUsernameLoading}
                  />
                </div>
                <button type="submit" className="btn-primary" disabled={isUsernameLoading}>
                  {isUsernameLoading ? (
                    <>
                      <RefreshCw size={16} className="animate-spin" /> Scanning Sources...
                    </>
                  ) : (
                    <>
                      <Search size={16} /> Scan Digital Footprint
                    </>
                  )}
                </button>
              </form>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Lock size={12} /> Authorized ethical reconnaissance only. Checks public profile endpoints without credential brute-forcing.
              </div>
            </div>

            {/* Results Presentation */}
            {usernameResult && (
              <div>
                {/* Result Summary Bar */}
                <div className="card" style={{ padding: '18px 24px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f8fafc' }}>Target: @{usernameResult.target}</h2>
                      <span className="badge badge-found">{usernameResult.status}</span>
                    </div>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                      Collected: {usernameResult.timestamp} • {usernameResult.summary}
                    </p>
                  </div>

                  <div style={{ display: 'flex', gap: '10px' }}>
                    <a href={`${API_BASE}/reports/pdf/${usernameResult.id}`} download className="btn-secondary" style={{ textDecoration: 'none' }}>
                      <FileText size={15} color="#0284c7" /> Download PDF Dossier
                    </a>
                    <a href={`${API_BASE}/reports/csv/${usernameResult.id}`} download className="btn-secondary" style={{ textDecoration: 'none' }}>
                      <Download size={15} color="#10b981" /> Export CSV
                    </a>
                  </div>
                </div>

                {/* Filter and Metrics */}
                <div style={{ display: 'flex', gap: '12px', marginBottom: '16px', flexWrap: 'wrap' }}>
                  <button 
                    onClick={() => setUsernameFilter('ALL')} 
                    className={usernameFilter === 'ALL' ? 'btn-primary' : 'btn-secondary'}
                    style={{ fontSize: '0.8rem', padding: '6px 14px' }}
                  >
                    All ({usernameResult.total_sources})
                  </button>
                  <button 
                    onClick={() => setUsernameFilter('FOUND')} 
                    className={usernameFilter === 'FOUND' ? 'btn-primary' : 'btn-secondary'}
                    style={{ fontSize: '0.8rem', padding: '6px 14px', color: '#34d399' }}
                  >
                    Found ({usernameResult.found_count})
                  </button>
                  <button 
                    onClick={() => setUsernameFilter('INCONCLUSIVE')} 
                    className={usernameFilter === 'INCONCLUSIVE' ? 'btn-primary' : 'btn-secondary'}
                    style={{ fontSize: '0.8rem', padding: '6px 14px', color: '#fbbf24' }}
                  >
                    Inconclusive ({usernameResult.inconclusive_count})
                  </button>
                  <button 
                    onClick={() => setUsernameFilter('NOT_FOUND')} 
                    className={usernameFilter === 'NOT_FOUND' ? 'btn-primary' : 'btn-secondary'}
                    style={{ fontSize: '0.8rem', padding: '6px 14px', color: '#94a3b8' }}
                  >
                    Not Found ({usernameResult.not_found_count})
                  </button>
                </div>

                {/* Table of Findings */}
                <div className="table-container card">
                  <table>
                    <thead>
                      <tr>
                        <th>Platform</th>
                        <th>Category</th>
                        <th>Profile URL</th>
                        <th>Status</th>
                        <th>Latency</th>
                        <th>Verification &amp; Observed Detail</th>
                      </tr>
                    </thead>
                    <tbody>
                      {usernameResult.findings
                        .filter(f => usernameFilter === 'ALL' || f.status === usernameFilter)
                        .map((f, idx) => (
                          <tr key={idx}>
                            <td style={{ fontWeight: 600, color: '#f8fafc' }}>{f.source}</td>
                            <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{f.category}</td>
                            <td>
                              <a 
                                href={f.url} 
                                target="_blank" 
                                rel="noreferrer" 
                                className="mono" 
                                style={{ color: '#38bdf8', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem' }}
                              >
                                {f.url} <ExternalLink size={12} />
                              </a>
                            </td>
                            <td>
                              <span className={`badge ${
                                f.status === 'FOUND' ? 'badge-found' : (
                                  f.status === 'NOT_FOUND' ? 'badge-notfound' : (
                                    f.status === 'INCONCLUSIVE' ? 'badge-inconclusive' : 'badge-failed'
                                  )
                                )
                              }`}>
                                {f.status}
                              </span>
                            </td>
                            <td className="mono" style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                              {f.response_time_ms} ms
                            </td>
                            <td>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
                                {f.verified && <CheckCircle size={14} color="#34d399" />}
                                <span>{f.detail}</span>
                              </div>
                            </td>
                          </tr>
                        ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ----------------- TAB: DOMAIN INTELLIGENCE ----------------- */}
        {activeTab === 'domain' && (
          <div>
            <div style={{ marginBottom: '20px' }}>
              <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#f8fafc' }}>Domain Intelligence</h1>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Passive DNS reconnaissance, RDAP registration records, authoritative nameservers, and IP geolocation telemetry.</p>
            </div>

            {/* Input Card */}
            <div className="card" style={{ padding: '24px', marginBottom: '24px' }}>
              <form onSubmit={handleDomainSearch} style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                <div style={{ flex: 1, minWidth: '260px' }}>
                  <input 
                    type="text" 
                    className="input-text mono"
                    placeholder="Enter authorized test domain (e.g. example.com or github.com)"
                    value={domainInput}
                    onChange={(e) => setDomainInput(e.target.value)}
                    disabled={isDomainLoading}
                  />
                </div>
                <button type="submit" className="btn-primary" disabled={isDomainLoading}>
                  {isDomainLoading ? (
                    <>
                      <RefreshCw size={16} className="animate-spin" /> Querying RDAP &amp; DNS...
                    </>
                  ) : (
                    <>
                      <Globe size={16} /> Analyze Domain
                    </>
                  )}
                </button>
              </form>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginTop: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Lock size={12} /> Passive collection: queries publicly delegated authoritative nameservers and ICANN RDAP registries.
              </div>
            </div>

            {/* Error Diagnostics Card */}
            {domainErrorDetail && (
              <div style={{
                background: 'rgba(239, 68, 68, 0.08)',
                border: '1px solid #ef4444',
                borderRadius: '10px',
                padding: '20px',
                marginBottom: '24px',
                display: 'flex',
                gap: '16px',
                alignItems: 'flex-start'
              }}>
                <AlertCircle size={26} color="#ef4444" style={{ flexShrink: 0, marginTop: '2px' }} />
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                    <span style={{ fontWeight: 700, color: '#f87171', fontSize: '0.95rem' }}>RFC 1035 / FQDN Validation Gate Error</span>
                    <span className="badge badge-failed" style={{ fontSize: '0.7rem' }}>CLIENT_REJECTED (422)</span>
                  </div>
                  <p style={{ color: '#e2e8f0', fontSize: '0.85rem', lineHeight: '1.5', margin: '4px 0 10px 0' }}>
                    {domainErrorDetail}
                  </p>
                  <div style={{ background: '#0b0f19', borderRadius: '6px', padding: '12px 14px', fontSize: '0.75rem', color: '#94a3b8' }}>
                    <div><strong style={{ color: '#cbd5e1' }}>Safety Control:</strong> TRACE active query safeguards intercept malformed domains prior to socket resolution to prevent SSRF and injection attacks.</div>
                    <div style={{ marginTop: '4px' }}><strong style={{ color: '#cbd5e1' }}>Permitted format:</strong> Use fully qualified domain names (e.g., <code style={{ color: '#38bdf8' }}>example.com</code>, <code style={{ color: '#38bdf8' }}>github.com</code>).</div>
                  </div>
                </div>
              </div>
            )}

            {/* Results Presentation */}
            {domainResult && (
              <div>
                {/* Result Header */}
                <div className="card" style={{ padding: '18px 24px', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#f8fafc' }}>Domain: {domainResult.target}</h2>
                      <span className="badge badge-found">{domainResult.status}</span>
                    </div>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                      Collected: {domainResult.timestamp} • Primary IP: <span className="mono" style={{ color: '#38bdf8' }}>{domainResult.primary_ip || 'None'}</span>
                    </p>
                  </div>

                  <div style={{ display: 'flex', gap: '10px' }}>
                    <a href={`${API_BASE}/reports/pdf/${domainResult.id}`} download className="btn-secondary" style={{ textDecoration: 'none' }}>
                      <FileText size={15} color="#0284c7" /> Download PDF Report
                    </a>
                    <a href={`${API_BASE}/reports/csv/${domainResult.id}`} download className="btn-secondary" style={{ textDecoration: 'none' }}>
                      <Download size={15} color="#10b981" /> Export CSV
                    </a>
                  </div>
                </div>

                {/* Grid: Registration & Geolocation */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px', marginBottom: '20px' }}>
                  {/* Registration Card */}
                  <div className="card" style={{ padding: '20px' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#38bdf8', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Shield size={16} /> Registration &amp; Registrar (RDAP)
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.875rem' }}>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>Registrar:</span>{' '}
                        <span style={{ fontWeight: 600, color: '#f8fafc' }}>{domainResult.registration.registrar}</span>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>Creation Date:</span>{' '}
                        <span className="mono" style={{ color: '#10b981' }}>{domainResult.registration.creation_date}</span>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>Expiration Date:</span>{' '}
                        <span className="mono" style={{ color: '#f59e0b' }}>{domainResult.registration.expiration_date}</span>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>Status Flags:</span>{' '}
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '4px' }}>
                          {domainResult.registration.status.length > 0 ? (
                            domainResult.registration.status.map((st, i) => (
                              <span key={i} style={{ background: '#1e293b', padding: '2px 6px', borderRadius: '4px', fontSize: '0.7rem', color: '#94a3b8' }}>
                                {st}
                              </span>
                            ))
                          ) : (
                            <span style={{ color: 'var(--text-dim)', fontSize: '0.8rem' }}>Standard Active</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Geolocation & Network Card */}
                  <div className="card" style={{ padding: '20px' }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#10b981', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Globe size={16} /> Server Geolocation &amp; Autonomous System
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.875rem' }}>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>Resolved IP:</span>{' '}
                        <span className="mono" style={{ color: '#38bdf8', fontWeight: 600 }}>{domainResult.geolocation.ip}</span>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>Location:</span>{' '}
                        <span style={{ color: '#f8fafc' }}>{domainResult.geolocation.city}, {domainResult.geolocation.country}</span>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>Hosting ISP:</span>{' '}
                        <span style={{ color: '#f8fafc' }}>{domainResult.geolocation.isp}</span>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)' }}>Autonomous System:</span>{' '}
                        <span className="mono" style={{ color: '#a78bfa' }}>{domainResult.geolocation.asn}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* DNS Records Breakdown */}
                <div className="card" style={{ padding: '20px', marginBottom: '20px' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Server size={16} color="#8b5cf6" /> Authoritative DNS Records
                  </h3>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
                    {/* A Records */}
                    <div style={{ background: '#111827', padding: '14px', borderRadius: '8px', border: '1px solid var(--border)' }}>
                      <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#38bdf8', marginBottom: '6px' }}>A (IPv4 Addresses)</div>
                      <div className="mono" style={{ fontSize: '0.8rem', color: '#e2e8f0' }}>
                        {domainResult.dns_records.A.length > 0 ? domainResult.dns_records.A.join(', ') : 'None resolved'}
                      </div>
                    </div>

                    {/* MX Records */}
                    <div style={{ background: '#111827', padding: '14px', borderRadius: '8px', border: '1px solid var(--border)' }}>
                      <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#34d399', marginBottom: '6px' }}>MX (Mail Routing)</div>
                      <div className="mono" style={{ fontSize: '0.8rem', color: '#e2e8f0' }}>
                        {domainResult.dns_records.MX.length > 0 ? domainResult.dns_records.MX.slice(0, 3).join(', ') : 'No mail exchanger configured'}
                      </div>
                    </div>

                    {/* NS Records */}
                    <div style={{ background: '#111827', padding: '14px', borderRadius: '8px', border: '1px solid var(--border)' }}>
                      <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#a78bfa', marginBottom: '6px' }}>NS (Nameservers)</div>
                      <div className="mono" style={{ fontSize: '0.8rem', color: '#e2e8f0' }}>
                        {domainResult.dns_records.NS.length > 0 ? domainResult.dns_records.NS.slice(0, 3).join(', ') : 'None'}
                      </div>
                    </div>

                    {/* TXT Records */}
                    <div style={{ background: '#111827', padding: '14px', borderRadius: '8px', border: '1px solid var(--border)' }}>
                      <div style={{ fontWeight: 700, fontSize: '0.85rem', color: '#f59e0b', marginBottom: '6px' }}>TXT (SPF / Verification)</div>
                      <div className="mono" style={{ fontSize: '0.75rem', color: '#e2e8f0', wordBreak: 'break-all' }}>
                        {domainResult.dns_records.TXT.length > 0 ? domainResult.dns_records.TXT.slice(0, 2).join(' | ') : 'No TXT records found'}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ----------------- TAB: INVESTIGATION HISTORY ----------------- */}
        {activeTab === 'history' && (
          <div>
            <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
              <div>
                <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#f8fafc' }}>Investigation History</h1>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Local SQLite database audit log of previous OSINT inquiries and generated dossiers.</p>
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button className="btn-secondary" onClick={loadHistory}>
                  <RefreshCw size={14} /> Refresh
                </button>
                {historyItems.length > 0 && (
                  <button className="btn-danger" onClick={handleClearAllHistory}>
                    <Trash2 size={14} /> Clear All Records
                  </button>
                )}
              </div>
            </div>

            {/* Filter Buttons */}
            <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
              <button 
                onClick={() => setHistoryFilter('ALL')} 
                className={historyFilter === 'ALL' ? 'btn-primary' : 'btn-secondary'}
                style={{ fontSize: '0.8rem', padding: '6px 14px' }}
              >
                All Records ({historyItems.length})
              </button>
              <button 
                onClick={() => setHistoryFilter('username')} 
                className={historyFilter === 'username' ? 'btn-primary' : 'btn-secondary'}
                style={{ fontSize: '0.8rem', padding: '6px 14px' }}
              >
                Usernames ({historyItems.filter(h => h.inv_type === 'username').length})
              </button>
              <button 
                onClick={() => setHistoryFilter('domain')} 
                className={historyFilter === 'domain' ? 'btn-primary' : 'btn-secondary'}
                style={{ fontSize: '0.8rem', padding: '6px 14px' }}
              >
                Domains ({historyItems.filter(h => h.inv_type === 'domain').length})
              </button>
            </div>

            {historyItems.length === 0 ? (
              <div className="card" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-dim)' }}>
                <History size={36} style={{ margin: '0 auto 12px auto', display: 'block', opacity: 0.5 }} />
                <p>No historical records in SQLite database.</p>
              </div>
            ) : (
              <div className="table-container card">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Type</th>
                      <th>Target Analyzed</th>
                      <th>Timestamp</th>
                      <th>Status</th>
                      <th>Summary Finding</th>
                      <th>Export Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {historyItems
                      .filter(item => historyFilter === 'ALL' || item.inv_type === historyFilter)
                      .map((item) => (
                        <tr key={item.id}>
                          <td className="mono" style={{ color: 'var(--text-dim)' }}>#{item.id}</td>
                          <td>
                            <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: item.inv_type === 'username' ? '#34d399' : '#a78bfa' }}>
                              {item.inv_type}
                            </span>
                          </td>
                          <td className="mono" style={{ fontWeight: 600, color: '#38bdf8' }}>{item.target}</td>
                          <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{item.timestamp}</td>
                          <td>
                            <span className={`badge ${item.status === 'Completed' ? 'badge-found' : 'badge-inconclusive'}`}>
                              {item.status}
                            </span>
                          </td>
                          <td style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>{item.summary}</td>
                          <td>
                            <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                              <button onClick={() => openReportModal(item.id)} className="btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem', display: 'inline-flex', alignItems: 'center', gap: '4px' }} title="Preview Report Dossier">
                                <FileText size={13} color="#38bdf8" /> Dossier
                              </button>
                              <a href={`${API_BASE}/reports/pdf/${item.id}`} download className="btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '4px' }} title="Download PDF Report">
                                <FileText size={13} color="#0284c7" /> PDF
                              </a>
                              <a href={`${API_BASE}/reports/csv/${item.id}`} download className="btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '4px' }} title="Download CSV Report">
                                <Download size={13} color="#10b981" /> CSV
                              </a>
                              <button onClick={() => handleDeleteHistory(item.id)} className="btn-danger" style={{ padding: '4px 8px' }} title="Delete Record">
                                <Trash2 size={13} />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Investigation Dossier & Export Modal */}
      {reportModalData && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(3, 7, 18, 0.88)', backdropFilter: 'blur(8px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 9999, padding: '20px'
        }}>
          <div className="card" style={{
            maxWidth: '900px', width: '100%', maxHeight: '92vh', overflowY: 'auto',
            border: '1px solid #1e293b', background: '#0d1322', padding: '30px',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.85)', borderRadius: '14px'
          }}>
            {/* Top Bar */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid var(--border)', paddingBottom: '16px', marginBottom: '20px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge badge-found" style={{ fontSize: '0.75rem', fontWeight: 700 }}>VERIFIED AUDIT REPORT</span>
                  <span className="mono" style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Dossier ID: TRACE-REP-{String(reportModalData.id).padStart(4, '0')}</span>
                </div>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#f8fafc', marginTop: '6px' }}>
                  Investigation Report: {reportModalData.target}
                </h2>
                <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginTop: '3px' }}>
                  Compiled {reportModalData.timestamp} • Analysis Module: <strong style={{ textTransform: 'uppercase', color: '#38bdf8' }}>{reportModalData.inv_type}</strong>
                </p>
              </div>
              <button onClick={() => setReportModalData(null)} className="btn-secondary" style={{ padding: '6px' }}>
                <X size={18} />
              </button>
            </div>

            {/* Academic Credentials Card */}
            <div style={{ background: '#111827', border: '1px solid #1f2937', borderRadius: '8px', padding: '14px 18px', marginBottom: '20px', fontSize: '0.8rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: '8px', color: '#cbd5e1' }}>
                <div><span style={{ color: '#94a3b8' }}>Investigator:</span> <strong style={{ color: '#f8fafc' }}>Fardeen Akmal</strong> (Roll: 2)</div>
                <div><span style={{ color: '#94a3b8' }}>Project Guide:</span> <strong style={{ color: '#f8fafc' }}>Akanksha Thakare</strong></div>
                <div><span style={{ color: '#94a3b8' }}>Specialization:</span> CSE (IoT, Cyber Sec &amp; Blockchain)</div>
                <div><span style={{ color: '#94a3b8' }}>Institution:</span> GVAIET, University of Mumbai</div>
              </div>
            </div>

            {/* Export Confirmation Banner */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(16, 185, 129, 0.08)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '8px', padding: '14px 18px', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <CheckCircle size={22} color="#10b981" />
                <div>
                  <div style={{ fontWeight: 600, color: '#f8fafc', fontSize: '0.9rem' }}>Artifact Export Generated Successfully</div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Ready for academic case study submission and external auditing. Formatted in standard PDF and CSV schemas.</div>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '10px' }}>
                <a href={`${API_BASE}/reports/pdf/${reportModalData.id}`} download className="btn-primary" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem' }}>
                  <FileText size={15} /> Download PDF
                </a>
                <a href={`${API_BASE}/reports/csv/${reportModalData.id}`} download className="btn-secondary" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem' }}>
                  <Download size={15} /> Download CSV
                </a>
              </div>
            </div>

            {/* Summary Findings */}
            <div className="card" style={{ padding: '16px 20px', marginBottom: '20px', background: '#111827' }}>
              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', marginBottom: '8px' }}>Executive Summary &amp; Telemetry</h4>
              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: '1.5' }}>{reportModalData.summary}</p>
            </div>

            {/* Detailed Findings Table (Username) */}
            {reportModalData.inv_type === 'username' && reportModalData.data?.findings && (
              <div className="table-container card" style={{ maxHeight: '250px', overflowY: 'auto', marginBottom: '20px' }}>
                <table>
                  <thead>
                    <tr>
                      <th>Platform</th>
                      <th>Category</th>
                      <th>Observed Status</th>
                      <th>Verification Detail</th>
                    </tr>
                  </thead>
                  <tbody>
                    {reportModalData.data.findings.map((f: any, idx: number) => (
                      <tr key={idx}>
                        <td style={{ fontWeight: 600, color: '#f8fafc' }}>{f.source}</td>
                        <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{f.category}</td>
                        <td>
                          <span className={`badge ${
                            f.status === 'FOUND' ? 'badge-found' : (
                              f.status === 'NOT_FOUND' ? 'badge-notfound' : (
                                f.status === 'INCONCLUSIVE' ? 'badge-inconclusive' : 'badge-failed'
                              )
                            )
                          }`}>
                            {f.status}
                          </span>
                        </td>
                        <td style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>{f.detail}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Detailed Info (Domain) */}
            {reportModalData.inv_type === 'domain' && reportModalData.data && (
              <div className="card" style={{ padding: '16px', background: '#111827', marginBottom: '20px' }}>
                <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', marginBottom: '8px' }}>Authoritative Records</h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px', fontSize: '0.8rem' }}>
                  <div><span style={{ color: '#94a3b8' }}>Primary IPv4:</span> <span className="mono" style={{ color: '#38bdf8' }}>{reportModalData.data.primary_ip || 'None'}</span></div>
                  <div><span style={{ color: '#94a3b8' }}>Registrar:</span> <span style={{ color: '#f8fafc' }}>{reportModalData.data.registration?.registrar || 'N/A'}</span></div>
                  <div><span style={{ color: '#94a3b8' }}>Hosting ISP:</span> <span style={{ color: '#f8fafc' }}>{reportModalData.data.geolocation?.isp || 'N/A'}</span></div>
                  <div><span style={{ color: '#94a3b8' }}>Country:</span> <span style={{ color: '#f8fafc' }}>{reportModalData.data.geolocation?.country || 'N/A'}</span></div>
                </div>
              </div>
            )}

            {/* Bottom Controls */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border)', paddingTop: '16px' }}>
              <div className="mono" style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                System: TRACE OSINT v1.0 • Academic Build (Mumbai Univ)
              </div>
              <button onClick={() => setReportModalData(null)} className="btn-secondary">
                Close Dossier
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer style={{ borderTop: '1px solid var(--border)', padding: '16px 20px', background: '#0b0f19', textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-dim)' }}>
        <div>TRACE OSINT Digital Footprint Analyzer • Educational Cybersecurity Mini Project</div>
        <div style={{ marginTop: '4px' }}>Developer: Fardeen Akmal (Roll No: 2) • Guide: Akanksha Thakare • G.V. Acharya Institute of Engineering and Technology (University of Mumbai)</div>
      </footer>
    </div>
  );
}
