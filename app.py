import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlparse
from duckduckgo_search import DDGS

st.set_page_config(page_title="Off-Page SEO Backlink Finder", page_icon="🔗", layout="wide")

st.title("🔗 Off-Page SEO High-DA Backlink Finder")
st.caption("Find verified High-DA free backlink sites and discover live niche-specific link-building opportunities.")

# Curated Database of Verified High-DA Free Backlink Sites
VERIFIED_SITES = [
    {"Site": "GitHub", "DA": 96, "Spam": "1%", "Type": "Profile / Repo Link", "Link_Type": "NoFollow", "Niche": "Tech / General", "URL": "https://github.com/"},
    {"Site": "Medium", "DA": 95, "Spam": "1%", "Type": "Web 2.0 / Article", "Link_Type": "NoFollow", "Niche": "All Niches", "URL": "https://medium.com/"},
    {"Site": "Sites.Google", "DA": 97, "Spam": "1%", "Type": "Web 2.0", "Link_Type": "DoFollow", "Niche": "All Niches", "URL": "https://sites.google.com/"},
    {"Site": "Trustpilot", "DA": 93, "Spam": "1%", "Type": "Business Directory", "Link_Type": "NoFollow", "Niche": "Business / SaaS / E-com", "URL": "https://www.trustpilot.com/"},
    {"Site": "Crunchbase", "DA": 91, "Spam": "1%", "Type": "Business Directory", "Link_Type": "NoFollow", "Niche": "Startups / Business", "URL": "https://www.crunchbase.com/"},
    {"Site": "WordPress.com", "DA": 94, "Spam": "1%", "Type": "Web 2.0", "Link_Type": "DoFollow", "Niche": "All Niches", "URL": "https://wordpress.com/"},
    {"Site": "Blogger", "DA": 99, "Spam": "1%", "Type": "Web 2.0", "Link_Type": "DoFollow", "Niche": "All Niches", "URL": "https://www.blogger.com/"},
    {"Site": "HubPages", "DA": 93, "Spam": "2%", "Type": "Guest Article", "Link_Type": "DoFollow", "Niche": "General / How-To", "URL": "https://discover.hubpages.com/"},
    {"Site": "Product Hunt", "DA": 91, "Spam": "1%", "Type": "Product Directory", "Link_Type": "DoFollow", "Niche": "Tech / Tools / SaaS", "URL": "https://www.producthunt.com/"},
    {"Site": "Behance", "DA": 92, "Spam": "1%", "Type": "Profile Creation", "Link_Type": "DoFollow", "Niche": "Design / Agency / Creative", "URL": "https://www.behance.net/"},
    {"Site": "Dribbble", "DA": 92, "Spam": "1%", "Type": "Profile Creation", "Link_Type": "NoFollow", "Niche": "Design / Tech / Agency", "URL": "https://dribbble.com/"},
    {"Site": "Dev.to", "DA": 84, "Spam": "1%", "Type": "Guest Post / Article", "Link_Type": "DoFollow", "Niche": "Tech / Coding / SaaS", "URL": "https://dev.to/"},
    {"Site": "HackerNoon", "DA": 88, "Spam": "1%", "Type": "Guest Post / Article", "Link_Type": "DoFollow (Bio)", "Niche": "Tech / Startups / AI", "URL": "https://hackernoon.com/"},
    {"Site": "Hashnode", "DA": 78, "Spam": "1%", "Type": "Web 2.0 / Tech Blog", "Link_Type": "DoFollow", "Niche": "Tech / Development", "URL": "https://hashnode.com/"},
    {"Site": "G2", "DA": 80, "Spam": "1%", "Type": "Business Directory", "Link_Type": "NoFollow", "Niche": "Software / B2B Services", "URL": "https://www.g2.com/"},
    {"Site": "Hotfrog", "DA": 81, "Spam": "2%", "Type": "Business Directory", "Link_Type": "NoFollow", "Niche": "Local Business / Services", "URL": "https://www.hotfrog.com/"},
    {"Site": "PRLog", "DA": 76, "Spam": "2%", "Type": "Free Press Release", "Link_Type": "NoFollow", "Niche": "Business / News", "URL": "https://www.prlog.org/"},
    {"Site": "About.me", "DA": 90, "Spam": "1%", "Type": "Profile Creation", "Link_Type": "DoFollow", "Niche": "Personal / Founders", "URL": "https://about.me/"},
    {"Site": "Linktree", "DA": 93, "Spam": "1%", "Type": "Profile / Social Bio", "Link_Type": "DoFollow", "Niche": "All Niches", "URL": "https://linktr.ee/"},
    {"Site": "AlternativeTo", "DA": 84, "Spam": "1%", "Type": "Product Directory", "Link_Type": "NoFollow", "Niche": "Apps / Software / Web Tools", "URL": "https://alternativeto.net/"},
    {"Site": "Storeboard", "DA": 64, "Spam": "3%", "Type": "Business Directory", "Link_Type": "DoFollow", "Niche": "Business / E-com", "URL": "https://www.storeboard.com/"},
    {"Site": "IndiBlogHub", "DA": 62, "Spam": "2%", "Type": "Blog Directory / Guest Post", "Link_Type": "DoFollow", "Niche": "India / Blogging / General", "URL": "https://indibloghub.com/"},
    {"Site": "Justdial", "DA": 82, "Spam": "1%", "Type": "Local Citation", "Link_Type": "NoFollow", "Niche": "India Local Business", "URL": "https://www.justdial.com/"},
    {"Site": "IndiaMART", "DA": 79, "Spam": "1%", "Type": "Business Directory", "Link_Type": "NoFollow", "Niche": "B2B / Suppliers", "URL": "https://www.indiamart.com/"}
]

