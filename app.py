import { useState, useEffect, useCallback, useReducer, createContext, useContext } from "react";

// ─────────────────────────────────────────────
// DESIGN TOKENS
// ─────────────────────────────────────────────
const colors = {
  navy: "#0B1437",
  navyMid: "#111D4A",
  navyLight: "#1A2B6B",
  electric: "#4361EE",
  electricHover: "#3451D1",
  electricLight: "#EEF2FF",
  teal: "#06D6A0",
  tealLight: "#ECFDF5",
  amber: "#F59E0B",
  amberLight: "#FFFBEB",
  rose: "#F43F5E",
  roseLight: "#FFF1F2",
  purple: "#7C3AED",
  purpleLight: "#F5F3FF",
  slate50: "#F8FAFC",
  slate100: "#F1F5F9",
  slate200: "#E2E8F0",
  slate300: "#CBD5E1",
  slate400: "#94A3B8",
  slate500: "#64748B",
  slate600: "#475569",
  slate700: "#334155",
  slate800: "#1E293B",
  slate900: "#0F172A",
  white: "#FFFFFF",
};

// ─────────────────────────────────────────────
// CONTEXTS
// ─────────────────────────────────────────────
const AppContext = createContext(null);

// ─────────────────────────────────────────────
// MOCK DATA ENGINE
// ─────────────────────────────────────────────
const generateId = () => Math.random().toString(36).slice(2, 10);
const now = () => new Date().toISOString();
const daysAgo = (n) => new Date(Date.now() - n * 86400000).toISOString();

const MOCK_ORG = {
  id: "org_1",
  name: "Nexus Retail India Pvt Ltd",
  domain: "nexusretail.in",
  plan: "Business",
  trustScore: 78,
  websites: 4,
  members: 12,
};

const MOCK_WEBSITES = [
  { id: "w1", url: "https://nexusretail.in", name: "Main Store", status: "healthy", trustScore: 82, lastScan: daysAgo(1), monitoringEnabled: true, environment: "Production" },
  { id: "w2", url: "https://app.nexusretail.in", name: "Customer Portal", status: "warning", trustScore: 67, lastScan: daysAgo(3), monitoringEnabled: true, environment: "Production" },
  { id: "w3", url: "https://blog.nexusretail.in", name: "Blog", status: "healthy", trustScore: 91, lastScan: daysAgo(7), monitoringEnabled: false, environment: "Production" },
  { id: "w4", url: "https://staging.nexusretail.in", name: "Staging", status: "critical", trustScore: 44, lastScan: daysAgo(14), monitoringEnabled: false, environment: "Staging" },
];

const MOCK_ISSUES = [
  { id: generateId(), severity: "critical", category: "Privacy", title: "No cookie consent banner", description: "The website collects cookies without obtaining prior consent from users.", evidence: "No CMP detected on homepage", businessImpact: "Risk of regulatory fines up to ₹250 crore under DPDP Act 2023.", legalImpact: "Non-compliant with DPDP Act Section 6, GDPR Article 7.", recommendation: "Implement a DPDP-compliant cookie consent management platform with granular category controls.", effortHours: 8, status: "open", assignee: "Priya Sharma", website: "Customer Portal", createdAt: daysAgo(5) },
  { id: generateId(), severity: "critical", category: "Security", title: "Missing Content Security Policy header", description: "No CSP header detected, leaving site vulnerable to XSS attacks.", evidence: "HTTP response headers analysis", businessImpact: "XSS attacks could expose customer PII and payment data.", legalImpact: "Data breach liability under IT Act 2000.", recommendation: "Implement strict CSP: default-src 'self'; script-src 'self' 'nonce-xxx'", effortHours: 4, status: "open", assignee: null, website: "Customer Portal", createdAt: daysAgo(3) },
  { id: generateId(), severity: "high", category: "Privacy", title: "Privacy Policy not linked from footer", description: "Privacy Policy exists but is not linked from key touchpoints including footer and forms.", evidence: "Crawl of all 47 pages", businessImpact: "Reduced user trust and potential DPDP violation.", legalImpact: "Non-compliant with DPDP Act Section 5.", recommendation: "Add Privacy Policy link to footer, checkout forms, and all data collection points.", effortHours: 2, status: "in_progress", assignee: "Arjun Mehta", website: "Main Store", createdAt: daysAgo(8) },
  { id: generateId(), severity: "high", category: "Security", title: "TLS 1.0 still enabled", description: "Server accepts TLS 1.0 connections which have known vulnerabilities.", evidence: "SSL Labs scan result: B grade", businessImpact: "MITM attack risk on customer sessions.", legalImpact: "PCI-DSS non-compliance if processing payments.", recommendation: "Disable TLS 1.0 and 1.1. Enable only TLS 1.2 and 1.3.", effortHours: 1, status: "open", assignee: null, website: "Customer Portal", createdAt: daysAgo(2) },
  { id: generateId(), severity: "medium", category: "Accessibility", title: "41 images missing alt text", description: "Product images across 12 category pages lack descriptive alt attributes.", evidence: "WCAG 2.1 Level AA automated audit", businessImpact: "Excludes visually impaired customers, potential ADA liability.", legalImpact: "WCAG 2.1 AA non-compliance.", recommendation: "Add descriptive alt text to all product images. Use empty alt='' for decorative images.", effortHours: 6, status: "resolved", assignee: "Kavitha Nair", website: "Main Store", createdAt: daysAgo(12) },
  { id: generateId(), severity: "medium", category: "Performance", title: "LCP exceeds 4 seconds on mobile", description: "Largest Contentful Paint is 4.2s on 3G, far above the 2.5s threshold.", evidence: "Core Web Vitals: CrUX data, PageSpeed score 48", businessImpact: "Estimated 15% checkout abandonment attributable to slow load.", legalImpact: null, recommendation: "Optimize hero image delivery with next-gen formats and lazy loading.", effortHours: 12, status: "open", assignee: "Arjun Mehta", website: "Main Store", createdAt: daysAgo(6) },
];

const MOCK_DSARS = [
  { id: generateId(), requesterName: "Meera Iyer", requesterEmail: "meera.iyer@gmail.com", requestType: "Access", status: "in_review", submittedAt: daysAgo(12), dueAt: new Date(Date.now() + 18 * 86400000).toISOString(), assignee: "Priya Sharma" },
  { id: generateId(), requesterName: "Rahul Singh", requesterEmail: "rahul.s@company.com", requestType: "Delete", status: "pending_verification", submittedAt: daysAgo(5), dueAt: new Date(Date.now() + 25 * 86400000).toISOString(), assignee: null },
  { id: generateId(), requesterName: "Anjali Bhat", requesterEmail: "anjali@personal.in", requestType: "Portability", status: "completed", submittedAt: daysAgo(30), dueAt: daysAgo(5), assignee: "Arjun Mehta" },
  { id: generateId(), requesterName: "Vikram Rao", requesterEmail: "v.rao@business.in", requestType: "Rectification", status: "submitted", submittedAt: daysAgo(2), dueAt: new Date(Date.now() + 28 * 86400000).toISOString(), assignee: null },
];

const MOCK_AUDIT_LOGS = [
  { id: generateId(), user: "admin@nexusretail.in", action: "SCAN_COMPLETED", entity: "Website", entityId: "w2", ip: "49.204.11.2", browser: "Chrome 124 / macOS", timestamp: daysAgo(0.1) },
  { id: generateId(), user: "priya@nexusretail.in", action: "DSAR_STATUS_UPDATED", entity: "DSAR", entityId: "req_001", ip: "49.204.11.5", browser: "Safari 17 / iOS", timestamp: daysAgo(0.3) },
  { id: generateId(), user: "arjun@nexusretail.in", action: "ISSUE_ASSIGNED", entity: "Issue", entityId: "iss_004", ip: "103.1.42.9", browser: "Firefox 125 / Windows", timestamp: daysAgo(0.5) },
  { id: generateId(), user: "admin@nexusretail.in", action: "CONSENT_RECORD_EXPORTED", entity: "Consent", entityId: null, ip: "49.204.11.2", browser: "Chrome 124 / macOS", timestamp: daysAgo(1) },
  { id: generateId(), user: "kavitha@nexusretail.in", action: "ISSUE_RESOLVED", entity: "Issue", entityId: "iss_005", ip: "103.1.45.22", browser: "Edge 124 / Windows", timestamp: daysAgo(1.5) },
  { id: generateId(), user: "priya@nexusretail.in", action: "POLICY_PUBLISHED", entity: "PrivacyPolicy", entityId: "pol_003", ip: "49.204.11.5", browser: "Safari 17 / iOS", timestamp: daysAgo(3) },
];

const MOCK_CONSENTS = [
  { id: generateId(), email: "customer1@example.com", purpose: "Marketing", granted: true, grantedAt: daysAgo(10), ip: "122.161.44.1", channel: "Web" },
  { id: generateId(), email: "customer2@example.com", purpose: "Analytics", granted: true, grantedAt: daysAgo(8), ip: "122.161.44.2", channel: "Web" },
  { id: generateId(), email: "customer3@example.com", purpose: "Marketing", granted: false, grantedAt: daysAgo(6), ip: "122.161.44.3", channel: "Mobile" },
  { id: generateId(), email: "customer4@example.com", purpose: "Newsletter", granted: true, grantedAt: daysAgo(4), ip: "122.161.44.4", channel: "Web" },
  { id: generateId(), email: "customer5@example.com", purpose: "Product Updates", granted: true, grantedAt: daysAgo(2), ip: "122.161.44.5", channel: "Email" },
];

// ─────────────────────────────────────────────
// STATE MANAGEMENT
// ─────────────────────────────────────────────
function appReducer(state, action) {
  switch (action.type) {
    case "SET_PAGE": return { ...state, currentPage: action.page, subPage: null };
    case "SET_SUBPAGE": return { ...state, subPage: action.subPage };
    case "ADD_TOAST": return { ...state, toasts: [...state.toasts, { id: generateId(), ...action.toast }] };
    case "REMOVE_TOAST": return { ...state, toasts: state.toasts.filter(t => t.id !== action.id) };
    case "START_SCAN": return { ...state, activeScan: { websiteId: action.websiteId, url: action.url, progress: 0, step: "Initializing scanner…" } };
    case "UPDATE_SCAN": return { ...state, activeScan: { ...state.activeScan, progress: action.progress, step: action.step } };
    case "COMPLETE_SCAN": return { ...state, activeScan: null, scanResults: action.results, currentPage: "scanner", subPage: "results" };
    case "SET_SELECTED_WEBSITE": return { ...state, selectedWebsite: action.websiteId };
    case "UPDATE_ISSUE": return {
      ...state,
      issues: state.issues.map(i => i.id === action.id ? { ...i, ...action.patch } : i)
    };
    case "ADD_DSAR": return { ...state, dsars: [action.dsar, ...state.dsars] };
    case "UPDATE_DSAR": return { ...state, dsars: state.dsars.map(d => d.id === action.id ? { ...d, ...action.patch } : d) };
    case "ADD_CONSENT": return { ...state, consents: [action.consent, ...state.consents] };
    case "ADD_AUDIT": return { ...state, auditLogs: [action.log, ...state.auditLogs] };
    case "SET_NOTIFICATION_READ": return {
      ...state,
      notifications: state.notifications.map(n => n.id === action.id ? { ...n, read: true } : n)
    };
    default: return state;
  }
}

const NOTIFICATIONS = [
  { id: "n1", type: "critical", title: "Critical security issue detected", body: "CSP header missing on Customer Portal", read: false, timestamp: daysAgo(0.2) },
  { id: "n2", type: "warning", title: "DSAR approaching deadline", body: "Meera Iyer's access request due in 18 days", read: false, timestamp: daysAgo(0.5) },
  { id: "n3", type: "info", title: "Scan completed", body: "nexusretail.in scored 82/100", read: true, timestamp: daysAgo(1) },
  { id: "n4", type: "success", title: "Issue resolved", body: "Alt text accessibility issue marked resolved", read: true, timestamp: daysAgo(1.5) },
];

function initState() {
  return {
    currentPage: "dashboard",
    subPage: null,
    toasts: [],
    activeScan: null,
    scanResults: null,
    selectedWebsite: MOCK_WEBSITES[0].id,
    issues: MOCK_ISSUES,
    dsars: MOCK_DSARS,
    consents: MOCK_CONSENTS,
    auditLogs: MOCK_AUDIT_LOGS,
    notifications: NOTIFICATIONS,
    sidebarCollapsed: false,
  };
}

