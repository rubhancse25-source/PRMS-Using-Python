# prms_reports.py
"""
Improved Reports window for PRMS — charts scaled so axis labels/ticks are visible.
Place this file next to prms_final.py and click "Reports" in the sidebar.
Requires: matplotlib, numpy
Install: python3 -m pip install matplotlib numpy
"""

import os
import sqlite3
import datetime
import textwrap
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def generate_insights(stats):
    insights = []
    monthly = stats.get("monthly_counts", {})
    months = list(monthly.keys())
    vals = list(monthly.values())
    if len(vals) >= 2:
        last = vals[-1]
        prev = vals[-2]
        try:
            pct = int((last - prev) / (prev or 1) * 100)
            if abs(pct) >= 20:
                verb = "increase" if pct > 0 else "decrease"
                insights.append(
                    f"Entries {verb} of {abs(pct)}% in the most recent month vs previous month."
                )
        except Exception:
            pass
    if stats.get("disease_counts"):
        top = sorted(stats["disease_counts"].items(), key=lambda x: x[1], reverse=True)[
            :3
        ]
        if top:
            insights.append("Top diseases: " + ", ".join([t[0] for t in top]))
    if not insights:
        insights.append("No significant trends detected.")
    return insights


DEFAULT_DB = os.path.join(os.path.expanduser("~"), "prms_patients.db")


def get_conn(db_path):
    return sqlite3.connect(os.path.expanduser(db_path))


