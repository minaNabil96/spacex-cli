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
**Status:** {"✅ Success" if la.success else ("❌ Failure" if la.success is False else "⏳ Pending")}

**Payload:**
- Mass: {d.payload_mass_kg or "N/A"} kg / {d.payload_mass_lbs or "N/A"} lbs
- Orbit: {d.orbit or "N/A"}
- Customers: {", ".join(d.customers) if d.customers else "N/A"}

**Details:**
{la.details or "No details available."}

**Links:**
- Webcast: {la.links_webcast or "N/A"}
- Article: {la.links_article or "N/A"}
"""
    return Panel(Markdown(content), title=f"🚀 Launch Details [{la.id}]", border_style="blue")


def format_rocket_panel(r: Rocket) -> Panel:
    content = f"""
**Name:** {r.name} | **Type:** {r.type}
**Active:** {"✅" if r.active else "❌"} | **Stages:** {r.stages} | **Boosters:** {r.boosters}
**Success Rate:** {r.success_rate_pct}% | **Cost/Launch:** ${r.cost_per_launch:,}
**First Flight:** {r.first_flight or "N/A"} | **Country:** {r.country}

**Dimensions:**
- Height: {r.height.get("meters", "N/A")} m
- Diameter: {r.diameter.get("meters", "N/A")} m
- Mass: {r.mass.get("kg", "N/A")} kg

**Description:**
{r.description}
"""
    return Panel(Markdown(content), title=f"🛰️ Rocket Specs [{r.id}]", border_style="cyan")


def format_capsule_panel(c: Capsule) -> Panel:
    content = f"""
**Serial:** {c.serial} | **Type:** {c.type}
**Status:** {c.status}
**Reuse Count:** {c.reuse_count}
**Water Landings:** {c.water_landings} | **Land Landings:** {c.land_landings}

**Last Update:**
{c.last_update or "No updates available."}
"""
    return Panel(Markdown(content), title=f"🐉 Capsule Details [{c.id}]", border_style="magenta")


def format_company_panel(c: CompanyInfo) -> Panel:
    content = f"""
**Company:** {c.name} | **Founded:** {c.founded} by {c.founder}
**Employees:** {c.employees:,} | **Valuation:** ${c.valuation:,}

**Leadership:** CEO {c.ceo} | CTO {c.cto} | COO {c.coo}

**Infrastructure:**
- Vehicles: {c.vehicles}
- Launch Sites: {c.launch_sites}
- Test Sites: {c.test_sites}

**HQ:** {c.headquarters.get("city", "")}, {c.headquarters.get("state", "")},
{c.headquarters.get("address", "")}

**Summary:**
{c.summary}
"""
    return Panel(Markdown(content), title="🏢 SpaceX Company Info", border_style="green")