// ─────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────
function relativeTime(iso) {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

function scoreColor(score) {
  if (score >= 80) return colors.teal;
  if (score >= 60) return colors.amber;
  return colors.rose;
}

function severityColor(sev) {
  const map = { critical: colors.rose, high: "#F97316", medium: colors.amber, low: colors.teal };
  return map[sev] || colors.slate400;
}

function statusColor(status) {
  const map = {
    open: colors.rose, in_progress: colors.amber, in_review: colors.amber,
    resolved: colors.teal, completed: colors.teal,
    submitted: colors.electric, pending_verification: colors.purple,
    healthy: colors.teal, warning: colors.amber, critical: colors.rose,
  };
  return map[status] || colors.slate400;
}

function statusLabel(status) {
  const map = {
    open: "Open", in_progress: "In Progress", in_review: "In Review",
    resolved: "Resolved", completed: "Completed",
    submitted: "Submitted", pending_verification: "Pending Verification",
    healthy: "Healthy", warning: "Warning", critical: "Critical",
  };
  return map[status] || status;
}

// ─────────────────────────────────────────────
// TOAST SYSTEM
// ─────────────────────────────────────────────
function ToastContainer({ toasts, dispatch }) {
  useEffect(() => {
    toasts.forEach(t => {
      const timer = setTimeout(() => dispatch({ type: "REMOVE_TOAST", id: t.id }), 4000);
      return () => clearTimeout(timer);
    });
  }, [toasts]);

  const typeStyles = {
    success: { bg: colors.tealLight, border: colors.teal, icon: "✓", color: "#065F46" },
    error: { bg: colors.roseLight, border: colors.rose, icon: "✕", color: "#9F1239" },
    warning: { bg: colors.amberLight, border: colors.amber, icon: "⚠", color: "#92400E" },
    info: { bg: colors.electricLight, border: colors.electric, icon: "ℹ", color: "#1E40AF" },
  };

  return (
    <div style={{ position: "fixed", bottom: 24, right: 24, zIndex: 9999, display: "flex", flexDirection: "column", gap: 8, maxWidth: 360 }}>
      {toasts.map(t => {
        const s = typeStyles[t.type] || typeStyles.info;
        return (
          <div key={t.id} style={{ background: s.bg, border: `1px solid ${s.border}`, borderRadius: 12, padding: "12px 16px", display: "flex", alignItems: "flex-start", gap: 10, boxShadow: "0 4px 24px rgba(0,0,0,0.12)", animation: "slideInRight 0.25s ease" }}>
            <span style={{ width: 20, height: 20, borderRadius: "50%", background: s.border, color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 700, flexShrink: 0, marginTop: 1 }}>{s.icon}</span>
            <div>
              <div style={{ fontWeight: 600, fontSize: 13, color: s.color }}>{t.title}</div>
              {t.body && <div style={{ fontSize: 12, color: s.color, opacity: 0.8, marginTop: 2 }}>{t.body}</div>}
            </div>
            <button onClick={() => dispatch({ type: "REMOVE_TOAST", id: t.id })} style={{ marginLeft: "auto", background: "none", border: "none", cursor: "pointer", color: s.color, opacity: 0.6, fontSize: 14, padding: 0, flexShrink: 0 }}>✕</button>
          </div>
        );
      })}
    </div>
  );
}

// ─────────────────────────────────────────────
// PRIMITIVE COMPONENTS
// ─────────────────────────────────────────────
function Badge({ children, color, bg }) {
  return (
    <span style={{ display: "inline-flex", alignItems: "center", padding: "3px 10px", borderRadius: 999, background: bg || `${color}18`, color: color || colors.slate600, fontSize: 11, fontWeight: 700, letterSpacing: 0.3, textTransform: "uppercase" }}>
      {children}
    </span>
  );
}

function ScorePill({ score, size = "sm" }) {
  const c = scoreColor(score);
  const sz = size === "lg" ? { fontSize: 28, fontWeight: 800, padding: "10px 20px" } : { fontSize: 13, fontWeight: 700, padding: "4px 12px" };
  return (
    <span style={{ background: `${c}18`, color: c, borderRadius: 999, display: "inline-flex", alignItems: "center", gap: 4, ...sz }}>
      {size === "lg" && <span style={{ width: 10, height: 10, borderRadius: "50%", background: c, display: "inline-block" }} />}
      {score}/100
    </span>
  );
}

function Button({ children, onClick, variant = "primary", size = "md", disabled = false, loading = false, icon, fullWidth = false }) {
  const variants = {
    primary: { bg: colors.electric, color: "white", border: "none", hoverBg: colors.electricHover },
    secondary: { bg: "transparent", color: colors.slate700, border: `1px solid ${colors.slate200}`, hoverBg: colors.slate50 },
    danger: { bg: "transparent", color: colors.rose, border: `1px solid ${colors.rose}26`, hoverBg: colors.roseLight },
    ghost: { bg: "transparent", color: colors.slate600, border: "none", hoverBg: colors.slate100 },
    teal: { bg: colors.teal, color: "white", border: "none", hoverBg: "#05C090" },
  };
  const sizes = {
    sm: { padding: "6px 12px", fontSize: 12, borderRadius: 8 },
    md: { padding: "9px 16px", fontSize: 13, borderRadius: 10 },
    lg: { padding: "12px 24px", fontSize: 14, borderRadius: 12 },
  };
  const v = variants[variant];
  const s = sizes[size];
  const [hovered, setHovered] = useState(false);

  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: "inline-flex", alignItems: "center", gap: 6, justifyContent: "center",
        background: hovered && !disabled ? v.hoverBg : v.bg,
        color: v.color, border: v.border,
        padding: s.padding, fontSize: s.fontSize, fontWeight: 600,
        borderRadius: s.borderRadius, cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.5 : 1, transition: "all 0.15s ease",
        width: fullWidth ? "100%" : undefined, fontFamily: "inherit",
        whiteSpace: "nowrap",
      }}
    >
      {loading ? <span style={{ width: 14, height: 14, border: `2px solid ${v.color}40`, borderTopColor: v.color, borderRadius: "50%", animation: "spin 0.8s linear infinite", display: "inline-block" }} /> : icon}
      {children}
    </button>
  );
}

function Card({ children, style, onClick, hoverable = false }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => hoverable && setHovered(true)}
      onMouseLeave={() => hoverable && setHovered(false)}
      style={{
        background: colors.white, borderRadius: 16, border: `1px solid ${colors.slate200}`,
        padding: 24, boxShadow: hovered && hoverable ? "0 8px 32px rgba(67,97,238,0.12)" : "0 1px 4px rgba(0,0,0,0.04)",
        transition: "box-shadow 0.2s, transform 0.2s",
        transform: hovered && hoverable ? "translateY(-2px)" : undefined,
        cursor: onClick ? "pointer" : undefined, ...style
      }}
    >
      {children}
    </div>
  );
}

function MetricCard({ label, value, delta, deltaType = "up", icon, color, sub }) {
  return (
    <Card style={{ padding: "20px 24px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <div style={{ fontSize: 12, color: colors.slate400, fontWeight: 600, textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 8 }}>{label}</div>
          <div style={{ fontSize: 28, fontWeight: 800, color: color || colors.slate900, lineHeight: 1 }}>{value}</div>
          {sub && <div style={{ fontSize: 11, color: colors.slate400, marginTop: 4 }}>{sub}</div>}
        </div>
        <div style={{ width: 44, height: 44, borderRadius: 12, background: `${color || colors.electric}15`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20 }}>
          {icon}
        </div>
      </div>
      {delta && (
        <div style={{ marginTop: 12, display: "flex", alignItems: "center", gap: 4, fontSize: 12, color: deltaType === "up" ? colors.teal : colors.rose, fontWeight: 600 }}>
          {deltaType === "up" ? "↑" : "↓"} {delta}
        </div>
      )}
    </Card>
  );
}

function EmptyState({ icon, title, description, action }) {
  return (
    <div style={{ textAlign: "center", padding: "60px 24px", display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
      <div style={{ fontSize: 48, marginBottom: 4 }}>{icon || "📂"}</div>
      <div style={{ fontSize: 18, fontWeight: 700, color: colors.slate900 }}>{title}</div>
      <div style={{ fontSize: 14, color: colors.slate400, maxWidth: 320, lineHeight: 1.6 }}>{description}</div>
      {action && <div style={{ marginTop: 8 }}>{action}</div>}
    </div>
  );
}

function SkeletonLoader({ lines = 3 }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} style={{ height: 16, background: `linear-gradient(90deg, ${colors.slate100} 25%, ${colors.slate200} 50%, ${colors.slate100} 75%)`, backgroundSize: "200% 100%", borderRadius: 8, width: i === lines - 1 ? "60%" : "100%", animation: "shimmer 1.5s infinite" }} />
      ))}
    </div>
  );
}

function Input({ label, value, onChange, placeholder, type = "text", icon, error, required }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      {label && <label style={{ fontSize: 12, fontWeight: 600, color: colors.slate600, textTransform: "uppercase", letterSpacing: 0.4 }}>{label}{required && <span style={{ color: colors.rose, marginLeft: 2 }}>*</span>}</label>}
      <div style={{ position: "relative" }}>
        {icon && <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", fontSize: 16 }}>{icon}</span>}
        <input
          type={type}
          value={value}
          onChange={e => onChange(e.target.value)}
          placeholder={placeholder}
          style={{
            width: "100%", boxSizing: "border-box",
            padding: icon ? "10px 12px 10px 38px" : "10px 12px",
            fontSize: 13, fontFamily: "inherit",
            border: `1px solid ${error ? colors.rose : colors.slate200}`,
            borderRadius: 10, background: colors.white,
            color: colors.slate900, outline: "none",
            transition: "border-color 0.15s",
          }}
          onFocus={e => e.target.style.borderColor = colors.electric}
          onBlur={e => e.target.style.borderColor = error ? colors.rose : colors.slate200}
        />
      </div>
      {error && <div style={{ fontSize: 11, color: colors.rose }}>{error}</div>}
    </div>
  );
}

function Select({ label, value, onChange, options }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      {label && <label style={{ fontSize: 12, fontWeight: 600, color: colors.slate600, textTransform: "uppercase", letterSpacing: 0.4 }}>{label}</label>}
      <select value={value} onChange={e => onChange(e.target.value)} style={{ padding: "10px 12px", fontSize: 13, fontFamily: "inherit", border: `1px solid ${colors.slate200}`, borderRadius: 10, background: colors.white, color: colors.slate900, outline: "none", cursor: "pointer" }}>
        {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
    </div>
  );
}

function Modal({ open, onClose, title, children, width = 520 }) {
  if (!open) return null;
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 1000, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(11,20,55,0.6)", backdropFilter: "blur(4px)" }} onClick={onClose}>
      <div onClick={e => e.stopPropagation()} style={{ background: colors.white, borderRadius: 20, padding: 32, width, maxWidth: "90vw", maxHeight: "85vh", overflow: "auto", boxShadow: "0 24px 64px rgba(0,0,0,0.2)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <div style={{ fontSize: 18, fontWeight: 700, color: colors.slate900 }}>{title}</div>
          <button onClick={onClose} style={{ background: colors.slate100, border: "none", borderRadius: 8, width: 32, height: 32, cursor: "pointer", fontSize: 16, color: colors.slate500 }}>✕</button>
        </div>
        {children}
      </div>
    </div>
  );
}

function ProgressBar({ value, color, height = 8 }) {
  return (
    <div style={{ background: colors.slate100, borderRadius: 999, height, overflow: "hidden" }}>
      <div style={{ width: `${Math.min(100, Math.max(0, value))}%`, height: "100%", background: color || colors.electric, borderRadius: 999, transition: "width 0.6s ease" }} />
    </div>
  );
}

function Tabs({ tabs, active, onChange }) {
  return (
    <div style={{ display: "flex", gap: 2, background: colors.slate100, borderRadius: 12, padding: 4 }}>
      {tabs.map(t => (
        <button key={t.value} onClick={() => onChange(t.value)} style={{ padding: "7px 16px", borderRadius: 9, border: "none", background: active === t.value ? colors.white : "transparent", color: active === t.value ? colors.slate900 : colors.slate500, fontSize: 13, fontWeight: active === t.value ? 600 : 500, cursor: "pointer", transition: "all 0.15s", fontFamily: "inherit", boxShadow: active === t.value ? "0 1px 4px rgba(0,0,0,0.08)" : "none" }}>
          {t.label}
        </button>
      ))}
    </div>
  );
}

// ─────────────────────────────────────────────
// SIDEBAR
// ─────────────────────────────────────────────
const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: "⊞", section: "Overview" },
  { id: "websites", label: "Websites", icon: "🌐", section: "Monitor" },
  { id: "scanner", label: "Scanner", icon: "🔍", section: "Monitor" },
  { id: "issues", label: "Issues", icon: "⚠", section: "Monitor", badge: 4 },
  { id: "action-plan", label: "Action Plan", icon: "✓", section: "Compliance" },
  { id: "consent", label: "Consent", icon: "🍪", section: "Compliance" },
  { id: "dsar", label: "DSAR", icon: "📨", section: "Compliance", badge: 2 },
  { id: "policies", label: "Policies", icon: "📄", section: "Compliance" },
  { id: "audit-logs", label: "Audit Logs", icon: "📋", section: "Reports" },
  { id: "reports", label: "Reports", icon: "📊", section: "Reports" },
  { id: "settings", label: "Settings", icon: "⚙", section: "Account" },
];