class ScrollableFrame(ttk.Frame):
    """A simple scrollable frame to hold many charts vertically."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.frame = ttk.Frame(canvas)
        vsb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self._window = canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # resize canvas window to frame width
        def _on_resize(e):
            canvas.itemconfigure(self._window, width=e.width)

        canvas.bind("<Configure>", _on_resize)
        self.canvas = canvas


class ReportsWindow(tk.Toplevel):
    def __init__(self, parent, db_path=DEFAULT_DB):
        super().__init__(parent)
        self.parent = parent
        self.db_path = os.path.expanduser(db_path)
        self.title("📊 Reports — Patient Analytics")
        self.geometry("1100x800")
        self.configure(background="#f7f7fb")
        self._figs = []

        header = ttk.Frame(self, padding=(8, 8))
        header.pack(fill="x")
        ttk.Label(header, text="Reports", font=("Helvetica", 18, "bold")).pack(
            side="left"
        )
        ttk.Label(header, text=f"DB: {self.db_path}", font=("Helvetica", 10)).pack(
            side="right"
        )

        # scrollable area for vertical charts
        self.scroll = ScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=8, pady=8)

        # footer
        footer = ttk.Frame(self, padding=(8, 8))
        footer.pack(fill="x")
        ttk.Button(footer, text="🔁 Refresh", command=self.render).pack(
            side="left", padx=6
        )
        ttk.Button(
            footer, text="💾 Export All Charts", command=self.export_charts
        ).pack(side="left", padx=6)
        ttk.Button(footer, text="Close", command=self.destroy).pack(
            side="right", padx=6
        )

        try:
            self.render()
        except Exception as e:
            messagebox.showerror("Reports Error", f"Failed to render reports: {e}")
            self.destroy()

    def gather_stats(self):
        conn = get_conn(self.db_path)
        cur = conn.cursor()

        # gender counts
        cur.execute("SELECT gender, COUNT(1) FROM patients GROUP BY gender")
        gender_counts = {
            row[0] if row[0] else "Unknown": row[1] for row in cur.fetchall()
        }

        # chronic/acute
        cur.execute("SELECT chronic, COUNT(1) FROM patients GROUP BY chronic")
        chronic = 0
        acute = 0
        for flag, cnt in cur.fetchall():
            if flag == 1:
                chronic = cnt
            else:
                acute = cnt

        # disease counts
        cur.execute(
            "SELECT disease, COUNT(1) FROM patients GROUP BY disease ORDER BY COUNT(1) DESC"
        )
        disease_counts = {row[0]: row[1] for row in cur.fetchall() if row[0]}

        # monthly counts (YYYY-MM)
        cur.execute(
            "SELECT admission_date FROM patients WHERE admission_date IS NOT NULL AND admission_date != ''"
        )
        monthly = {}
        for (ad,) in cur.fetchall():
            if not ad:
                continue
            key = ad.strip()[:7]
            if len(key) >= 7 and key[4] == "-":
                key = key[:7]
            else:
                key = datetime.date.today().strftime("%Y-%m")
            monthly[key] = monthly.get(key, 0) + 1

        # age list and avg age per disease
        cur.execute("SELECT age, disease FROM patients WHERE age IS NOT NULL")
        ages = []
        ages_by_disease = {}
        for age, disease in cur.fetchall():
            if age is None:
                continue
            try:
                a = int(age)
            except Exception:
                continue
            ages.append(a)
            if disease:
                ages_by_disease.setdefault(disease, []).append(a)

        conn.close()

        # prepare monthly for last 12 months
        today = datetime.date.today()
        last12 = []
        for n in range(11, -1, -1):
            yr = today.year
            mo = today.month - n
            while mo <= 0:
                mo += 12
                yr -= 1
            last12.append(f"{yr:04d}-{mo:02d}")
        monthly_counts = {k: monthly.get(k, 0) for k in last12}

        avg_age_by_disease = {
            d: sum(lst) / len(lst)
            for d, lst in ages_by_disease.items()
            if len(lst) >= 2
        }

        return {
            "gender_counts": gender_counts,
            "chronic": chronic,
            "acute": acute,
            "disease_counts": disease_counts,
            "monthly_counts": monthly_counts,
            "ages": ages,
            "avg_age_by_disease": avg_age_by_disease,
        }

    def clear_reports_area(self):
        for w in self.scroll.frame.winfo_children():
            w.destroy()
        self._figs = []

    def _wrap_labels(self, names, width=20):
        """Wrap long labels to multiple lines so they don't get clipped."""
        return [textwrap.fill(n, width=width) for n in names]

    def add_chart(self, title, subtitle, fig, adjust_kwargs=None):
        container = ttk.Frame(self.scroll.frame, padding=(8, 8))
        container.pack(fill="x", pady=(6, 6))
        ttk.Label(container, text=title, font=("Helvetica", 14, "bold")).pack(
            anchor="w"
        )
        ttk.Label(
            container, text=subtitle, font=("Helvetica", 10), foreground="#555555"
        ).pack(anchor="w", pady=(0, 6))
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        # apply tight layout and any additional adjustments
        try:
            fig.tight_layout()
        except Exception:
            pass
        if adjust_kwargs:
            try:
                fig.subplots_adjust(**adjust_kwargs)
            except Exception:
                pass
        self._figs.append(fig)
        return canvas

    def render(self):
        self.clear_reports_area()
        stats = self.gather_stats()
        insights = generate_insights(stats)
        if insights:
            banner = ttk.Frame(self.scroll.frame, padding=(8, 6))
            banner.pack(fill="x", pady=(0, 6))
            ttk.Label(
                banner, text="Auto Insights:", font=("Helvetica", 12, "bold")
            ).pack(side="left")
            ttk.Label(
                banner, text="  ".join(insights[:3]), font=("Helvetica", 10)
            ).pack(side="left", padx=(6, 0))

        # 1. Gender pie
        fig = Figure(figsize=(10, 2.8), dpi=110, constrained_layout=False)
        ax = fig.add_subplot(111)
        labels = list(stats["gender_counts"].keys())
        sizes = list(stats["gender_counts"].values())
        if sum(sizes) == 0:
            ax.text(0.5, 0.5, "No gender data available", ha="center", va="center")
        else:
            ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=140,
                textprops={"fontsize": 10},
            )
        ax.set_title("Gender Distribution", fontsize=12)
        self.add_chart(
            "Gender Distribution",
            "Share of Male / Female / Other patients.",
            fig,
            adjust_kwargs={"bottom": 0.15},
        )

        # 2. Chronic vs Acute
        fig = Figure(figsize=(10, 2.8), dpi=110, constrained_layout=False)
        ax = fig.add_subplot(111)
        vals = [stats["chronic"], stats["acute"]]
        labels2 = ["Chronic", "Acute"]
        if sum(vals) == 0:
            ax.text(0.5, 0.5, "No chronic/acute data", ha="center", va="center")
        else:
            ax.pie(vals, labels=labels2, autopct="%1.1f%%", textprops={"fontsize": 10})
        ax.set_title("Chronic vs Acute Cases", fontsize=12)
        self.add_chart(
            "Chronic vs Acute",
            "Percentage split between chronic and acute patients.",
            fig,
            adjust_kwargs={"bottom": 0.15},
        )

        # 3. Top 20 diseases (horizontal bar) — wrap labels & enlarge left margin
        fig = Figure(figsize=(10, 5), dpi=110, constrained_layout=False)
        ax = fig.add_subplot(111)
        items = sorted(
            stats["disease_counts"].items(), key=lambda x: x[1], reverse=True
        )[:20]
        if not items:
            ax.text(0.5, 0.5, "No disease data", ha="center", va="center")
        else:
            names = [i[0] for i in items]
            vals = [i[1] for i in items]
            wrapped = self._wrap_labels(names, width=22)
            y = np.arange(len(wrapped))
            ax.barh(y, vals)
            ax.set_yticks(y)
            ax.set_yticklabels(wrapped, fontsize=10)
            ax.invert_yaxis()
            ax.set_xlabel("Number of patients", fontsize=11)
            ax.set_title("Top 20 Diseases", fontsize=12)
        self.add_chart(
            "Top Diseases",
            "Most common diseases in the database (top 20).",
            fig,
            adjust_kwargs={"left": 0.28, "bottom": 0.12},
        )

        # 4. Disease by gender (stacked bar) for top 10 diseases — rotate labels and adjust bottom
        fig = Figure(figsize=(10, 4.2), dpi=110, constrained_layout=False)
        ax = fig.add_subplot(111)
        top_diseases = [
            d
            for d, _ in sorted(
                stats["disease_counts"].items(), key=lambda x: x[1], reverse=True
            )[:10]
        ]
        if not top_diseases:
            ax.text(0.5, 0.5, "No data", ha="center", va="center")
        else:
            genders = ["Male", "Female", "Other"]
            counts_by_gender = {g: [] for g in genders}
            conn = get_conn(self.db_path)
            cur = conn.cursor()
            for d in top_diseases:
                cur.execute(
                    "SELECT gender, COUNT(1) FROM patients WHERE disease = ? GROUP BY gender",
                    (d,),
                )
                rowmap = {r[0] if r[0] else "Unknown": r[1] for r in cur.fetchall()}
                for g in genders:
                    counts_by_gender[g].append(rowmap.get(g, 0))
            conn.close()
            x = np.arange(len(top_diseases))
            bottom = np.zeros(len(top_diseases))
            colors = ["#4daf4a", "#377eb8", "#ff7f00"]
            for i, g in enumerate(genders):
                vals = counts_by_gender[g]
                ax.bar(x, vals, bottom=bottom, label=g, color=colors[i % len(colors)])
                bottom = bottom + np.array(vals)
            wrapped = self._wrap_labels(top_diseases, width=18)
            ax.set_xticks(x)
            ax.set_xticklabels(wrapped, rotation=30, ha="right", fontsize=10)
            ax.set_title("Disease by Gender (Top 10)", fontsize=12)
            ax.legend()
        self.add_chart(
            "Disease by Gender",
            "Stacked bar showing gender composition per disease (top 10).",
            fig,
            adjust_kwargs={"bottom": 0.20},
        )

        # 5. Age distribution (histogram) — bigger bins and margins
        fig = Figure(figsize=(10, 3.4), dpi=110, constrained_layout=False)
        ax = fig.add_subplot(111)
        ages = stats["ages"]
        if not ages:
            ax.text(0.5, 0.5, "No age data", ha="center", va="center")
        else:
            bins = range(0, 101, 5)
            ax.hist(ages, bins=bins)
            ax.set_xlabel("Age", fontsize=11)
            ax.set_ylabel("Number of patients", fontsize=11)
            ax.set_title("Age Distribution", fontsize=12)
            ax.tick_params(axis="x", labelsize=10)
            ax.tick_params(axis="y", labelsize=10)
        self.add_chart(
            "Age Distribution",
            "Histogram of patient ages (bins of 5 years).",
            fig,
            adjust_kwargs={"bottom": 0.12},
        )

        # 6. Patient entries per month (last 12 months) — rotate x labels and give bottom margin
        fig = Figure(figsize=(10, 3.6), dpi=110, constrained_layout=False)
        ax = fig.add_subplot(111)
        months = list(stats["monthly_counts"].keys())
        vals = list(stats["monthly_counts"].values())
        if sum(vals) == 0:
            ax.text(0.5, 0.5, "No monthly entries", ha="center", va="center")
        else:
            x = np.arange(len(months))
            ax.bar(x, vals)
            ax.set_xticks(x)
            ax.set_xticklabels(months, rotation=45, ha="right", fontsize=10)
            ax.set_ylabel("Number of entries", fontsize=11)
            ax.set_title("Patient entries per month (last 12 months)", fontsize=12)
            ax.tick_params(axis="y", labelsize=10)
        self.add_chart(
            "Patient entries per month",
            "Count of patient admissions across the last 12 months.",
            fig,
            adjust_kwargs={"bottom": 0.25},
        )

        # 7. Average age by top diseases (top 10) — rotate labels & adjust bottom
        fig = Figure(figsize=(10, 3.8), dpi=110, constrained_layout=False)
        ax = fig.add_subplot(111)
        avg = stats["avg_age_by_disease"]
        items = sorted(avg.items(), key=lambda x: x[1], reverse=True)[:10]
        if not items:
            ax.text(0.5, 0.5, "No average age data", ha="center", va="center")
        else:
            names = [i[0] for i in items]
            vals = [i[1] for i in items]
            wrapped = self._wrap_labels(names, width=18)
            x = np.arange(len(wrapped))
            ax.bar(x, vals)
            ax.set_xticks(x)
            ax.set_xticklabels(wrapped, rotation=35, ha="right", fontsize=10)
            ax.set_ylabel("Average age", fontsize=11)
            ax.set_title("Average Age by Disease (top diseases)", fontsize=12)
            ax.tick_params(axis="y", labelsize=10)
        self.add_chart(
            "Average age by disease",
            "Shows average patient age for top diseases (requires ≥2 samples per disease).",
            fig,
            adjust_kwargs={"bottom": 0.22},
        )

    def export_charts(self):
        folder = filedialog.askdirectory(title="Select folder to save charts")
        if not folder:
            return
        try:
            for i, fig in enumerate(self._figs, start=1):
                path = os.path.join(folder, f"prms_report_chart_{i}.png")
                fig.savefig(path, bbox_inches="tight", dpi=150)
            messagebox.showinfo("Export", f"Saved {len(self._figs)} charts to {folder}")
        except Exception as e:
            messagebox.showerror("Export error", f"Failed to save charts: {e}")


def generate_longitudinal_summary(patient_visits, trend_result):
    if not patient_visits:
        return "No patient history available."

    latest = patient_visits[-1]

    return (
        f"The patient has {len(patient_visits)} recorded visits. "
        f"The latest visit indicates {latest.risk_level} risk with "
        f"a {latest.disease_type} condition. "
        f"Overall health trend is {trend_result['trend'].lower()}. "
        f"{trend_result['alert']}."
    )
