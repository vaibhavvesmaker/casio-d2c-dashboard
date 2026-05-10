import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# Casio D2C Growth Intelligence Dashboard
# Streamlit prototype using public Casio context + simulated data
# =========================================================

st.set_page_config(
    page_title="Casio D2C Growth Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: #f4f7fb;
        color: #0f172a;
    }

    header[data-testid="stHeader"] {
        background: #ffffff !important;
        border-bottom: 1px solid #e5e7eb;
        box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04);
    }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 1.3rem;
    }

    .block-container {
        padding-top: 2.1rem;
        padding-left: 2.4rem;
        padding-right: 2.4rem;
        max-width: 1480px;
    }

    h1, h2, h3 {
        color: #0f172a;
        letter-spacing: -0.035em;
    }

    .brand-logo {
        font-size: 30px;
        font-weight: 900;
        color: #003296;
        letter-spacing: 2px;
        margin: 0 0 26px 4px;
    }

    .sidebar-caption {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin: 8px 0 10px 4px;
    }

    /* Real Streamlit radio navigation styling */
    div[role="radiogroup"] label {
        background: transparent;
        padding: 11px 12px;
        border-radius: 12px;
        margin-bottom: 5px;
        min-height: 42px;
        border: 1px solid transparent;
        transition: all 0.15s ease-in-out;
    }

    div[role="radiogroup"] label:hover {
        background: #eef4ff;
        border: 1px solid #dbeafe;
    }

    div[role="radiogroup"] label p {
        font-weight: 750;
        color: #475569;
        font-size: 14px;
    }

    div[role="radiogroup"] label:hover p {
        color: #0057d9;
    }

    div[role="radiogroup"] input:checked + div p {
        color: #0057d9 !important;
        font-weight: 900;
    }

    div[role="radiogroup"] input:checked + div {
        background: #eaf1ff;
        border-radius: 12px;
    }

    .hero {
        background: linear-gradient(135deg, #003296 0%, #0057d9 64%, #0a6cff 100%);
        color: white;
        border-radius: 22px;
        padding: 34px 38px;
        margin-bottom: 24px;
        box-shadow: 0 18px 36px rgba(0, 50, 150, 0.18);
        position: relative;
        overflow: hidden;
    }

    .hero:after {
        content: "";
        position: absolute;
        right: -120px;
        top: -120px;
        width: 420px;
        height: 420px;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
    }

    .hero h1 {
        color: white;
        font-size: 34px;
        line-height: 1.15;
        margin-bottom: 12px;
        position: relative;
        z-index: 2;
    }

    .hero p {
        color: #eaf1ff;
        font-size: 16px;
        max-width: 900px;
        line-height: 1.65;
        position: relative;
        z-index: 2;
    }

    .page-title {
        font-size: 34px;
        font-weight: 900;
        margin: 8px 0 20px 0;
        color: #0f172a;
    }

    .metric-card {
        background: white;
        padding: 23px 22px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        min-height: 158px;
    }

    .metric-icon {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: #eef4ff;
        color: #0057d9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        margin-bottom: 12px;
    }

    .metric-label {
        font-size: 12.5px;
        color: #64748b;
        font-weight: 850;
        letter-spacing: .05em;
        text-transform: uppercase;
    }

    .metric-value {
        font-size: 31px;
        font-weight: 950;
        color: #081f62;
        margin-top: 9px;
        letter-spacing: -0.045em;
    }

    .metric-sub {
        font-size: 13.5px;
        color: #64748b;
        margin-top: 5px;
    }

    .metric-up {
        color: #10b981;
        font-weight: 850;
        margin-top: 11px;
        font-size: 13.5px;
    }

    .metric-down {
        color: #f97316;
        font-weight: 850;
        margin-top: 11px;
        font-size: 13.5px;
    }

    .card {
        background: white;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        padding: 22px;
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 12px;
    }

    .card-subtitle {
        font-size: 13.5px;
        color: #64748b;
        margin-top: -6px;
        margin-bottom: 12px;
    }

    .readout-row {
        display: flex;
        gap: 14px;
        padding: 15px;
        border-radius: 14px;
        margin-bottom: 11px;
        background: #f8fafc;
        color: #1e293b;
        line-height: 1.48;
        border: 1px solid #eef2f7;
    }

    .readout-icon {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        background: #eaf1ff;
        color: #0057d9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        flex-shrink: 0;
    }

    .source-note {
        background: #ffffff;
        border: 1px dashed #94a3b8;
        padding: 18px;
        border-radius: 16px;
        color: #475569;
        font-size: 14px;
        line-height: 1.55;
    }

    .pill {
        display: inline-block;
        background: #eaf1ff;
        color: #0057d9;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 850;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .mini-kpi {
        color: #081f62;
        font-size: 24px;
        font-weight: 950;
        letter-spacing: -0.04em;
    }

    .muted {
        color: #64748b;
        font-size: 13.5px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }

    /* Hide Streamlit footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    /* Styling for the gray container */
    .card {
        background-color: #f8f9fc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        font-family: 'Inter', Arial, sans-serif;
    }
    
    /* Styling for the titles */
    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    
    .card-subtitle {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    
    /* Styling for the flex layout of the rows */
    .readout-row {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #334155;
    }
    
    /* Styling for the icons */
    .readout-icon {
        font-size: 1.2rem;
        margin-right: 0.75rem;
        color: #0f172a;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)
# -----------------------------
# Data: simulated ecommerce metrics
# -----------------------------
data = pd.DataFrame({
    "Category": ["G-SHOCK", "Edifice", "Keyboards", "Calculators"],
    "Sessions": [185000, 72000, 61000, 94000],
    "Product Views": [128000, 51000, 39000, 68000],
    "Add to Cart": [24500, 8500, 6400, 11200],
    "Purchases": [8200, 2700, 1800, 4600],
    "Revenue": [1476000, 567000, 540000, 276000],
    "AOV": [180, 210, 300, 60],
    "Marketing Spend": [280000, 95000, 110000, 45000],
    "Repeat Purchase Rate": [0.31, 0.24, 0.18, 0.28]
})

data["Conversion Rate"] = data["Purchases"] / data["Sessions"]
data["ROAS"] = data["Revenue"] / data["Marketing Spend"]
data["Revenue Share"] = data["Revenue"] / data["Revenue"].sum()
data["Product View Rate"] = data["Product Views"] / data["Sessions"]
data["Cart Rate"] = data["Add to Cart"] / data["Product Views"]
data["Checkout Completion"] = data["Purchases"] / data["Add to Cart"]

months = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [305000, 382000, 515000, 438000, 528000, 558000],
    "Conversion Rate": [0.031, 0.038, 0.042, 0.038, 0.043, 0.045],
    "Sessions": [58000, 65000, 76000, 68000, 72000, 73000]
})

channel = pd.DataFrame({
    "Channel": ["Paid Search", "Organic", "Email", "Social", "Referral"],
    "Revenue": [820000, 640000, 560000, 390000, 449000],
    "Spend": [210000, 45000, 52000, 120000, 103000],
    "Conversion Rate": [0.039, 0.046, 0.058, 0.026, 0.041]
})
channel["ROAS"] = channel["Revenue"] / channel["Spend"]

segments = pd.DataFrame({
    "Segment": ["Collectors", "Students", "Gift Buyers", "Musicians", "First-time Visitors"],
    "Users": [42000, 68000, 31000, 24000, 118000],
    "AOV": [245, 72, 135, 310, 95],
    "Conversion Rate": [0.061, 0.044, 0.035, 0.031, 0.021],
    "Primary Category": ["G-SHOCK", "Calculators", "G-SHOCK", "Keyboards", "Mixed"]
})

forecast = pd.DataFrame({
    "Month": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "Base Forecast": [575000, 640000, 610000, 690000, 820000, 910000],
    "Upside Scenario": [620000, 710000, 680000, 780000, 940000, 1050000],
    "Conservative Scenario": [520000, 580000, 560000, 610000, 720000, 790000]
})

# -----------------------------
# Helper functions
# -----------------------------
def money(x):
    return f"${x:,.0f}"


def number(x):
    return f"{x:,.0f}"


def percent(x):
    return f"{x * 100:.2f}%"


def compact_money(x):
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.2f}M"
    if abs(x) >= 1_000:
        return f"${x/1_000:.0f}K"
    return money(x)