function Sidebar({ currentPage, dispatch, notifications }) {
  const unread = notifications.filter(n => !n.read).length;
  const sections = [...new Set(NAV_ITEMS.map(i => i.section))];

  return (
    <aside style={{ width: 240, flexShrink: 0, background: colors.navy, display: "flex", flexDirection: "column", height: "100vh", position: "sticky", top: 0, overflow: "hidden" }}>
      {/* Logo */}
      <div style={{ padding: "24px 20px 20px", borderBottom: `1px solid rgba(255,255,255,0.08)` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: `linear-gradient(135deg, ${colors.electric}, #7C3AED)`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18, flexShrink: 0 }}>🛡</div>
          <div>
            <div style={{ fontSize: 15, fontWeight: 800, color: "white", letterSpacing: -0.3 }}>Armor</div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.4)", fontWeight: 500, letterSpacing: 0.5, textTransform: "uppercase", marginTop: -1 }}>Trust Platform</div>
          </div>
        </div>
      </div>

      {/* Org selector */}
      <div style={{ padding: "12px 16px", borderBottom: `1px solid rgba(255,255,255,0.06)` }}>
        <div style={{ background: "rgba(255,255,255,0.06)", borderRadius: 10, padding: "10px 12px", display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
          <div style={{ width: 28, height: 28, borderRadius: 7, background: colors.electric, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 800, color: "white", flexShrink: 0 }}>N</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: "white", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>Nexus Retail India</div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.4)" }}>Business Plan</div>
          </div>
          <span style={{ color: "rgba(255,255,255,0.3)", fontSize: 10 }}>▼</span>
        </div>
      </div>

      {/* Navigation */}
      <nav style={{ flex: 1, overflow: "auto", padding: "8px 0" }}>
        {sections.map(section => {
          const items = NAV_ITEMS.filter(i => i.section === section);
          return (
            <div key={section} style={{ marginBottom: 4 }}>
              <div style={{ fontSize: 9, fontWeight: 700, color: "rgba(255,255,255,0.25)", textTransform: "uppercase", letterSpacing: 1.2, padding: "8px 20px 4px" }}>{section}</div>
              {items.map(item => {
                const active = currentPage === item.id;
                return (
                  <button key={item.id} onClick={() => dispatch({ type: "SET_PAGE", page: item.id })} style={{ width: "100%", display: "flex", alignItems: "center", gap: 10, padding: "9px 16px 9px 18px", border: "none", background: active ? "rgba(67,97,238,0.25)" : "transparent", cursor: "pointer", fontFamily: "inherit", borderLeft: active ? `3px solid ${colors.electric}` : "3px solid transparent", transition: "all 0.15s" }}>
                    <span style={{ fontSize: 15, width: 20, textAlign: "center", opacity: active ? 1 : 0.6 }}>{item.icon}</span>
                    <span style={{ flex: 1, fontSize: 13, fontWeight: active ? 600 : 400, color: active ? "white" : "rgba(255,255,255,0.6)", textAlign: "left" }}>{item.label}</span>
                    {item.badge && <span style={{ background: colors.rose, color: "white", fontSize: 10, fontWeight: 700, borderRadius: 999, padding: "1px 6px", minWidth: 18, textAlign: "center" }}>{item.badge}</span>}
                  </button>
                );
              })}
            </div>
          );
        })}
      </nav>

      {/* Bottom user area */}
      <div style={{ padding: "12px 16px", borderTop: `1px solid rgba(255,255,255,0.08)` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 32, height: 32, borderRadius: "50%", background: "linear-gradient(135deg, #4361EE, #7C3AED)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, color: "white", flexShrink: 0 }}>A</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 12, fontWeight: 600, color: "white", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>Admin User</div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.35)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>admin@nexusretail.in</div>
          </div>
          {unread > 0 && (
            <button onClick={() => dispatch({ type: "SET_PAGE", page: "notifications" })} style={{ background: "none", border: "none", cursor: "pointer", position: "relative", padding: 4 }}>
              <span style={{ fontSize: 16 }}>🔔</span>
              <span style={{ position: "absolute", top: 0, right: 0, background: colors.rose, color: "white", fontSize: 9, fontWeight: 700, borderRadius: 999, padding: "1px 4px", minWidth: 14, textAlign: "center" }}>{unread}</span>
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}

// ─────────────────────────────────────────────
// TOP BAR
// ─────────────────────────────────────────────
function TopBar({ title, subtitle, actions, dispatch }) {
  const [search, setSearch] = useState("");

  return (
    <div style={{ padding: "20px 32px 0", display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16, flexWrap: "wrap" }}>
      <div>
        <h1 style={{ fontSize: 22, fontWeight: 800, color: colors.slate900, margin: 0, letterSpacing: -0.5 }}>{title}</h1>
        {subtitle && <p style={{ fontSize: 13, color: colors.slate400, margin: "4px 0 0", fontWeight: 400 }}>{subtitle}</p>}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <div style={{ position: "relative" }}>
          <span style={{ position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)", fontSize: 14, color: colors.slate400 }}>🔍</span>
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search everything…" style={{ padding: "8px 12px 8px 32px", fontSize: 13, border: `1px solid ${colors.slate200}`, borderRadius: 10, background: colors.white, color: colors.slate900, outline: "none", width: 220, fontFamily: "inherit" }} />
        </div>
        {actions}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// DASHBOARD PAGE
// ─────────────────────────────────────────────
function DashboardPage({ state, dispatch }) {
  const { issues, dsars, consents } = state;
  const openIssues = issues.filter(i => i.status === "open" || i.status === "in_progress");
  const criticalIssues = issues.filter(i => i.severity === "critical" && i.status === "open");
  const openDsars = dsars.filter(d => d.status !== "completed");
  const grantedConsents = consents.filter(c => c.granted).length;

  const scores = [
    { label: "Privacy", score: 72, color: colors.electric, icon: "🔒" },
    { label: "Security", score: 68, color: colors.purple, icon: "🛡" },
    { label: "Accessibility", score: 85, color: colors.teal, icon: "♿" },
    { label: "Performance", score: 61, color: colors.amber, icon: "⚡" },
    { label: "SEO", score: 88, color: "#10B981", icon: "📈" },
    { label: "Compliance", score: 74, color: colors.rose, icon: "⚖" },
  ];

  const recentActivity = [
    { icon: "🔍", text: "Scan completed — Customer Portal scored 67/100", time: daysAgo(0.2), type: "scan" },
    { icon: "⚠", text: "Critical: Missing CSP header detected", time: daysAgo(0.3), type: "issue" },
    { icon: "✓", text: "Issue resolved: Alt text on product images", time: daysAgo(1.5), type: "resolved" },
    { icon: "📨", text: "New DSAR from Vikram Rao (Rectification)", time: daysAgo(2), type: "dsar" },
    { icon: "📋", text: "Audit log exported by admin", time: daysAgo(3), type: "audit" },
  ];

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 24 }}>
      {/* Trust Score Hero */}
      <Card style={{ background: `linear-gradient(135deg, ${colors.navy} 0%, ${colors.navyLight} 100%)`, border: "none", padding: "28px 32px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: 24, alignItems: "center" }}>
          <div>
            <div style={{ fontSize: 12, fontWeight: 700, color: "rgba(255,255,255,0.5)", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 8 }}>Overall Trust Score</div>
            <div style={{ display: "flex", alignItems: "baseline", gap: 12 }}>
              <span style={{ fontSize: 64, fontWeight: 900, color: "white", lineHeight: 1 }}>78</span>
              <span style={{ fontSize: 24, color: "rgba(255,255,255,0.4)", fontWeight: 300 }}>/100</span>
            </div>
            <div style={{ marginTop: 16, display: "flex", alignItems: "center", gap: 8 }}>
              <Badge color={colors.amber} bg={`${colors.amber}25`}>Medium Risk</Badge>
              <span style={{ fontSize: 12, color: "rgba(255,255,255,0.4)" }}>↑ +4 pts this month</span>
            </div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
            {scores.map(s => (
              <div key={s.label} style={{ background: "rgba(255,255,255,0.07)", borderRadius: 12, padding: "12px 14px", minWidth: 90 }}>
                <div style={{ fontSize: 18, marginBottom: 4 }}>{s.icon}</div>
                <div style={{ fontSize: 20, fontWeight: 800, color: s.color }}>{s.score}</div>
                <div style={{ fontSize: 10, color: "rgba(255,255,255,0.4)", fontWeight: 500 }}>{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* KPI Row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
        <MetricCard label="Open Issues" value={openIssues.length} delta={`${criticalIssues.length} critical`} deltaType="down" icon="⚠" color={colors.rose} />
        <MetricCard label="Active DSARs" value={openDsars.length} sub="Due within 30 days" icon="📨" color={colors.electric} />
        <MetricCard label="Consent Records" value={grantedConsents} delta="+12 this week" deltaType="up" icon="🍪" color={colors.teal} />
        <MetricCard label="Websites Monitored" value={MOCK_WEBSITES.filter(w => w.monitoringEnabled).length} sub={`of ${MOCK_WEBSITES.length} total`} icon="🌐" color={colors.purple} />
      </div>

      {/* Middle Row */}
      <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 20 }}>
        {/* Website Health */}
        <Card style={{ padding: 0, overflow: "hidden" }}>
          <div style={{ padding: "20px 24px 16px", display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: `1px solid ${colors.slate100}` }}>
            <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900 }}>Website Health</div>
            <Button variant="ghost" size="sm" onClick={() => dispatch({ type: "SET_PAGE", page: "websites" })}>View all →</Button>
          </div>
          <div>
            {MOCK_WEBSITES.map((site, i) => (
              <div key={site.id} style={{ padding: "14px 24px", display: "flex", alignItems: "center", gap: 12, borderBottom: i < MOCK_WEBSITES.length - 1 ? `1px solid ${colors.slate100}` : "none" }}>
                <div style={{ width: 8, height: 8, borderRadius: "50%", background: statusColor(site.status), flexShrink: 0 }} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 13, fontWeight: 600, color: colors.slate900, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{site.name}</div>
                  <div style={{ fontSize: 11, color: colors.slate400 }}>{relativeTime(site.lastScan)}</div>
                </div>
                <div style={{ width: 80 }}>
                  <ProgressBar value={site.trustScore} color={scoreColor(site.trustScore)} />
                </div>
                <ScorePill score={site.trustScore} />
              </div>
            ))}
          </div>
        </Card>

        {/* Recent Activity */}
        <Card style={{ padding: 0, overflow: "hidden" }}>
          <div style={{ padding: "20px 24px 16px", borderBottom: `1px solid ${colors.slate100}` }}>
            <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900 }}>Recent Activity</div>
          </div>
          <div style={{ padding: "8px 0" }}>
            {recentActivity.map((item, i) => (
              <div key={i} style={{ padding: "10px 24px", display: "flex", gap: 10, alignItems: "flex-start" }}>
                <span style={{ fontSize: 16, flexShrink: 0, marginTop: 1 }}>{item.icon}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 12, color: colors.slate700, lineHeight: 1.5 }}>{item.text}</div>
                  <div style={{ fontSize: 11, color: colors.slate400, marginTop: 2 }}>{relativeTime(item.time)}</div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Critical Issues */}
      {criticalIssues.length > 0 && (
        <Card style={{ borderLeft: `4px solid ${colors.rose}`, borderRadius: 16, padding: "20px 24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900 }}>🚨 {criticalIssues.length} Critical Issues Require Attention</div>
            <Button variant="danger" size="sm" onClick={() => dispatch({ type: "SET_PAGE", page: "issues" })}>View all issues</Button>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {criticalIssues.map(issue => (
              <div key={issue.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 14px", background: colors.roseLight, borderRadius: 10 }}>
                <Badge color={colors.rose}>Critical</Badge>
                <span style={{ fontSize: 13, color: colors.slate700, flex: 1 }}>{issue.title}</span>
                <span style={{ fontSize: 11, color: colors.slate400 }}>{issue.website}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────
// WEBSITES PAGE
// ─────────────────────────────────────────────
function WebsitesPage({ state, dispatch }) {
  const [showAdd, setShowAdd] = useState(false);
  const [newUrl, setNewUrl] = useState("");
  const [newName, setNewName] = useState("");

  const handleAddSite = () => {
    if (!newUrl) return;
    dispatch({ type: "ADD_TOAST", toast: { type: "success", title: "Website added", body: newUrl } });
    setShowAdd(false); setNewUrl(""); setNewName("");
  };

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Websites" subtitle="Monitor and scan your web properties" dispatch={dispatch} actions={
        <Button icon="＋" onClick={() => setShowAdd(true)}>Add website</Button>
      } />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
        {MOCK_WEBSITES.map(site => (
          <Card key={site.id} hoverable style={{ padding: 0, overflow: "hidden" }} onClick={() => { dispatch({ type: "SET_SELECTED_WEBSITE", websiteId: site.id }); dispatch({ type: "SET_PAGE", page: "scanner" }); }}>
            <div style={{ padding: "20px 24px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                <div>
                  <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900 }}>{site.name}</div>
                  <div style={{ fontSize: 12, color: colors.slate400, marginTop: 2 }}>{site.url}</div>
                </div>
                <Badge color={statusColor(site.status)}>{statusLabel(site.status)}</Badge>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 12, marginTop: 16 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 11, color: colors.slate400, marginBottom: 4 }}>Trust Score</div>
                  <ProgressBar value={site.trustScore} color={scoreColor(site.trustScore)} />
                </div>
                <ScorePill score={site.trustScore} size="lg" />
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", marginTop: 16, paddingTop: 14, borderTop: `1px solid ${colors.slate100}` }}>
                <div style={{ fontSize: 11, color: colors.slate400 }}>Last scan: {relativeTime(site.lastScan)}</div>
                <div style={{ display: "flex", gap: 6 }}>
                  <Badge color={colors.slate500}>{site.environment}</Badge>
                  {site.monitoringEnabled && <Badge color={colors.teal}>Monitoring on</Badge>}
                </div>
              </div>
            </div>
            <div style={{ background: colors.slate50, padding: "12px 24px", display: "flex", gap: 8 }}>
              <Button size="sm" variant="secondary" onClick={e => { e.stopPropagation(); dispatch({ type: "SET_SELECTED_WEBSITE", websiteId: site.id }); dispatch({ type: "SET_PAGE", page: "scanner" }); }}>🔍 Scan now</Button>
              <Button size="sm" variant="ghost">View report</Button>
            </div>
          </Card>
        ))}
      </div>

      <Modal open={showAdd} onClose={() => setShowAdd(false)} title="Add website">
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Input label="Website URL" value={newUrl} onChange={setNewUrl} placeholder="https://example.com" required icon="🌐" />
          <Input label="Display name" value={newName} onChange={setNewName} placeholder="Main Store" />
          <Select label="Environment" value="Production" onChange={() => {}} options={[{ value: "Production", label: "Production" }, { value: "Staging", label: "Staging" }, { value: "Development", label: "Development" }]} />
          <div style={{ display: "flex", gap: 10, marginTop: 8 }}>
            <Button onClick={handleAddSite} fullWidth>Add website</Button>
            <Button variant="secondary" onClick={() => setShowAdd(false)} fullWidth>Cancel</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}

// ─────────────────────────────────────────────
// SCANNER PAGE
// ─────────────────────────────────────────────
const SCAN_STEPS = [
  "Connecting to website…",
  "Downloading HTML & resources…",
  "Checking HTTPS & TLS version…",
  "Detecting privacy policy…",
  "Detecting cookie banner & CMP…",
  "Scanning forms & data collection…",
  "Analyzing security headers…",
  "Checking content security policy…",
  "Running accessibility audit (WCAG 2.1)…",
  "Measuring Core Web Vitals…",
  "Detecting third-party trackers…",
  "Calculating trust scores…",
  "Generating AI recommendations…",
];

const FULL_SCAN_RESULT = {
  url: "https://app.nexusretail.in",
  scannedAt: new Date().toISOString(),
  overallScore: 67,
  scores: { privacy: 58, security: 62, accessibility: 78, performance: 71, seo: 84, compliance: 55 },
  checks: [
    { category: "Privacy", name: "Privacy Policy", passed: true, detail: "Policy found at /privacy-policy", severity: null },
    { category: "Privacy", name: "Cookie consent banner", passed: false, detail: "No CMP detected. Cookies set before consent.", severity: "critical" },
    { category: "Privacy", name: "Third-party trackers", passed: false, detail: "6 trackers found: GA4, Meta Pixel, Hotjar, Intercom, Mixpanel, Amplitude", severity: "high" },
    { category: "Security", name: "HTTPS enabled", passed: true, detail: "SSL certificate valid until Mar 2026", severity: null },
    { category: "Security", name: "Content Security Policy", passed: false, detail: "CSP header absent in HTTP response", severity: "critical" },
    { category: "Security", name: "HSTS header", passed: false, detail: "HTTP Strict Transport Security not configured", severity: "high" },
    { category: "Security", name: "TLS version", passed: false, detail: "TLS 1.0 still enabled. Only 1.2+ recommended.", severity: "high" },
    { category: "Security", name: "X-Frame-Options", passed: true, detail: "Clickjacking protection present", severity: null },
    { category: "Accessibility", name: "Alt text on images", passed: false, detail: "41 of 67 images missing alt attributes", severity: "medium" },
    { category: "Accessibility", name: "Color contrast", passed: true, detail: "Primary text passes WCAG AA contrast ratio 4.5:1", severity: null },
    { category: "Accessibility", name: "ARIA landmarks", passed: false, detail: "Missing main landmark role on page", severity: "low" },
    { category: "Performance", name: "LCP (Largest Contentful Paint)", passed: false, detail: "4.2s on 3G — exceeds 2.5s threshold", severity: "medium" },
    { category: "Performance", name: "CLS (Cumulative Layout Shift)", passed: true, detail: "CLS: 0.08 — within 0.1 threshold", severity: null },
    { category: "SEO", name: "Meta description", passed: true, detail: "All key pages have unique meta descriptions", severity: null },
    { category: "SEO", name: "Canonical tags", passed: true, detail: "Canonicals correctly implemented", severity: null },
  ],
  recommendations: [
    { priority: 1, title: "Implement cookie consent management", effort: "8h", impact: "Critical", detail: "Deploy a DPDP-compliant CMP. Classify cookies into Necessary, Analytics, Marketing, Preferences categories. Block non-essential scripts until consent is obtained." },
    { priority: 2, title: "Add Content Security Policy header", effort: "4h", impact: "Critical", detail: "Configure CSP to restrict script sources: Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{random}'" },
    { priority: 3, title: "Disable TLS 1.0 and 1.1", effort: "1h", impact: "High", detail: "In your nginx/Apache configuration, set ssl_protocols TLSv1.2 TLSv1.3;" },
    { priority: 4, title: "Configure HSTS header", effort: "1h", impact: "High", detail: "Add Strict-Transport-Security: max-age=31536000; includeSubDomains to all HTTPS responses." },
    { priority: 5, title: "Audit and add alt text to 41 images", effort: "6h", impact: "Medium", detail: "Descriptive alt text is required for WCAG 2.1 Level AA compliance and improves SEO." },
  ],
};

function ScannerPage({ state, dispatch }) {
  const [url, setUrl] = useState("https://app.nexusretail.in");
  const [scanning, setScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState("");
  const [results, setResults] = useState(state.scanResults);
  const [activeTab, setActiveTab] = useState("overview");

  const handleScan = async () => {
    if (!url.trim()) return;
    setScanning(true); setProgress(0); setResults(null);

    for (let i = 0; i < SCAN_STEPS.length; i++) {
      setCurrentStep(SCAN_STEPS[i]);
      setProgress(Math.round(((i + 1) / SCAN_STEPS.length) * 100));
      await new Promise(r => setTimeout(r, 280));
    }
    setResults(FULL_SCAN_RESULT);
    setScanning(false);
    dispatch({ type: "ADD_TOAST", toast: { type: "success", title: "Scan complete", body: `${url} scored ${FULL_SCAN_RESULT.overallScore}/100` } });
    dispatch({ type: "ADD_AUDIT", log: { id: generateId(), user: "admin@nexusretail.in", action: "SCAN_COMPLETED", entity: "Website", entityId: url, ip: "49.204.11.2", browser: "Chrome 124", timestamp: now() } });
  };

  const passed = results?.checks?.filter(c => c.passed).length || 0;
  const failed = results?.checks?.filter(c => !c.passed).length || 0;
  const critical = results?.checks?.filter(c => c.severity === "critical").length || 0;

  const checksByCategory = results ? [...new Set(results.checks.map(c => c.category))].reduce((acc, cat) => {
    acc[cat] = results.checks.filter(c => c.category === cat);
    return acc;
  }, {}) : {};

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Website Scanner" subtitle="AI-powered compliance & security scanner" dispatch={dispatch} />

      {/* Scan input */}
      <Card style={{ padding: "24px 28px" }}>
        <div style={{ display: "flex", gap: 12, alignItems: "flex-end" }}>
          <div style={{ flex: 1 }}>
            <Input label="Website URL to scan" value={url} onChange={setUrl} placeholder="https://example.com" icon="🌐" required />
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <Select label="Scan type" value="deep" onChange={() => {}} options={[{ value: "quick", label: "Quick scan" }, { value: "deep", label: "Deep scan" }]} />
            <div style={{ paddingTop: 22 }}>
              <Button onClick={handleScan} loading={scanning} size="lg" icon={scanning ? null : "🚀"}>
                {scanning ? "Scanning…" : "Start scan"}
              </Button>
            </div>
          </div>
        </div>

        {/* Progress */}
        {scanning && (
          <div style={{ marginTop: 20, padding: "16px 20px", background: colors.electricLight, borderRadius: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
              <span style={{ fontSize: 13, color: colors.electric, fontWeight: 600 }}>{currentStep}</span>
              <span style={{ fontSize: 13, fontWeight: 700, color: colors.electric }}>{progress}%</span>
            </div>
            <ProgressBar value={progress} color={colors.electric} height={6} />
          </div>
        )}
      </Card>

      {/* Results */}
      {results && !scanning && (
        <>
          {/* Score hero */}
          <Card style={{ background: `linear-gradient(135deg, ${colors.navy}, ${colors.navyLight})`, border: "none" }}>
            <div style={{ display: "grid", gridTemplateColumns: "auto 1fr auto", gap: 32, alignItems: "center" }}>
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: 10, fontWeight: 700, color: "rgba(255,255,255,0.4)", textTransform: "uppercase", letterSpacing: 0.8, marginBottom: 6 }}>Trust Score</div>
                <div style={{ fontSize: 56, fontWeight: 900, color: scoreColor(results.overallScore), lineHeight: 1 }}>{results.overallScore}</div>
                <div style={{ fontSize: 14, color: "rgba(255,255,255,0.4)" }}>/100</div>
              </div>
              <div>
                <div style={{ fontSize: 14, fontWeight: 600, color: "white", marginBottom: 4 }}>{results.url}</div>
                <div style={{ fontSize: 11, color: "rgba(255,255,255,0.4)" }}>Scanned {relativeTime(results.scannedAt)}</div>
                <div style={{ display: "flex", gap: 10, marginTop: 16 }}>
                  <div style={{ textAlign: "center", background: "rgba(255,255,255,0.08)", borderRadius: 10, padding: "10px 16px" }}>
                    <div style={{ fontSize: 20, fontWeight: 800, color: colors.teal }}>{passed}</div>
                    <div style={{ fontSize: 10, color: "rgba(255,255,255,0.4)" }}>Passed</div>
                  </div>
                  <div style={{ textAlign: "center", background: "rgba(255,255,255,0.08)", borderRadius: 10, padding: "10px 16px" }}>
                    <div style={{ fontSize: 20, fontWeight: 800, color: colors.rose }}>{failed}</div>
                    <div style={{ fontSize: 10, color: "rgba(255,255,255,0.4)" }}>Failed</div>
                  </div>
                  <div style={{ textAlign: "center", background: "rgba(255,255,255,0.08)", borderRadius: 10, padding: "10px 16px" }}>
                    <div style={{ fontSize: 20, fontWeight: 800, color: colors.rose }}>{critical}</div>
                    <div style={{ fontSize: 10, color: "rgba(255,255,255,0.4)" }}>Critical</div>
                  </div>
                </div>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
                {Object.entries(results.scores).map(([k, v]) => (
                  <div key={k} style={{ background: "rgba(255,255,255,0.07)", borderRadius: 10, padding: "10px 12px", textAlign: "center" }}>
                    <div style={{ fontSize: 18, fontWeight: 800, color: scoreColor(v) }}>{v}</div>
                    <div style={{ fontSize: 9, color: "rgba(255,255,255,0.4)", textTransform: "capitalize", marginTop: 2 }}>{k}</div>
                  </div>
                ))}
              </div>
            </div>
          </Card>

          <Tabs tabs={[{ value: "overview", label: "Overview" }, { value: "checks", label: `Checks (${results.checks.length})` }, { value: "recommendations", label: `Recommendations (${results.recommendations.length})` }]} active={activeTab} onChange={setActiveTab} />

          {activeTab === "overview" && (
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              {Object.entries(checksByCategory).map(([cat, checks]) => {
                const catPassed = checks.filter(c => c.passed).length;
                const catScore = Math.round((catPassed / checks.length) * 100);
                return (
                  <Card key={cat} style={{ padding: "20px 24px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                      <div style={{ fontSize: 14, fontWeight: 700, color: colors.slate900 }}>{cat}</div>
                      <ScorePill score={catScore} />
                    </div>
                    <ProgressBar value={catScore} color={scoreColor(catScore)} />
                    <div style={{ marginTop: 12, fontSize: 12, color: colors.slate400 }}>{catPassed}/{checks.length} checks passed</div>
                  </Card>
                );
              })}
            </div>
          )}

          {activeTab === "checks" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {Object.entries(checksByCategory).map(([cat, checks]) => (
                <Card key={cat} style={{ padding: "16px 20px" }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: colors.slate600, marginBottom: 10, textTransform: "uppercase", letterSpacing: 0.5, fontSize: 11 }}>{cat}</div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                    {checks.map((check, i) => (
                      <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 10, padding: "10px 14px", background: check.passed ? colors.tealLight : `${colors.rose}08`, borderRadius: 10, border: `1px solid ${check.passed ? "#D1FAE5" : `${colors.rose}20`}` }}>
                        <span style={{ fontSize: 16, flexShrink: 0, marginTop: 1 }}>{check.passed ? "✅" : "❌"}</span>
                        <div style={{ flex: 1 }}>
                          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                            <span style={{ fontSize: 13, fontWeight: 600, color: colors.slate800 }}>{check.name}</span>
                            {check.severity && <Badge color={severityColor(check.severity)}>{check.severity}</Badge>}
                          </div>
                          <div style={{ fontSize: 12, color: colors.slate500, marginTop: 3 }}>{check.detail}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              ))}
            </div>
          )}

          {activeTab === "recommendations" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {results.recommendations.map((rec, i) => (
                <Card key={i} style={{ borderLeft: `4px solid ${i < 2 ? colors.rose : i < 4 ? colors.amber : colors.teal}` }}>
                  <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
                    <div style={{ width: 32, height: 32, borderRadius: 8, background: colors.electricLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, fontWeight: 800, color: colors.electric, flexShrink: 0 }}>{rec.priority}</div>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                        <div style={{ fontSize: 14, fontWeight: 700, color: colors.slate900 }}>{rec.title}</div>
                        <Badge color={severityColor(rec.impact.toLowerCase())}>{rec.impact}</Badge>
                        <span style={{ fontSize: 11, color: colors.slate400 }}>~{rec.effort}</span>
                      </div>
                      <div style={{ fontSize: 13, color: colors.slate600, lineHeight: 1.6 }}>{rec.detail}</div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </>
      )}

      {!results && !scanning && (
        <Card style={{ background: colors.slate50, border: `2px dashed ${colors.slate200}` }}>
          <EmptyState icon="🔍" title="Ready to scan" description="Enter a website URL above and click Start scan to run a comprehensive compliance, security, and privacy audit." />
        </Card>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────
// ISSUES PAGE
// ─────────────────────────────────────────────
function IssuesPage({ state, dispatch }) {
  const [filter, setFilter] = useState("all");
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [sortBy, setSortBy] = useState("severity");

  const { issues } = state;

  const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };

  const filtered = issues
    .filter(i => filter === "all" ? true : filter === "open" ? (i.status === "open" || i.status === "in_progress") : i.status === filter)
    .sort((a, b) => sortBy === "severity" ? (severityOrder[a.severity] - severityOrder[b.severity]) : new Date(b.createdAt) - new Date(a.createdAt));

  const counts = {
    all: issues.length,
    open: issues.filter(i => i.status === "open").length,
    in_progress: issues.filter(i => i.status === "in_progress").length,
    resolved: issues.filter(i => i.status === "resolved").length,
  };

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Issues" subtitle={`${counts.open} open issues requiring attention`} dispatch={dispatch} actions={
        <Select label="" value={sortBy} onChange={setSortBy} options={[{ value: "severity", label: "Sort by severity" }, { value: "date", label: "Sort by date" }]} />
      } />

      {/* Filter tabs */}
      <div style={{ display: "flex", gap: 8 }}>
        {[["all", "All"], ["open", "Open"], ["in_progress", "In Progress"], ["resolved", "Resolved"]].map(([val, label]) => (
          <button key={val} onClick={() => setFilter(val)} style={{ padding: "6px 14px", borderRadius: 20, border: `1px solid ${filter === val ? colors.electric : colors.slate200}`, background: filter === val ? colors.electricLight : "white", color: filter === val ? colors.electric : colors.slate600, fontSize: 12, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", display: "flex", alignItems: "center", gap: 6 }}>
            {label}
            <span style={{ background: filter === val ? colors.electric : colors.slate100, color: filter === val ? "white" : colors.slate500, borderRadius: 999, padding: "1px 7px", fontSize: 10, fontWeight: 700 }}>{counts[val]}</span>
          </button>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: selectedIssue ? "1fr 1fr" : "1fr", gap: 20 }}>
        {/* Issue list */}
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {filtered.length === 0 ? (
            <Card style={{ background: colors.slate50, border: `2px dashed ${colors.slate200}` }}>
              <EmptyState icon="✅" title="No issues here" description="All issues in this category have been addressed." />
            </Card>
          ) : (
            filtered.map(issue => (
              <Card key={issue.id} hoverable onClick={() => setSelectedIssue(issue)} style={{ padding: "16px 20px", cursor: "pointer", border: selectedIssue?.id === issue.id ? `2px solid ${colors.electric}` : `1px solid ${colors.slate200}` }}>
                <div style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
                  <div style={{ width: 4, alignSelf: "stretch", borderRadius: 2, background: severityColor(issue.severity), flexShrink: 0 }} />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4, flexWrap: "wrap" }}>
                      <Badge color={severityColor(issue.severity)}>{issue.severity}</Badge>
                      <Badge color={colors.slate500} bg={colors.slate100}>{issue.category}</Badge>
                      <Badge color={statusColor(issue.status)} bg={`${statusColor(issue.status)}15`}>{statusLabel(issue.status)}</Badge>
                    </div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: colors.slate900, marginBottom: 4 }}>{issue.title}</div>
                    <div style={{ display: "flex", gap: 12, fontSize: 11, color: colors.slate400 }}>
                      <span>🌐 {issue.website}</span>
                      {issue.assignee && <span>👤 {issue.assignee}</span>}
                      <span>🕐 {relativeTime(issue.createdAt)}</span>
                      <span>⏱ ~{issue.effortHours}h to fix</span>
                    </div>
                  </div>
                </div>
              </Card>
            ))
          )}
        </div>

        {/* Issue detail panel */}
        {selectedIssue && (
          <Card style={{ position: "sticky", top: 20, alignSelf: "flex-start", maxHeight: "calc(100vh - 100px)", overflow: "auto" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 20 }}>
              <div>
                <div style={{ display: "flex", gap: 6, marginBottom: 8 }}>
                  <Badge color={severityColor(selectedIssue.severity)}>{selectedIssue.severity}</Badge>
                  <Badge color={colors.slate500} bg={colors.slate100}>{selectedIssue.category}</Badge>
                </div>
                <div style={{ fontSize: 16, fontWeight: 700, color: colors.slate900 }}>{selectedIssue.title}</div>
              </div>
              <button onClick={() => setSelectedIssue(null)} style={{ background: colors.slate100, border: "none", borderRadius: 8, width: 28, height: 28, cursor: "pointer", fontSize: 14, color: colors.slate500 }}>✕</button>
            </div>

            {[
              ["Description", selectedIssue.description],
              ["Evidence", selectedIssue.evidence],
              ["Business impact", selectedIssue.businessImpact],
              ["Legal impact", selectedIssue.legalImpact],
              ["Recommendation", selectedIssue.recommendation],
            ].map(([label, val]) => val && (
              <div key={label} style={{ marginBottom: 16 }}>
                <div style={{ fontSize: 11, fontWeight: 700, color: colors.slate400, textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 }}>{label}</div>
                <div style={{ fontSize: 13, color: colors.slate700, lineHeight: 1.6, padding: "10px 12px", background: colors.slate50, borderRadius: 8 }}>{val}</div>
              </div>
            ))}

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 8 }}>
              {[
                ["Website", selectedIssue.website],
                ["Estimated effort", `${selectedIssue.effortHours} hours`],
                ["Assigned to", selectedIssue.assignee || "Unassigned"],
                ["Status", statusLabel(selectedIssue.status)],
                ["Reported", formatDate(selectedIssue.createdAt)],
              ].map(([label, val]) => (
                <div key={label} style={{ background: colors.slate50, borderRadius: 8, padding: "10px 12px" }}>
                  <div style={{ fontSize: 10, color: colors.slate400, fontWeight: 600, textTransform: "uppercase", marginBottom: 4 }}>{label}</div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: colors.slate800 }}>{val}</div>
                </div>
              ))}
            </div>

            <div style={{ display: "flex", gap: 8, marginTop: 20 }}>
              {selectedIssue.status !== "resolved" && (
                <Button size="sm" variant="teal" fullWidth onClick={() => {
                  dispatch({ type: "UPDATE_ISSUE", id: selectedIssue.id, patch: { status: "resolved" } });
                  dispatch({ type: "ADD_TOAST", toast: { type: "success", title: "Issue resolved" } });
                  setSelectedIssue(null);
                }}>Mark resolved</Button>
              )}
              {selectedIssue.status === "open" && (
                <Button size="sm" variant="secondary" fullWidth onClick={() => {
                  dispatch({ type: "UPDATE_ISSUE", id: selectedIssue.id, patch: { status: "in_progress" } });
                  dispatch({ type: "ADD_TOAST", toast: { type: "info", title: "Issue in progress" } });
                  setSelectedIssue(prev => ({ ...prev, status: "in_progress" }));
                }}>Start working</Button>
              )}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// ACTION PLAN PAGE
// ─────────────────────────────────────────────
function ActionPlanPage({ state, dispatch }) {
  const { issues } = state;
  const openIssues = issues.filter(i => i.status !== "resolved");

  const riskReduction = [
    { action: "Implement cookie consent banner", risk: 28, effort: "8h", priority: "Critical", category: "Privacy" },
    { action: "Add Content Security Policy header", risk: 22, effort: "4h", priority: "Critical", category: "Security" },
    { action: "Disable TLS 1.0", risk: 18, effort: "1h", priority: "High", category: "Security" },
    { action: "Configure HSTS header", risk: 12, effort: "1h", priority: "High", category: "Security" },
    { action: "Add alt text to 41 images", risk: 8, effort: "6h", priority: "Medium", category: "Accessibility" },
    { action: "Optimize LCP to under 2.5s", risk: 6, effort: "12h", priority: "Medium", category: "Performance" },
  ];

  const totalHours = riskReduction.reduce((sum, r) => sum + parseInt(r.effort), 0);
  const totalRiskReduction = riskReduction.reduce((sum, r) => sum + r.risk, 0);

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Action Plan" subtitle="AI-prioritized remediation roadmap" dispatch={dispatch} />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
        <MetricCard label="Open tasks" value={openIssues.length} icon="📋" color={colors.electric} />
        <MetricCard label="Estimated effort" value={`${totalHours}h`} sub="to resolve all issues" icon="⏱" color={colors.purple} />
        <MetricCard label="Potential score gain" value={`+${Math.min(totalRiskReduction, 33)} pts`} delta="on Trust Score" deltaType="up" icon="📈" color={colors.teal} />
      </div>

      {/* Prioritized tasks */}
      <Card style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ padding: "20px 24px", borderBottom: `1px solid ${colors.slate100}` }}>
          <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900 }}>Prioritized remediation tasks</div>
          <div style={{ fontSize: 12, color: colors.slate400, marginTop: 2 }}>Ordered by risk reduction impact</div>
        </div>
        {riskReduction.map((item, i) => (
          <div key={i} style={{ padding: "16px 24px", display: "flex", alignItems: "center", gap: 14, borderBottom: i < riskReduction.length - 1 ? `1px solid ${colors.slate100}` : "none" }}>
            <div style={{ width: 28, height: 28, borderRadius: "50%", background: severityColor(item.priority.toLowerCase()) + "20", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 800, color: severityColor(item.priority.toLowerCase()), flexShrink: 0 }}>{i + 1}</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 14, fontWeight: 600, color: colors.slate900 }}>{item.action}</div>
              <div style={{ display: "flex", gap: 8, marginTop: 4 }}>
                <Badge color={colors.slate500} bg={colors.slate100}>{item.category}</Badge>
                <span style={{ fontSize: 11, color: colors.slate400 }}>~{item.effort}</span>
              </div>
            </div>
            <div style={{ textAlign: "right", flexShrink: 0 }}>
              <div style={{ fontSize: 14, fontWeight: 700, color: colors.teal }}>−{item.risk} risk pts</div>
              <Badge color={severityColor(item.priority.toLowerCase())}>{item.priority}</Badge>
            </div>
          </div>
        ))}
      </Card>

      {/* AI Explanation */}
      <Card style={{ background: colors.electricLight, border: `1px solid ${colors.electric}30`, padding: "24px 28px" }}>
        <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
          <div style={{ fontSize: 28, flexShrink: 0 }}>🤖</div>
          <div>
            <div style={{ fontSize: 14, fontWeight: 700, color: colors.electric, marginBottom: 8 }}>AI compliance assessment</div>
            <div style={{ fontSize: 13, color: colors.slate700, lineHeight: 1.7 }}>
              Your current Trust Score of <strong>67/100</strong> indicates moderate compliance risk. The two critical findings (missing cookie consent and absent CSP header) account for <strong>50 points of risk</strong>. Addressing these in the first sprint, estimated at <strong>12 total hours</strong>, would bring your score to approximately <strong>82/100</strong> — moving you from Medium to Low risk tier under DPDP Act 2023.
              <br /><br />
              Priority recommendation: Engage a DPDP-compliant CMP vendor before Q3 to avoid potential regulatory action as Indian enforcement begins.
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}

// ─────────────────────────────────────────────
// CONSENT PAGE
// ─────────────────────────────────────────────
function ConsentPage({ state, dispatch }) {
  const { consents } = state;
  const [showAdd, setShowAdd] = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [newPurpose, setNewPurpose] = useState("Marketing");
  const [activeTab, setActiveTab] = useState("records");

  const granted = consents.filter(c => c.granted).length;
  const withdrawn = consents.filter(c => !c.granted).length;

  const handleAdd = () => {
    if (!newEmail) return;
    const record = { id: generateId(), email: newEmail, purpose: newPurpose, granted: true, grantedAt: now(), ip: "0.0.0.0", channel: "Manual" };
    dispatch({ type: "ADD_CONSENT", consent: record });
    dispatch({ type: "ADD_AUDIT", log: { id: generateId(), user: "admin@nexusretail.in", action: "CONSENT_CREATED", entity: "Consent", entityId: record.id, ip: "49.204.11.2", browser: "Chrome 124", timestamp: now() } });
    dispatch({ type: "ADD_TOAST", toast: { type: "success", title: "Consent record created" } });
    setShowAdd(false); setNewEmail(""); setNewPurpose("Marketing");
  };

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Consent Management" subtitle="Track and manage user consent records" dispatch={dispatch} actions={
        <Button icon="＋" onClick={() => setShowAdd(true)}>Create record</Button>
      } />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
        <MetricCard label="Total records" value={consents.length} icon="🍪" color={colors.electric} />
        <MetricCard label="Active consents" value={granted} delta={`${Math.round(granted / consents.length * 100)}% rate`} deltaType="up" icon="✅" color={colors.teal} />
        <MetricCard label="Withdrawn" value={withdrawn} icon="❌" color={colors.rose} />
        <MetricCard label="Channels" value={3} sub="Web, Mobile, Email" icon="📡" color={colors.purple} />
      </div>

      <Tabs tabs={[{ value: "records", label: "Consent records" }, { value: "analytics", label: "Analytics" }, { value: "categories", label: "Cookie categories" }]} active={activeTab} onChange={setActiveTab} />

      {activeTab === "records" && (
        <Card style={{ padding: 0, overflow: "hidden" }}>
          <div style={{ overflow: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
              <thead>
                <tr style={{ background: colors.slate50 }}>
                  {["Email", "Purpose", "Status", "Channel", "Granted at", "Actions"].map(h => (
                    <th key={h} style={{ padding: "10px 16px", textAlign: "left", fontSize: 11, fontWeight: 700, color: colors.slate500, textTransform: "uppercase", letterSpacing: 0.5, borderBottom: `1px solid ${colors.slate200}` }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {consents.map((c, i) => (
                  <tr key={c.id} style={{ borderBottom: `1px solid ${colors.slate100}` }}>
                    <td style={{ padding: "12px 16px", color: colors.slate900, fontWeight: 500 }}>{c.email}</td>
                    <td style={{ padding: "12px 16px" }}><Badge color={colors.electric} bg={colors.electricLight}>{c.purpose}</Badge></td>
                    <td style={{ padding: "12px 16px" }}>{c.granted ? <Badge color={colors.teal} bg={colors.tealLight}>Granted</Badge> : <Badge color={colors.rose} bg={colors.roseLight}>Withdrawn</Badge>}</td>
                    <td style={{ padding: "12px 16px", color: colors.slate500 }}>{c.channel}</td>
                    <td style={{ padding: "12px 16px", color: colors.slate400 }}>{formatDate(c.grantedAt)}</td>
                    <td style={{ padding: "12px 16px" }}>
                      {c.granted && <Button size="sm" variant="ghost" onClick={() => {
                        dispatch({ type: "UPDATE_ISSUE" });
                        const updated = consents.map(x => x.id === c.id ? { ...x, granted: false } : x);
                        dispatch({ type: "ADD_TOAST", toast: { type: "warning", title: "Consent withdrawn" } });
                      }}>Withdraw</Button>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {activeTab === "analytics" && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
          {[["Marketing", 68], ["Analytics", 82], ["Newsletter", 75], ["Product Updates", 91]].map(([purpose, rate]) => (
            <Card key={purpose}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                <div style={{ fontSize: 14, fontWeight: 600, color: colors.slate900 }}>{purpose}</div>
                <span style={{ fontSize: 18, fontWeight: 800, color: scoreColor(rate) }}>{rate}%</span>
              </div>
              <ProgressBar value={rate} color={scoreColor(rate)} />
              <div style={{ fontSize: 11, color: colors.slate400, marginTop: 8 }}>Consent rate</div>
            </Card>
          ))}
        </div>
      )}

      {activeTab === "categories" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {[
            { name: "Necessary", desc: "Required for basic website functionality. Cannot be disabled.", required: true, cookies: 4 },
            { name: "Analytics", desc: "Help understand how visitors interact with the website.", required: false, cookies: 8 },
            { name: "Marketing", desc: "Track visitors for targeted advertising purposes.", required: false, cookies: 12 },
            { name: "Preferences", desc: "Remember user preferences like language or region.", required: false, cookies: 3 },
          ].map(cat => (
            <Card key={cat.name} style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                  <div style={{ fontSize: 14, fontWeight: 700, color: colors.slate900 }}>{cat.name}</div>
                  {cat.required && <Badge color={colors.teal} bg={colors.tealLight}>Always on</Badge>}
                  <Badge color={colors.slate500} bg={colors.slate100}>{cat.cookies} cookies</Badge>
                </div>
                <div style={{ fontSize: 13, color: colors.slate500 }}>{cat.desc}</div>
              </div>
              <div style={{ flexShrink: 0 }}>
                <div style={{ width: 40, height: 22, borderRadius: 11, background: !cat.required ? colors.slate200 : colors.teal, position: "relative", cursor: !cat.required ? "pointer" : "default" }}>
                  <div style={{ width: 16, height: 16, borderRadius: "50%", background: "white", position: "absolute", top: 3, left: cat.required ? 21 : 3, transition: "left 0.2s" }} />
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal open={showAdd} onClose={() => setShowAdd(false)} title="Create consent record">
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Input label="Email address" value={newEmail} onChange={setNewEmail} placeholder="customer@example.com" required type="email" />
          <Select label="Purpose" value={newPurpose} onChange={setNewPurpose} options={["Marketing", "Analytics", "Newsletter", "Product Updates", "Other"].map(p => ({ value: p, label: p }))} />
          <div style={{ display: "flex", gap: 10 }}>
            <Button onClick={handleAdd} fullWidth>Create record</Button>
            <Button variant="secondary" onClick={() => setShowAdd(false)} fullWidth>Cancel</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}

// ─────────────────────────────────────────────
// DSAR PAGE
// ─────────────────────────────────────────────
function DSARPage({ state, dispatch }) {
  const { dsars } = state;
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({ email: "", name: "", type: "Access" });
  const [filter, setFilter] = useState("all");

  const open = dsars.filter(d => d.status !== "completed").length;
  const overdue = dsars.filter(d => d.status !== "completed" && new Date(d.dueAt) < new Date()).length;

  const filtered = dsars.filter(d => filter === "all" ? true : d.status === filter);

  const handleCreate = () => {
    if (!form.email || !form.name) return;
    const dsar = {
      id: generateId(), requesterName: form.name, requesterEmail: form.email,
      requestType: form.type, status: "submitted",
      submittedAt: now(), dueAt: new Date(Date.now() + 30 * 86400000).toISOString(), assignee: null
    };
    dispatch({ type: "ADD_DSAR", dsar });
    dispatch({ type: "ADD_AUDIT", log: { id: generateId(), user: "admin@nexusretail.in", action: "DSAR_CREATED", entity: "DSAR", entityId: dsar.id, ip: "49.204.11.2", browser: "Chrome 124", timestamp: now() } });
    dispatch({ type: "ADD_TOAST", toast: { type: "success", title: "DSAR request created", body: `${form.name}'s ${form.type} request opened` } });
    setShowAdd(false); setForm({ email: "", name: "", type: "Access" });
  };

  const workflowSteps = ["Submitted", "Identity Verification", "Data Collection", "In Review", "Approved", "Response Sent", "Completed"];

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="DSAR Management" subtitle="Data Subject Access Request workflow" dispatch={dispatch} actions={
        <Button icon="＋" onClick={() => setShowAdd(true)}>New request</Button>
      } />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
        <MetricCard label="Open requests" value={open} icon="📨" color={colors.electric} />
        <MetricCard label="Overdue" value={overdue} icon="⚠" color={colors.rose} />
        <MetricCard label="Completed" value={dsars.filter(d => d.status === "completed").length} delta="this month" deltaType="up" icon="✅" color={colors.teal} />
        <MetricCard label="Avg. resolution" value="12d" sub="30-day SLA" icon="⏱" color={colors.purple} />
      </div>

      {/* Workflow */}
      <Card style={{ padding: "20px 24px" }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: colors.slate900, marginBottom: 16 }}>DSAR workflow stages</div>
        <div style={{ display: "flex", gap: 0, overflowX: "auto" }}>
          {workflowSteps.map((step, i) => (
            <div key={step} style={{ display: "flex", alignItems: "center" }}>
              <div style={{ textAlign: "center", padding: "8px 12px", background: i < 4 ? colors.electricLight : colors.slate50, borderRadius: 8, minWidth: 90 }}>
                <div style={{ width: 24, height: 24, borderRadius: "50%", background: i < 4 ? colors.electric : colors.slate200, color: i < 4 ? "white" : colors.slate400, fontSize: 11, fontWeight: 700, display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 6px" }}>{i + 1}</div>
                <div style={{ fontSize: 10, fontWeight: 600, color: i < 4 ? colors.electric : colors.slate400, lineHeight: 1.3 }}>{step}</div>
              </div>
              {i < workflowSteps.length - 1 && <div style={{ width: 20, height: 2, background: i < 3 ? colors.electric : colors.slate200, flexShrink: 0 }} />}
            </div>
          ))}
        </div>
      </Card>

      {/* Filter */}
      <div style={{ display: "flex", gap: 8 }}>
        {[["all", "All"], ["submitted", "Submitted"], ["in_review", "In Review"], ["pending_verification", "Pending Verification"], ["completed", "Completed"]].map(([val, label]) => (
          <button key={val} onClick={() => setFilter(val)} style={{ padding: "5px 12px", borderRadius: 20, border: `1px solid ${filter === val ? colors.electric : colors.slate200}`, background: filter === val ? colors.electricLight : "white", color: filter === val ? colors.electric : colors.slate600, fontSize: 12, fontWeight: 500, cursor: "pointer", fontFamily: "inherit" }}>{label}</button>
        ))}
      </div>

      {/* Request list */}
      <Card style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ overflow: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ background: colors.slate50 }}>
                {["Requester", "Type", "Status", "Submitted", "Due", "Assignee", "Actions"].map(h => (
                  <th key={h} style={{ padding: "10px 16px", textAlign: "left", fontSize: 11, fontWeight: 700, color: colors.slate500, textTransform: "uppercase", letterSpacing: 0.5, borderBottom: `1px solid ${colors.slate200}` }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map(req => {
                const isOverdue = req.status !== "completed" && new Date(req.dueAt) < new Date();
                return (
                  <tr key={req.id} style={{ borderBottom: `1px solid ${colors.slate100}` }}>
                    <td style={{ padding: "12px 16px" }}>
                      <div style={{ fontWeight: 600, color: colors.slate900 }}>{req.requesterName}</div>
                      <div style={{ fontSize: 11, color: colors.slate400 }}>{req.requesterEmail}</div>
                    </td>
                    <td style={{ padding: "12px 16px" }}><Badge color={colors.electric} bg={colors.electricLight}>{req.requestType}</Badge></td>
                    <td style={{ padding: "12px 16px" }}><Badge color={statusColor(req.status)} bg={`${statusColor(req.status)}15`}>{statusLabel(req.status)}</Badge></td>
                    <td style={{ padding: "12px 16px", color: colors.slate500 }}>{formatDate(req.submittedAt)}</td>
                    <td style={{ padding: "12px 16px" }}>
                      <span style={{ color: isOverdue ? colors.rose : colors.slate500, fontWeight: isOverdue ? 700 : 400 }}>
                        {isOverdue ? "⚠ " : ""}{formatDate(req.dueAt)}
                      </span>
                    </td>
                    <td style={{ padding: "12px 16px", color: colors.slate500 }}>{req.assignee || "—"}</td>
                    <td style={{ padding: "12px 16px" }}>
                      {req.status !== "completed" && (
                        <Button size="sm" variant="ghost" onClick={() => {
                          const nextStatus = { submitted: "pending_verification", pending_verification: "in_review", in_review: "completed" };
                          dispatch({ type: "UPDATE_DSAR", id: req.id, patch: { status: nextStatus[req.status] || "completed" } });
                          dispatch({ type: "ADD_TOAST", toast: { type: "info", title: "DSAR status updated" } });
                        }}>Advance →</Button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          {filtered.length === 0 && <EmptyState icon="📭" title="No requests found" description="DSAR requests appear here when submitted by data subjects." />}
        </div>
      </Card>

      <Modal open={showAdd} onClose={() => setShowAdd(false)} title="Create DSAR request">
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Input label="Requester name" value={form.name} onChange={v => setForm(f => ({ ...f, name: v }))} placeholder="Full name" required />
          <Input label="Email address" value={form.email} onChange={v => setForm(f => ({ ...f, email: v }))} placeholder="requester@email.com" type="email" required />
          <Select label="Request type" value={form.type} onChange={v => setForm(f => ({ ...f, type: v }))} options={["Access", "Delete", "Rectification", "Portability", "Consent Withdrawal"].map(t => ({ value: t, label: t }))} />
          <div style={{ background: colors.amberLight, borderRadius: 10, padding: "10px 14px", fontSize: 12, color: colors.amber, fontWeight: 500 }}>
            ⏱ 30-day SLA starts from today: due by {formatDate(new Date(Date.now() + 30 * 86400000).toISOString())}
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <Button onClick={handleCreate} fullWidth>Create request</Button>
            <Button variant="secondary" onClick={() => setShowAdd(false)} fullWidth>Cancel</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}

// ─────────────────────────────────────────────
// AUDIT LOGS PAGE
// ─────────────────────────────────────────────
function AuditLogsPage({ state, dispatch }) {
  const { auditLogs } = state;
  const [filter, setFilter] = useState("");

  const filtered = filter ? auditLogs.filter(l => l.action.toLowerCase().includes(filter.toLowerCase()) || l.user.toLowerCase().includes(filter.toLowerCase()) || l.entity.toLowerCase().includes(filter.toLowerCase())) : auditLogs;

  const actionColors = {
    SCAN_COMPLETED: colors.electric, DSAR_CREATED: colors.purple, DSAR_STATUS_UPDATED: colors.amber,
    CONSENT_CREATED: colors.teal, CONSENT_RECORD_EXPORTED: colors.teal, ISSUE_ASSIGNED: colors.electric,
    ISSUE_RESOLVED: colors.teal, POLICY_PUBLISHED: colors.purple,
  };

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Audit Logs" subtitle="Immutable record of all platform activity" dispatch={dispatch} actions={
        <Button variant="secondary" size="sm" icon="↓">Export CSV</Button>
      } />

      <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <div style={{ flex: 1, position: "relative" }}>
          <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", fontSize: 14, color: colors.slate400 }}>🔍</span>
          <input value={filter} onChange={e => setFilter(e.target.value)} placeholder="Filter by user, action, or entity…" style={{ width: "100%", boxSizing: "border-box", padding: "9px 12px 9px 36px", fontSize: 13, border: `1px solid ${colors.slate200}`, borderRadius: 10, background: colors.white, color: colors.slate900, outline: "none", fontFamily: "inherit" }} />
        </div>
        <div style={{ fontSize: 12, color: colors.slate400, flexShrink: 0 }}>{filtered.length} events</div>
      </div>

      <Card style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ overflow: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ background: colors.slate50 }}>
                {["Timestamp", "User", "Action", "Entity", "IP Address", "Browser"].map(h => (
                  <th key={h} style={{ padding: "10px 16px", textAlign: "left", fontSize: 11, fontWeight: 700, color: colors.slate500, textTransform: "uppercase", letterSpacing: 0.5, borderBottom: `1px solid ${colors.slate200}`, whiteSpace: "nowrap" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((log, i) => (
                <tr key={log.id} style={{ borderBottom: `1px solid ${colors.slate100}`, background: i % 2 === 0 ? "white" : colors.slate50 }}>
                  <td style={{ padding: "10px 16px", color: colors.slate400, whiteSpace: "nowrap", fontFamily: "monospace", fontSize: 12 }}>{new Date(log.timestamp).toLocaleString("en-IN", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" })}</td>
                  <td style={{ padding: "10px 16px", color: colors.slate700, fontWeight: 500 }}>{log.user}</td>
                  <td style={{ padding: "10px 16px" }}>
                    <span style={{ background: `${actionColors[log.action] || colors.slate400}15`, color: actionColors[log.action] || colors.slate400, padding: "3px 8px", borderRadius: 6, fontWeight: 700, fontSize: 11, fontFamily: "monospace", letterSpacing: 0.2 }}>{log.action}</span>
                  </td>
                  <td style={{ padding: "10px 16px" }}><span style={{ color: colors.slate600 }}>{log.entity}</span> {log.entityId && <span style={{ fontSize: 10, color: colors.slate300, fontFamily: "monospace" }}>{log.entityId}</span>}</td>
                  <td style={{ padding: "10px 16px", color: colors.slate400, fontFamily: "monospace", fontSize: 12 }}>{log.ip}</td>
                  <td style={{ padding: "10px 16px", color: colors.slate400, fontSize: 12 }}>{log.browser}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {filtered.length === 0 && <EmptyState icon="📋" title="No logs match your filter" description="Try different search terms to find audit records." />}
        </div>
      </Card>
    </div>
  );
}

// ─────────────────────────────────────────────
// REPORTS PAGE
// ─────────────────────────────────────────────
function ReportsPage({ state, dispatch }) {
  const reportTypes = [
    { icon: "📊", title: "Executive Summary", desc: "C-suite overview of compliance posture and risk", tags: ["PDF", "DOCX"], time: "~30s" },
    { icon: "🔒", title: "Privacy Report", desc: "Detailed privacy compliance analysis per website", tags: ["PDF", "CSV"], time: "~45s" },
    { icon: "🛡", title: "Security Report", desc: "Security headers, SSL, vulnerability findings", tags: ["PDF"], time: "~40s" },
    { icon: "📨", title: "DSAR Activity Report", desc: "Request log, SLA compliance, resolution times", tags: ["PDF", "CSV"], time: "~20s" },
    { icon: "🍪", title: "Consent Analytics Report", desc: "Opt-in rates, categories, geographic breakdown", tags: ["PDF", "XLSX"], time: "~25s" },
    { icon: "📋", title: "Audit Trail Report", desc: "Complete immutable event log for compliance evidence", tags: ["PDF", "CSV"], time: "~15s" },
    { icon: "⚖", title: "DPDP Compliance Report", desc: "India DPDP Act 2023 readiness assessment", tags: ["PDF"], time: "~60s" },
    { icon: "⚡", title: "Performance Report", desc: "Core Web Vitals and performance findings per site", tags: ["PDF", "XLSX"], time: "~35s" },
  ];

  const [generating, setGenerating] = useState(null);

  const handleGenerate = async (title) => {
    setGenerating(title);
    await new Promise(r => setTimeout(r, 2000));
    setGenerating(null);
    dispatch({ type: "ADD_TOAST", toast: { type: "success", title: "Report generated", body: `${title} is ready to download` } });
  };

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Reports" subtitle="Generate and export compliance reports" dispatch={dispatch} />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
        {reportTypes.map(r => (
          <Card key={r.title} style={{ padding: "20px 24px", display: "flex", gap: 16, alignItems: "flex-start" }}>
            <div style={{ fontSize: 28, flexShrink: 0 }}>{r.icon}</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 14, fontWeight: 700, color: colors.slate900, marginBottom: 4 }}>{r.title}</div>
              <div style={{ fontSize: 12, color: colors.slate500, lineHeight: 1.5, marginBottom: 10 }}>{r.desc}</div>
              <div style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" }}>
                {r.tags.map(tag => <Badge key={tag} color={colors.slate500} bg={colors.slate100}>{tag}</Badge>)}
                <span style={{ fontSize: 11, color: colors.slate400 }}>⏱ {r.time}</span>
              </div>
            </div>
            <Button size="sm" loading={generating === r.title} onClick={() => handleGenerate(r.title)} variant="secondary">
              {generating === r.title ? "Generating…" : "Generate"}
            </Button>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// POLICIES PAGE
// ─────────────────────────────────────────────
function PoliciesPage({ state, dispatch }) {
  const policies = [
    { id: "p1", name: "Privacy Policy", version: "v3.2", status: "published", updatedAt: daysAgo(3), wordCount: 2840 },
    { id: "p2", name: "Cookie Policy", version: "v2.0", status: "published", updatedAt: daysAgo(30), wordCount: 1240 },
    { id: "p3", name: "Terms of Service", version: "v1.5", status: "draft", updatedAt: daysAgo(7), wordCount: 5610 },
    { id: "p4", name: "Data Processing Agreement", version: "v1.0", status: "published", updatedAt: daysAgo(60), wordCount: 3200 },
  ];

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Policy Management" subtitle="Generate, version, and publish compliance policies" dispatch={dispatch} actions={
        <Button icon="✨">Generate with AI</Button>
      } />

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {policies.map(p => (
          <Card key={p.id} style={{ padding: "20px 24px", display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ fontSize: 28 }}>📄</div>
            <div style={{ flex: 1 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900 }}>{p.name}</div>
                <Badge color={colors.slate500} bg={colors.slate100}>{p.version}</Badge>
                <Badge color={p.status === "published" ? colors.teal : colors.amber} bg={p.status === "published" ? colors.tealLight : colors.amberLight}>{p.status === "published" ? "Published" : "Draft"}</Badge>
              </div>
              <div style={{ fontSize: 12, color: colors.slate400 }}>Updated {relativeTime(p.updatedAt)} · {p.wordCount.toLocaleString()} words</div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <Button size="sm" variant="secondary">Edit</Button>
              {p.status === "draft" && <Button size="sm" variant="teal" onClick={() => dispatch({ type: "ADD_TOAST", toast: { type: "success", title: `${p.name} published` } })}>Publish</Button>}
              <Button size="sm" variant="ghost">History</Button>
            </div>
          </Card>
        ))}
      </div>

      <Card style={{ background: colors.electricLight, border: `1px solid ${colors.electric}30` }}>
        <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
          <span style={{ fontSize: 24 }}>✨</span>
          <div>
            <div style={{ fontSize: 14, fontWeight: 700, color: colors.electric, marginBottom: 6 }}>AI Policy Generator</div>
            <div style={{ fontSize: 13, color: colors.slate600, lineHeight: 1.6 }}>Generate a DPDP Act 2023-compliant Privacy Policy, Cookie Policy, or Terms of Service from your business details. The AI drafts, you review and publish — with full version history and rollback.</div>
            <Button style={{ marginTop: 12 }} size="sm">Generate new policy</Button>
          </div>
        </div>
      </Card>
    </div>
  );
}

// ─────────────────────────────────────────────
// SETTINGS PAGE
// ─────────────────────────────────────────────
function SettingsPage({ state, dispatch }) {
  const [activeTab, setActiveTab] = useState("organization");

  return (
    <div style={{ padding: "24px 32px 48px", display: "flex", flexDirection: "column", gap: 20 }}>
      <TopBar title="Settings" subtitle="Manage your organization, team, and preferences" dispatch={dispatch} />

      <Tabs tabs={[{ value: "organization", label: "Organization" }, { value: "security", label: "Security" }, { value: "team", label: "Team & roles" }, { value: "api", label: "API keys" }, { value: "notifications", label: "Notifications" }]} active={activeTab} onChange={setActiveTab} />

      {activeTab === "organization" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Card>
            <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900, marginBottom: 20 }}>Organization details</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <Input label="Organization name" value="Nexus Retail India Pvt Ltd" onChange={() => {}} />
              <Input label="Domain" value="nexusretail.in" onChange={() => {}} />
              <Input label="Country" value="India" onChange={() => {}} />
              <Input label="Industry" value="Retail / E-commerce" onChange={() => {}} />
            </div>
            <div style={{ marginTop: 20 }}><Button>Save changes</Button></div>
          </Card>
          <Card>
            <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900, marginBottom: 16 }}>Compliance settings</div>
            {[["DPDP Act 2023 (India)", true], ["GDPR (EU)", false], ["CCPA (California)", false]].map(([reg, enabled]) => (
              <div key={reg} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 0", borderBottom: `1px solid ${colors.slate100}` }}>
                <div style={{ fontSize: 13, fontWeight: 500, color: colors.slate800 }}>{reg}</div>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  {enabled && <Badge color={colors.teal} bg={colors.tealLight}>Active</Badge>}
                  <div style={{ width: 40, height: 22, borderRadius: 11, background: enabled ? colors.teal : colors.slate200, position: "relative", cursor: "pointer" }}>
                    <div style={{ width: 16, height: 16, borderRadius: "50%", background: "white", position: "absolute", top: 3, left: enabled ? 21 : 3, transition: "left 0.2s" }} />
                  </div>
                </div>
              </div>
            ))}
          </Card>
        </div>
      )}

      {activeTab === "team" && (
        <Card style={{ padding: 0, overflow: "hidden" }}>
          <div style={{ padding: "20px 24px", borderBottom: `1px solid ${colors.slate100}`, display: "flex", justifyContent: "space-between" }}>
            <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900 }}>Team members</div>
            <Button size="sm" icon="＋">Invite member</Button>
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ background: colors.slate50 }}>
                {["Member", "Role", "Status", "Last active", ""].map(h => (
                  <th key={h} style={{ padding: "10px 16px", textAlign: "left", fontSize: 11, fontWeight: 700, color: colors.slate500, textTransform: "uppercase", letterSpacing: 0.5, borderBottom: `1px solid ${colors.slate200}` }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[
                { name: "Admin User", email: "admin@nexusretail.in", role: "Owner", status: "active", last: daysAgo(0.1) },
                { name: "Priya Sharma", email: "priya@nexusretail.in", role: "Compliance Manager", status: "active", last: daysAgo(0.3) },
                { name: "Arjun Mehta", email: "arjun@nexusretail.in", role: "Developer", status: "active", last: daysAgo(0.5) },
                { name: "Kavitha Nair", email: "kavitha@nexusretail.in", role: "Developer", status: "active", last: daysAgo(1.5) },
                { name: "Ravi Kumar", email: "ravi@nexusretail.in", role: "Viewer", status: "invited", last: null },
              ].map((m, i) => (
                <tr key={i} style={{ borderBottom: `1px solid ${colors.slate100}` }}>
                  <td style={{ padding: "12px 16px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <div style={{ width: 32, height: 32, borderRadius: "50%", background: colors.electricLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, color: colors.electric }}>{m.name.charAt(0)}</div>
                      <div>
                        <div style={{ fontWeight: 600, color: colors.slate900 }}>{m.name}</div>
                        <div style={{ fontSize: 11, color: colors.slate400 }}>{m.email}</div>
                      </div>
                    </div>
                  </td>
                  <td style={{ padding: "12px 16px" }}><Badge color={colors.electric} bg={colors.electricLight}>{m.role}</Badge></td>
                  <td style={{ padding: "12px 16px" }}><Badge color={m.status === "active" ? colors.teal : colors.amber}>{m.status}</Badge></td>
                  <td style={{ padding: "12px 16px", color: colors.slate400 }}>{m.last ? relativeTime(m.last) : "—"}</td>
                  <td style={{ padding: "12px 16px" }}>{m.role !== "Owner" && <Button size="sm" variant="ghost">Remove</Button>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}

      {activeTab === "api" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Card>
            <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900, marginBottom: 20 }}>API keys</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {[
                { name: "Production key", key: "armor_live_•••••••••••••••••••••••••••••XdL2", created: daysAgo(30), lastUsed: daysAgo(0.1) },
                { name: "Test key", key: "armor_test_•••••••••••••••••••••••••••••Gh7P", created: daysAgo(30), lastUsed: daysAgo(2) },
              ].map(k => (
                <div key={k.name} style={{ display: "flex", alignItems: "center", gap: 12, padding: "14px 16px", background: colors.slate50, borderRadius: 10, border: `1px solid ${colors.slate200}` }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 13, fontWeight: 600, color: colors.slate900, marginBottom: 2 }}>{k.name}</div>
                    <div style={{ fontSize: 12, fontFamily: "monospace", color: colors.slate500 }}>{k.key}</div>
                    <div style={{ fontSize: 11, color: colors.slate400, marginTop: 2 }}>Created {formatDate(k.created)} · Last used {relativeTime(k.lastUsed)}</div>
                  </div>
                  <Button size="sm" variant="secondary">Revoke</Button>
                </div>
              ))}
            </div>
            <div style={{ marginTop: 16 }}><Button variant="secondary" icon="＋">Generate new key</Button></div>
          </Card>
        </div>
      )}

      {activeTab === "security" && (
        <Card>
          <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900, marginBottom: 20 }}>Security settings</div>
          {[
            { label: "Two-factor authentication", desc: "Require MFA for all team members", enabled: false },
            { label: "SSO with Google Workspace", desc: "Sign in with your Google organization account", enabled: true },
            { label: "Session timeout", desc: "Auto-logout after 8 hours of inactivity", enabled: true },
            { label: "IP allowlist", desc: "Restrict access to specific IP ranges", enabled: false },
          ].map(s => (
            <div key={s.label} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 0", borderBottom: `1px solid ${colors.slate100}` }}>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600, color: colors.slate900 }}>{s.label}</div>
                <div style={{ fontSize: 12, color: colors.slate400, marginTop: 2 }}>{s.desc}</div>
              </div>
              <div style={{ width: 40, height: 22, borderRadius: 11, background: s.enabled ? colors.teal : colors.slate200, position: "relative", cursor: "pointer" }}>
                <div style={{ width: 16, height: 16, borderRadius: "50%", background: "white", position: "absolute", top: 3, left: s.enabled ? 21 : 3 }} />
              </div>
            </div>
          ))}
        </Card>
      )}

      {activeTab === "notifications" && (
        <Card>
          <div style={{ fontSize: 15, fontWeight: 700, color: colors.slate900, marginBottom: 20 }}>Notification preferences</div>
          {[
            { label: "Critical issues detected", email: true, inApp: true },
            { label: "DSAR request submitted", email: true, inApp: true },
            { label: "DSAR deadline approaching (7 days)", email: true, inApp: true },
            { label: "Scan completed", email: false, inApp: true },
            { label: "Policy published", email: false, inApp: true },
            { label: "Weekly compliance digest", email: true, inApp: false },
          ].map(n => (
            <div key={n.label} style={{ display: "flex", alignItems: "center", padding: "12px 0", borderBottom: `1px solid ${colors.slate100}`, gap: 12 }}>
              <div style={{ flex: 1, fontSize: 13, color: colors.slate800 }}>{n.label}</div>
              <div style={{ display: "flex", gap: 20 }}>
                {[["Email", n.email], ["In-app", n.inApp]].map(([ch, on]) => (
                  <div key={ch} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                    <div style={{ width: 32, height: 18, borderRadius: 9, background: on ? colors.electric : colors.slate200, position: "relative", cursor: "pointer" }}>
                      <div style={{ width: 12, height: 12, borderRadius: "50%", background: "white", position: "absolute", top: 3, left: on ? 17 : 3 }} />
                    </div>
                    <span style={{ fontSize: 11, color: colors.slate400 }}>{ch}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </Card>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────
// PAGE ROUTER
// ─────────────────────────────────────────────
function PageContent({ state, dispatch }) {
  const { currentPage } = state;
  const pages = {
    dashboard: DashboardPage,
    websites: WebsitesPage,
    scanner: ScannerPage,
    issues: IssuesPage,
    "action-plan": ActionPlanPage,
    consent: ConsentPage,
    dsar: DSARPage,
    policies: PoliciesPage,
    "audit-logs": AuditLogsPage,
    reports: ReportsPage,
    settings: SettingsPage,
  };
  const Page = pages[currentPage] || DashboardPage;
  return <Page state={state} dispatch={dispatch} />;
}

// ─────────────────────────────────────────────
// ROOT APP
// ─────────────────────────────────────────────
export default function ArmorSolution() {
  const [state, dispatch] = useReducer(appReducer, null, initState);

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        * { box-sizing: border-box; }
        body { margin: 0; font-family: 'Inter', -apple-system, sans-serif; background: #F8FAFC; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes slideInRight { from { transform: translateX(60px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
        table { font-family: 'Inter', sans-serif; }
        input, select, button { font-family: 'Inter', sans-serif; }
      `}</style>

      <div style={{ display: "flex", minHeight: "100vh", background: "#F8FAFC" }}>
        <Sidebar currentPage={state.currentPage} dispatch={dispatch} notifications={state.notifications} />
        <main style={{ flex: 1, minWidth: 0, overflowX: "hidden" }}>
          <PageContent state={state} dispatch={dispatch} />
        </main>
      </div>

      <ToastContainer toasts={state.toasts} dispatch={dispatch} />
    </>
  );
}