# Sidebar for optional free OpenPageRank API Key
with st.sidebar:
    st.header("⚙️ Live DA Score Settings")
    opr_api_key = st.text_input(
        "OpenPageRank API Key (Optional)",
        type="password",
        help="Get a free API key at domcop.com/openpagerank to fetch live Domain Authority scores (0-100) for any searched site."
    )
    st.caption("💡 Without a key, Tab 1 shows verified DA scores, and Tab 2 still finds live niche backlink opportunities.")

def get_live_authority(domains, api_key):
    """Fetches free Domain Authority equivalent (0-100) via OpenPageRank API."""
    if not api_key or not domains:
        return {}
    url = "https://openpagerank.com/api/v1.0/getPageRank"
    headers = {"API-OPR": api_key}
    params = [("domains[]", d) for d in domains[:40]]
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get("response", [])
            return {item["domain"]: round(float(item.get("page_rank_decimal") or 0) * 10) for item in data}
    except Exception:
        pass
    return {}

tab1, tab2 = st.tabs(["🏆 Verified High-DA Backlink Vault", "🔍 Live Niche Backlink Harvester"])

# TAB 1: CURATED HIGH-DA SITES
with tab1:
    st.subheader("Verified High-DA Free Backlink Submission Sites")
    df_verified = pd.DataFrame(VERIFIED_SITES)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        min_da = st.slider("Minimum DA Score", 50, 95, 60)
    with c2:
        link_filter = st.multiselect("Link Type", ["DoFollow", "NoFollow", "DoFollow (Bio)"], default=["DoFollow", "NoFollow", "DoFollow (Bio)"])
    with c3:
        cat_filter = st.multiselect("Category", df_verified["Type"].unique(), default=df_verified["Type"].unique())
    with c4:
        search_txt = st.text_input("Search by Niche or Name", placeholder="e.g., Tech, India, Business")

    filtered = df_verified[
        (df_verified["DA"] >= min_da) &
        (df_verified["Link_Type"].isin(link_filter)) &
        (df_verified["Type"].isin(cat_filter))
    ]
    if search_txt:
        filtered = filtered[
            filtered["Site"].str.contains(search_txt, case=False) |
            filtered["Niche"].str.contains(search_txt, case=False)
        ]

    filtered = filtered.sort_values(by="DA", ascending=False)
    st.write(f"Showing **{len(filtered)}** verified high-authority platforms:")

    for _, row in filtered.iterrows():
        with st.container(border=True):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                badge = "🟢 DoFollow" if "DoFollow" in row["Link_Type"] else "🔵 NoFollow"
                st.markdown(f"### {row['Site']} &nbsp; `{badge}` &nbsp; `DA: {row['DA']}`")
                st.markdown(f"**Category:** {row['Type']} &nbsp;•&nbsp; **Best For:** {row['Niche']} &nbsp;•&nbsp; **Spam Score:** {row['Spam']}")
            with col_b:
                st.write("")
                st.link_button("🚀 Go to Site", row["URL"], use_container_width=True, type="primary")