def chart_layout(fig, height=None):
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=18, r=18, t=18, b=18),
        font=dict(color="#334155", family="Inter, Arial, sans-serif"),
        xaxis=dict(
            showgrid=False,
            linecolor="#e5e7eb",
            tickfont=dict(color="#64748b")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#eef2f7",
            gridwidth=1,
            zeroline=False,
            tickfont=dict(color="#64748b")
        )
    )
    if height:
        fig.update_layout(height=height)
    return fig


def metric_card(col, icon, label, value, sub, delta, delta_type="up"):
    delta_class = "metric-up" if delta_type == "up" else "metric-down"
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
        <div class="{delta_class}">{delta}</div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# Sidebar: real navigation
# -----------------------------
with st.sidebar:
    st.markdown('<div class="brand-logo">CASIO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-caption">Dashboard Sections</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "📊 Executive Overview",
            "📦 Product Performance",
            "🔎 Funnel Analysis",
            "🧪 CRO Roadmap",
            "👥 Customer Insights",
            "📈 Marketing Performance",
            "🔮 Forecasting",
            "📚 Sources & Assumptions"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <div class="card-title">Data Refresh</div>
        <div class="muted">Last updated</div>
        <div style="color:#0057d9;font-weight:900;margin-top:6px;">Jun 3, 2025 10:30 AM</div>
        <div style="margin-top:12px;">
            <span class="pill">Prototype</span>
            <span class="pill">Simulated</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Hero shown on all pages
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>Casio D2C Growth Intelligence Dashboard</h1>
    <p>
        Prototype analytics command center for North America D2C performance, connecting revenue,
        conversion, customer behavior, product categories, marketing effectiveness, forecasting, and CRO opportunities.
        Built with public Casio business context and simulated ecommerce data.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Executive Overview
# -----------------------------
if page == "📊 Executive Overview":
    st.markdown('<div class="page-title">Executive Overview</div>', unsafe_allow_html=True)

    total_revenue = data["Revenue"].sum()
    total_sessions = data["Sessions"].sum()
    conversion_rate = data["Purchases"].sum() / data["Sessions"].sum()
    aov = total_revenue / data["Purchases"].sum()
    roas = total_revenue / data["Marketing Spend"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    metric_card(c1, "$", "Revenue", money(total_revenue), "Simulated D2C total", "↑ 8.2% vs May 1 – May 31")
    metric_card(c2, "👥", "Sessions", number(total_sessions), "Total traffic", "↑ 5.6% vs May 1 – May 31")
    metric_card(c3, "↗", "Conversion Rate", percent(conversion_rate), "Purchase / session", "↑ 0.41 pp vs May 1 – May 31")
    metric_card(c4, "🛍", "AOV", money(aov), "Revenue / order", "↑ 6.3% vs May 1 – May 31")
    metric_card(c5, "◎", "ROAS", f"{roas:.2f}x", "Revenue / spend", "↑ 7.8% vs May 1 – May 31")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="card"><div class="card-title">Revenue Trend (Simulated)</div><div class="card-subtitle">Monthly revenue trend used to frame growth momentum.</div>', unsafe_allow_html=True)
        fig = px.line(months, x="Month", y="Revenue", markers=True)
        fig.update_traces(line=dict(color="#0057d9", width=3), marker=dict(size=8, color="#0057d9"))
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        fig = chart_layout(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><div class="card-title">Conversion Rate Trend (Simulated)</div><div class="card-subtitle">Conversion trend to support CRO prioritization.</div>', unsafe_allow_html=True)
        fig = px.line(months, x="Month", y="Conversion Rate", markers=True)
        fig.update_traces(line=dict(color="#0057d9", width=3), marker=dict(size=8, color="#0057d9"))
        fig.update_yaxes(tickformat=".1%")
        fig = chart_layout(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        # -----------------------------
    # Revenue Mix + Executive Readout
    # FIXED:
    # Do NOT wrap st.plotly_chart or st.dataframe inside custom <div class="card">.
    # Streamlit breaks custom HTML wrappers around native components.
    # Use st.container(border=True) for Streamlit charts/tables.
    # Use pure HTML only for the Executive Readout card.
    # -----------------------------

    left, right = st.columns([1.05, 1])

    with left:
        with st.container(border=True):
            st.markdown("### Revenue Mix by Category")
            st.caption("Category contribution to simulated D2C revenue.")

            fig = go.Figure(data=[go.Pie(
                labels=data["Category"],
                values=data["Revenue"],
                hole=.60,
                marker=dict(colors=["#003296", "#0057d9", "#6ea8fe", "#ff7a00"]),
                textinfo="none"
            )])

            fig.update_layout(
                showlegend=True,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="white",
                height=320,
                font=dict(color="#334155", family="Inter, Arial, sans-serif"),
                annotations=[dict(
                    text=f"<b>{compact_money(total_revenue)}</b><br><span style='font-size:13px;color:#64748b'>Total Revenue</span>",
                    x=0.5,
                    y=0.5,
                    font_size=20,
                    showarrow=False
                )]
            )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            mix = data[["Category", "Revenue", "Revenue Share"]].copy()
            mix["Revenue"] = mix["Revenue"].map(money)
            mix["Revenue Share"] = mix["Revenue Share"].map(lambda x: f"{x*100:.1f}%")
            st.dataframe(mix, use_container_width=True, hide_index=True)

    # with right:
    #     # FIXED:
    #     # This card is pure HTML, so unsafe_allow_html=True works correctly.
    #     # Also fixed indentation under "with right:".
    #     st.markdown("""
    #     <div class="card">
    #         <div class="card-title">Executive Readout</div>
    #         <div class="card-subtitle">Decision-oriented interpretation of simulated performance.</div>

    #         <div class="readout-row">
    #             <div class="readout-icon">↗</div>
    #             <div><b>Growth engine:</b> G-SHOCK contributes the largest simulated revenue share, making it the first category to prioritize for CRO and launch-flow testing.</div>
    #         </div>

    #         <div class="readout-row">
    #             <div class="readout-icon">◎</div>
    #             <div><b>Margin opportunity:</b> Keyboards show the highest AOV but lower conversion, suggesting a need for comparison content, financing CTAs, or guided buying.</div>
    #         </div>

    #         <div class="readout-row">
    #             <div class="readout-icon">☑</div>
    #             <div><b>Seasonality watch:</b> Calculators likely require a demand-planning lens around back-to-school cycles.</div>
    #         </div>
    #     </div>
    #     """, unsafe_allow_html=True)
        with right:
         st.markdown("""<div class="card">
<div class="card-title">Executive Readout</div>
<div class="card-subtitle">Decision-oriented interpretation of simulated performance.</div>
<div class="readout-row">
<div class="readout-icon">↗</div>
<div><b>Growth engine:</b> G-SHOCK contributes the largest simulated revenue share, making it the first category to prioritize for CRO and launch-flow testing.</div>
</div>
<div class="readout-row">
<div class="readout-icon">◎</div>
<div><b>Margin opportunity:</b> Keyboards show the highest AOV but lower conversion, suggesting a need for comparison content, financing CTAs, or guided buying.</div>
</div>
<div class="readout-row">
<div class="readout-icon">☑</div>
<div><b>Seasonality watch:</b> Calculators likely require a demand-planning lens around back-to-school cycles.</div>
</div>
</div>""", unsafe_allow_html=True)
# -----------------------------
# Product Performance
# -----------------------------
elif page == "📦 Product Performance":
    st.markdown('<div class="page-title">Product Performance</div>', unsafe_allow_html=True)

    display_df = data.copy()
    for col in ["Sessions", "Product Views", "Add to Cart", "Purchases"]:
        display_df[col] = display_df[col].map(number)
    for col in ["Revenue", "AOV", "Marketing Spend"]:
        display_df[col] = display_df[col].map(money)
    for col in ["Conversion Rate", "Revenue Share", "Product View Rate", "Cart Rate", "Checkout Completion", "Repeat Purchase Rate"]:
        display_df[col] = display_df[col].map(percent)
    display_df["ROAS"] = display_df["ROAS"].map(lambda x: f"{x:.2f}x")

    st.markdown('<div class="card"><div class="card-title">Category Performance Table</div>', unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="card"><div class="card-title">Conversion Rate by Category</div>', unsafe_allow_html=True)
        fig = px.bar(data, x="Category", y="Conversion Rate", text=data["Conversion Rate"].map(lambda x: f"{x*100:.2f}%"), color="Category", color_discrete_sequence=["#003296", "#0057d9", "#6ea8fe", "#ff7a00"])
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        fig.update_yaxes(tickformat=".1%")
        fig = chart_layout(fig, height=340)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><div class="card-title">ROAS by Category</div>', unsafe_allow_html=True)
        fig = px.bar(data, x="Category", y="ROAS", text=data["ROAS"].map(lambda x: f"{x:.2f}x"), color="Category", color_discrete_sequence=["#003296", "#0057d9", "#6ea8fe", "#ff7a00"])
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        fig = chart_layout(fig, height=340)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Funnel Analysis
# -----------------------------
elif page == "🔎 Funnel Analysis":
    st.markdown('<div class="page-title">Funnel Analysis</div>', unsafe_allow_html=True)

    selected_category = st.selectbox("Select product category", data["Category"])
    row = data[data["Category"] == selected_category].iloc[0]

    f1, f2, f3 = st.columns(3)
    metric_card(f1, "👁", "Product View Rate", percent(row["Product View Rate"]), "Product views / sessions", "Diagnostic metric")
    metric_card(f2, "🛒", "Cart Rate", percent(row["Cart Rate"]), "Add to cart / product views", "Friction indicator")
    metric_card(f3, "✅", "Checkout Completion", percent(row["Checkout Completion"]), "Purchases / add to cart", "Purchase readiness")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="card-title">Customer Journey Funnel</div>', unsafe_allow_html=True)

    funnel = pd.DataFrame({
        "Stage": ["Sessions", "Product Views", "Add to Cart", "Purchases"],
        "Users": [row["Sessions"], row["Product Views"], row["Add to Cart"], row["Purchases"]]
    })
    fig = px.funnel(funnel, x="Users", y="Stage", title=f"{selected_category} Funnel", color_discrete_sequence=["#0057d9"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#334155", family="Inter, Arial, sans-serif"), margin=dict(l=20, r=20, t=45, b=20), height=430)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# CRO Roadmap
# -----------------------------
elif page == "🧪 CRO Roadmap":
    st.markdown('<div class="page-title">CRO & A/B Testing Roadmap</div>', unsafe_allow_html=True)

    tests = pd.DataFrame({
        "Priority": ["P1", "P1", "P2", "P2"],
        "Test": [
            "G-SHOCK Limited Edition PDP Messaging",
            "Keyboard Guided Buying / Financing CTA",
            "Calculator Back-to-School Bundle",
            "Edifice Product Comparison Module"
        ],
        "Hypothesis": [
            "Scarcity and launch storytelling will increase add-to-cart rate.",
            "Guided product education and financing language will reduce hesitation on high-AOV items.",
            "Bundling calculators with accessories will increase AOV during seasonal periods.",
            "Comparison content will improve confidence and product-page conversion."
        ],
        "Primary Metric": ["Add-to-cart rate", "Checkout conversion", "AOV", "Product-page conversion"],
        "Business Impact": ["Revenue growth", "High-AOV conversion lift", "Seasonal demand capture", "Category education"]
    })

    st.markdown('<div class="card"><div class="card-title">Test Backlog</div>', unsafe_allow_html=True)
    st.dataframe(tests, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Recommended Test-and-Learn Framework</div>
        <div class="readout-row"><div class="readout-icon">1</div><div><b>Define business question:</b> Where is the largest revenue, AOV, or conversion friction?</div></div>
        <div class="readout-row"><div class="readout-icon">2</div><div><b>Form hypothesis:</b> What customer behavior should change and why?</div></div>
        <div class="readout-row"><div class="readout-icon">3</div><div><b>Select metric:</b> Conversion rate, AOV, cart rate, checkout completion, or ROAS.</div></div>
        <div class="readout-row"><div class="readout-icon">4</div><div><b>Run controlled experiment:</b> Test variation against baseline and define success thresholds upfront.</div></div>
        <div class="readout-row"><div class="readout-icon">5</div><div><b>Scale winning experience:</b> Document learnings and apply across relevant categories.</div></div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Customer Insights
# -----------------------------
elif page == "👥 Customer Insights":
    st.markdown('<div class="page-title">Customer Insights</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Segment Performance</div><div class="card-subtitle">Simulated segmentation view to show how customer behavior could inform merchandising and CRM.</div>', unsafe_allow_html=True)
    seg_display = segments.copy()
    seg_display["Users"] = seg_display["Users"].map(number)
    seg_display["AOV"] = seg_display["AOV"].map(money)
    seg_display["Conversion Rate"] = seg_display["Conversion Rate"].map(percent)
    st.dataframe(seg_display, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="card"><div class="card-title">Segment Conversion Rate</div>', unsafe_allow_html=True)
        fig = px.bar(segments, x="Segment", y="Conversion Rate", text=segments["Conversion Rate"].map(lambda x: f"{x*100:.1f}%"), color="Primary Category", color_discrete_sequence=["#003296", "#0057d9", "#6ea8fe", "#ff7a00", "#94a3b8"])
        fig.update_traces(textposition="outside")
        fig.update_yaxes(tickformat=".1%")
        fig = chart_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Segment Readout</div>
            <div class="readout-row"><div class="readout-icon">★</div><div><b>Collectors:</b> Highest simulated conversion rate, suggesting strong launch, limited-edition, and loyalty potential.</div></div>
            <div class="readout-row"><div class="readout-icon">🎓</div><div><b>Students:</b> Strong seasonal demand potential tied to calculators and back-to-school campaign planning.</div></div>
            <div class="readout-row"><div class="readout-icon">🎹</div><div><b>Musicians:</b> High AOV, but likely needs stronger product education and comparison tools.</div></div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Marketing Performance
# -----------------------------
elif page == "📈 Marketing Performance":
    st.markdown('<div class="page-title">Marketing Performance</div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="card"><div class="card-title">Revenue by Channel</div>', unsafe_allow_html=True)
        fig = px.bar(channel, x="Channel", y="Revenue", text=channel["Revenue"].map(money), color="Channel", color_discrete_sequence=["#003296", "#0057d9", "#6ea8fe", "#ff7a00", "#94a3b8"])
        fig.update_traces(textposition="outside")
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")
        fig.update_layout(showlegend=False)
        fig = chart_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><div class="card-title">ROAS by Channel</div>', unsafe_allow_html=True)
        fig = px.bar(channel, x="Channel", y="ROAS", text=channel["ROAS"].map(lambda x: f"{x:.2f}x"), color="Channel", color_discrete_sequence=["#003296", "#0057d9", "#6ea8fe", "#ff7a00", "#94a3b8"])
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
        fig = chart_layout(fig, height=360)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Channel Performance Table</div>', unsafe_allow_html=True)
    channel_display = channel.copy()
    channel_display["Revenue"] = channel_display["Revenue"].map(money)
    channel_display["Spend"] = channel_display["Spend"].map(money)
    channel_display["Conversion Rate"] = channel_display["Conversion Rate"].map(percent)
    channel_display["ROAS"] = channel_display["ROAS"].map(lambda x: f"{x:.2f}x")
    st.dataframe(channel_display, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Forecasting
# -----------------------------
elif page == "🔮 Forecasting":
    st.markdown('<div class="page-title">Forecasting</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Revenue Forecast Scenarios</div><div class="card-subtitle">Simulated scenario model for demand planning and executive conversations.</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast["Month"], y=forecast["Base Forecast"], mode="lines+markers", name="Base Forecast", line=dict(color="#0057d9", width=3)))
    fig.add_trace(go.Scatter(x=forecast["Month"], y=forecast["Upside Scenario"], mode="lines+markers", name="Upside Scenario", line=dict(color="#10b981", width=3)))
    fig.add_trace(go.Scatter(x=forecast["Month"], y=forecast["Conservative Scenario"], mode="lines+markers", name="Conservative Scenario", line=dict(color="#f97316", width=3)))
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    fig = chart_layout(fig, height=420)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    fdisplay = forecast.copy()
    for col in ["Base Forecast", "Upside Scenario", "Conservative Scenario"]:
        fdisplay[col] = fdisplay[col].map(money)
    st.markdown('<div class="card"><div class="card-title">Forecast Table</div>', unsafe_allow_html=True)
    st.dataframe(fdisplay, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Sources & Assumptions
# -----------------------------
elif page == "📚 Sources & Assumptions":
    st.markdown('<div class="page-title">Sources & Assumptions</div>', unsafe_allow_html=True)

    source_data = pd.DataFrame({
        "Source Area": [
            "FY2025 consolidated net sales",
            "FY2025 timepiece sales",
            "FY2025 consumer sales",
            "North America performance",
            "Product category structure"
        ],
        "Public Context Used": [
            "Casio reported FY2025 consolidated sales of ¥261.7B.",
            "Casio reported Timepiece segment sales of ¥166.1B.",
            "Casio reported Consumer segment sales of ¥82.0B.",
            "Casio reported positive North America performance in FY2025 briefing materials.",
            "Casio U.S. site shows major D2C product categories including watches, calculators, and musical instruments."
        ],
        "Source": [
            "Casio FY2025 Consolidated Financial Results",
            "Casio FY2025 Consolidated Financial Results",
            "Casio FY2025 Consolidated Financial Results",
            "Casio FY2025 Results Briefing",
            "Casio U.S. Official Website"
        ]
    })

    st.markdown('<div class="card"><div class="card-title">Public Source Context</div>', unsafe_allow_html=True)
    st.dataframe(source_data, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="source-note">
        <b>Important prototype note:</b><br>
        This dashboard does not use Casio internal ecommerce data. Revenue, funnel, conversion,
        AOV, ROAS, customer segment, marketing, and forecast metrics are simulated for demonstration purposes.
        The purpose is to show how a D2C Analytics & Insights Manager could structure reporting,
        diagnose performance, and translate customer behavior into commercial recommendations.
        <br><br>
        <b>Interview framing:</b> “Since internal D2C data is private, I used public company context and simulated funnel data to demonstrate the analytics framework, business questions, and decision-support layer I would build.”
    </div>
    """, unsafe_allow_html=True)
