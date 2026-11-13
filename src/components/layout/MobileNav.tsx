// SPDX-License-Identifier: AGPL-3.0-or-later

import { Mic, History, LayoutTemplate, Settings, BarChart2 } from "lucide-react";
import { NavLink } from "react-router-dom";
import { useLang } from "../../lib/useLang";
import type { LangKey } from "../../lib/i18n";

type Item = { to: string; icon: React.ElementType; key: LangKey };

// Five tabs, the record button sits raised in the middle.
const LEFT: Item[] = [
  { to: "/history", icon: History, key: "nav_history" },
  { to: "/templates", icon: LayoutTemplate, key: "nav_templates" },
];
const RIGHT: Item[] = [
  { to: "/analytics", icon: BarChart2, key: "nav_analytics" },
  { to: "/settings", icon: Settings, key: "nav_settings" },
];

function Tab({ to, icon: Icon, label }: { to: string; icon: React.ElementType; label: string }) {
  return (
    <NavLink to={to} className={({ isActive }) => `m-tab${isActive ? " active" : ""}`}>
      <span className="m-tab-ico">
        <Icon size={21} strokeWidth={1.9} />
      </span>
      <span className="m-tab-label">{label}</span>
    </NavLink>
  );
}

export function MobileNav() {
  const { t } = useLang();
  return (
    <nav className="m-nav" aria-label="Main">
      {LEFT.map((i) => (
        <Tab key={i.to} to={i.to} icon={i.icon} label={t(i.key)} />
      ))}
      <NavLink to="/" end className={({ isActive }) => `m-fab${isActive ? " active" : ""}`} aria-label={t("nav_record")}>
        <span className="m-fab-orb">
          <Mic size={26} strokeWidth={2} />
        </span>
      </NavLink>
      {RIGHT.map((i) => (
        <Tab key={i.to} to={i.to} icon={i.icon} label={t(i.key)} />
      ))}
    </nav>
  );
}