# TAB 2: LIVE NICHE BACKLINK FINDER
with tab2:
    st.subheader("Find Live Backlink Opportunities in Your Exact Niche")
    st.write("Uses SEO search footprints to find blogs, directories, and resource pages accepting submissions in your industry.")

    with st.form("niche_search"):
        sc1, sc2, sc3 = st.columns([3, 3, 1])
        with sc1:
            niche = st.text_input("Your Keyword / Niche", placeholder="e.g., SaaS, Fitness, Interior Design, EdTech")
        with sc2:
            strategy = st.selectbox(
                "Backlink Strategy (Search Footprint)",
                options=[
                    "Guest Post ('write for us')",
                    "Guest Post ('submit a guest post')",
                    "Resource Page ('useful links' OR 'resources')",
                    "Niche Directory ('add url' OR 'submit site')",
                    "Blog Comments / Discussions ('leave a reply')"
                ]
            )
        with sc3:
            max_res = st.number_input("Max Results", min_value=5, max_value=30, value=15)

        find_btn = st.form_submit_button("🔍 Harvest Backlink Sites", type="primary", use_container_width=True)

    if find_btn:
        if not niche.strip():
            st.warning("Please enter your niche or keyword first.")
        else:
            footprint_map = {
                "Guest Post ('write for us')": f'{niche} "write for us" OR "become a contributor"',
                "Guest Post ('submit a guest post')": f'{niche} "submit a guest post" OR "guest post guidelines"',
                "Resource Page ('useful links' OR 'resources')": f'{niche} intitle:resources "useful links" OR "submit resource"',
                "Niche Directory ('add url' OR 'submit site')": f'{niche} "submit site" OR "add url" directory',
                "Blog Comments / Discussions ('leave a reply')": f'{niche} blog "leave a reply" -"comments are closed"'
            }
            query = footprint_map[strategy]

            with st.spinner(f"Scanning the web for: `{query}` ..."):
                try:
                    results = list(DDGS().text(query, max_results=max_res))
                    if not results:
                        st.info("No results returned right now. Try a broader niche keyword.")
                    else:
                        domains = [urlparse(r["href"]).netloc.replace("www.", "") for r in results]
                        da_scores = get_live_authority(domains, opr_api_key)

                        st.success(f"Found {len(results)} live link-building pages for '{niche}'!")
                        for r in results:
                            domain = urlparse(r["href"]).netloc.replace("www.", "")
                            da_val = da_scores.get(domain, "Add Free API Key in Sidebar")
                            da_badge = f"⚡ Authority Score: {da_val}/100" if isinstance(da_val, int) else "🌐 Live Opportunity"

                            with st.container(border=True):
                                c1, c2 = st.columns([4, 1])
                                with c1:
                                    st.markdown(f"#### {r['title']}")
                                    st.markdown(f"🌐 **Domain:** `{domain}` &nbsp;•&nbsp; `{da_badge}`")
                                    st.caption(r.get("body", ""))
                                with c2:
                                    st.write("")
                                    st.link_button("🔗 Open Page", r["href"], use_container_width=True)
                except Exception as e:
                    st.error(f"Search error: {e}")
