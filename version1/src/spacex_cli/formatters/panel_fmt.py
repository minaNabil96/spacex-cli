from rich.markdown import Markdown
from rich.panel import Panel

from spacex_cli.models.capsule import Capsule
from spacex_cli.models.company import CompanyInfo
from spacex_cli.models.launch import LaunchDetails
from spacex_cli.models.rocket import Rocket


def format_launch_panel(d: LaunchDetails) -> Panel:
    la = d.launch
    content = f"""
**Mission:** {la.name}
**Date (UTC):** {la.date_utc.strftime("%Y-%m-%d %H:%M")}
**Status:** {la.status_name} ({la.status_abbrev})

**Agency:** {d.agency_name} ({d.agency_type or "N/A"})
**Location:** {la.location} | **Pad:** {la.launchpad}

**Mission Details:**
- Name: {d.mission_name or "N/A"}
- Type: {d.mission_type or "N/A"}
- Orbit: {d.orbit or "N/A"}

**Description:**
{d.description or la.details or "No details available."}

**Links:**
- Webcast: [Link]({la.links_webcast or "N/A"})
- Article: [Link]({la.links_article or "N/A"})
"""
    return Panel(Markdown(content), title="🚀 Launch Details", border_style="blue")


def format_rocket_panel(r: Rocket) -> Panel:
    content = f"""
**Name:** {r.full_name}
**Variant:** {r.variant} | **Family:** {r.family}
**Active:** {"✅" if r.active else "❌"} | **Reusable:** {"♻️" if r.reusable else "❌"}
**Maiden Flight:** {r.maiden_flight or "N/A"}

**Capacities:**
- LEO: {r.capacity_leo:,} kg if r.capacity_leo else "N/A"
- GTO: {r.capacity_gto:,} kg if r.capacity_gto else "N/A"

**Dimensions:**
- Height: {r.height or "N/A"} m
- Diameter: {r.diameter or "N/A"} m

**Description:**
{r.description}

**Links:**
- [Wiki]({r.wiki_url or "N/A"}) | [Info]({r.info_url or "N/A"})
"""
    # Fix the conditional string formatting logic
    leo = f"{r.capacity_leo:,} kg" if r.capacity_leo else "N/A"
    gto = f"{r.capacity_gto:,} kg" if r.capacity_gto else "N/A"
    
    content = content.replace('{r.capacity_leo:,} kg if r.capacity_leo else "N/A"', leo)
    content = content.replace('{r.capacity_gto:,} kg if r.capacity_gto else "N/A"', gto)

    return Panel(Markdown(content), title="🛰️ Launcher Specs", border_style="cyan")


def format_capsule_panel(c: Capsule) -> Panel:
    content = f"""
**Name:** {c.name} | **Type:** {c.type}
**Agency:** {c.agency}
**In Use:** {"✅" if c.in_use else "❌"} | **Human Rated:** {"👤" if c.human_rated else "❌"}
**Crew Capacity:** {c.crew_capacity or "N/A"}
**Capability:** {c.capability}

**Maiden Flight:** {c.maiden_flight or "N/A"}
**Dimensions:** {c.height or "N/A"}m (H) x {c.diameter or "N/A"}m (D)

**Links:**
- [Wiki]({c.wiki_url or "N/A"})
"""
    return Panel(Markdown(content), title="🐉 Spacecraft Details", border_style="magenta")


def format_company_panel(c: CompanyInfo) -> Panel:
    content = f"""
**Agency:** {c.name} ({c.abbrev})
**Type:** {c.type} | **Country:** {c.country_code}
**Admin:** {c.administrator} | **Founded:** {c.founding_year}

**Launch Statistics:**
- Total: {c.total_launch_count}
- Success: {c.successful_launches} ({ (c.successful_launches / c.total_launch_count * 100) if c.total_launch_count else 0 :.1f}%)
- Failed: {c.failed_launches}
- Pending: {c.pending_launches}
- Streak: {c.consecutive_successful_launches}

**Inventory:**
- Launchers: {c.launchers}
- Spacecraft: {c.spacecraft}

**Summary:**
{c.description}

**Links:**
- [Wiki]({c.wiki_url or "N/A"}) | [Info]({c.info_url or "N/A"})
"""
    # Fix the percentage calculation logic in string
    success_rate = f"{(c.successful_launches / c.total_launch_count * 100):.1f}%" if c.total_launch_count else "0.0%"
    content = content.replace("({ (c.successful_launches / c.total_launch_count * 100) if c.total_launch_count else 0 :.1f}%)", f"({success_rate})")

    return Panel(Markdown(content), title="🏢 Agency Info", border_style="green")
