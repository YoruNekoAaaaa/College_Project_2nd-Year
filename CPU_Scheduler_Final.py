import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time
import threading
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from collections import deque
import colorsys

# ─────────────────────────────────────────────
# THEME & PALETTE
# ─────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

PALETTE = {
    "bg":        "#0D1117",
    "surface":   "#161B22",
    "surface2":  "#21262D",
    "border":    "#30363D",
    "accent":    "#58A6FF",
    "accent2":   "#3FB950",
    "accent3":   "#FF7B72",
    "accent4":   "#D2A8FF",
    "accent5":   "#FFA657",
    "text":      "#E6EDF3",
    "muted":     "#8B949E",
    "highlight": "#1F6FEB",
    "meow":      "#D474F7"
}

PROCESS_COLORS = [
    "#58A6FF", "#3FB950", "#FF7B72", "#D2A8FF",
    "#FFA657", "#79C0FF", "#56D364", "#FFA198",
    "#E8B4F8", "#FFB77A", "#A5D6FF", "#ABFF76",
]

ALGORITHMS = ["FCFS", "SJF", "Round Robin", "Priority"]


# ─────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────
@dataclass
class Process:
    pid: int
    arrival: int
    burst: int
    priority: int = 1
    color: str = "#58A6FF"
    remaining: int = 0
    start_time: int = -1
    finish_time: int = -1
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: int = -1

    def __post_init__(self):
        self.remaining = self.burst

    @property
    def name(self):
        return f"P{self.pid}"


@dataclass
class GanttBlock:
    pid: int
    name: str
    start: int
    end: int
    color: str


# ─────────────────────────────────────────────
# SCHEDULING ALGORITHMS
# ─────────────────────────────────────────────
def run_fcfs(processes: List[Process]) -> Tuple[List[GanttBlock], List[Process]]:
    procs = [Process(p.pid, p.arrival, p.burst, p.priority, p.color) for p in processes]
    procs.sort(key=lambda x: (x.arrival, x.pid))
    gantt, time_cur = [], 0
    for p in procs:
        if time_cur < p.arrival:
            gantt.append(GanttBlock(-1, "IDLE", time_cur, p.arrival, PALETTE["surface2"]))
            time_cur = p.arrival
        p.start_time = time_cur
        p.response_time = time_cur - p.arrival
        p.finish_time = time_cur + p.burst
        p.turnaround_time = p.finish_time - p.arrival
        p.waiting_time = p.turnaround_time - p.burst
        gantt.append(GanttBlock(p.pid, p.name, time_cur, p.finish_time, p.color))
        time_cur = p.finish_time
    return gantt, procs


def run_sjf_preemptive(processes: List[Process]) -> Tuple[List[GanttBlock], List[Process]]:
    procs = [Process(p.pid, p.arrival, p.burst, p.priority, p.color) for p in processes]
    for p in procs:
        p.remaining = p.burst
    n, time_cur, done_count = len(procs), 0, 0
    gantt, last_pid, last_start = [], -2, 0
    while done_count < n:
        available = [p for p in procs if p.arrival <= time_cur and p.remaining > 0]
        if not available:
            time_cur += 1
            continue
        p = min(available, key=lambda x: (x.remaining, x.pid))
        if p.start_time == -1:
            p.start_time = time_cur
            p.response_time = time_cur - p.arrival
        if last_pid != p.pid:
            if last_pid != -2 and gantt:
                gantt[-1] = GanttBlock(gantt[-1].pid, gantt[-1].name, gantt[-1].start, time_cur, gantt[-1].color)
            col = p.color if p.pid >= 0 else PALETTE["surface2"]
            gantt.append(GanttBlock(p.pid, p.name, time_cur, time_cur + 1, col))
            last_pid = p.pid
        else:
            g = gantt[-1]
            gantt[-1] = GanttBlock(g.pid, g.name, g.start, time_cur + 1, g.color)
        p.remaining -= 1
        if p.remaining == 0:
            p.finish_time = time_cur + 1
            p.turnaround_time = p.finish_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst
            done_count += 1
        time_cur += 1
    return gantt, procs


def run_round_robin(processes: List[Process], quantum: int) -> Tuple[List[GanttBlock], List[Process]]:
    procs = [Process(p.pid, p.arrival, p.burst, p.priority, p.color) for p in processes]
    for p in procs:
        p.remaining = p.burst
    queue, gantt = deque(), []
    time_cur, done_count, n = 0, 0, len(procs)
    arrived = set()
    procs_sorted = sorted(procs, key=lambda x: x.arrival)
    idx = 0
    while idx < n and procs_sorted[idx].arrival <= time_cur:
        queue.append(procs_sorted[idx])
        arrived.add(procs_sorted[idx].pid)
        idx += 1
    while done_count < n:
        if not queue:
            if idx < n:
                gantt.append(GanttBlock(-1, "IDLE", time_cur, procs_sorted[idx].arrival, PALETTE["surface2"]))
                time_cur = procs_sorted[idx].arrival
                while idx < n and procs_sorted[idx].arrival <= time_cur:
                    queue.append(procs_sorted[idx])
                    arrived.add(procs_sorted[idx].pid)
                    idx += 1
            continue
        p = queue.popleft()
        if p.start_time == -1:
            p.start_time = time_cur
            p.response_time = time_cur - p.arrival
        run_time = min(quantum, p.remaining)
        gantt.append(GanttBlock(p.pid, p.name, time_cur, time_cur + run_time, p.color))
        p.remaining -= run_time
        time_cur += run_time
        while idx < n and procs_sorted[idx].arrival <= time_cur:
            queue.append(procs_sorted[idx])
            arrived.add(procs_sorted[idx].pid)
            idx += 1
        if p.remaining > 0:
            queue.append(p)
        else:
            p.finish_time = time_cur
            p.turnaround_time = p.finish_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst
            done_count += 1
    return gantt, procs


def run_priority_preemptive(processes: List[Process]) -> Tuple[List[GanttBlock], List[Process]]:
    procs = [Process(p.pid, p.arrival, p.burst, p.priority, p.color) for p in processes]
    for p in procs:
        p.remaining = p.burst
    n, time_cur, done_count = len(procs), 0, 0
    gantt, last_pid = [], -2
    while done_count < n:
        available = [p for p in procs if p.arrival <= time_cur and p.remaining > 0]
        if not available:
            time_cur += 1
            continue
        p = min(available, key=lambda x: (x.priority, x.pid))
        if p.start_time == -1:
            p.start_time = time_cur
            p.response_time = time_cur - p.arrival
        if last_pid != p.pid:
            gantt.append(GanttBlock(p.pid, p.name, time_cur, time_cur + 1, p.color))
            last_pid = p.pid
        else:
            g = gantt[-1]
            gantt[-1] = GanttBlock(g.pid, g.name, g.start, time_cur + 1, g.color)
        p.remaining -= 1
        if p.remaining == 0:
            p.finish_time = time_cur + 1
            p.turnaround_time = p.finish_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst
            done_count += 1
        time_cur += 1
    return gantt, procs


# ─────────────────────────────────────────────
# SMART ADVISOR ENGINE
# ─────────────────────────────────────────────
class SmartAdvisor:
    def analyze(self, processes: List[Process], quantum: int = 2) -> dict:
        if not processes:
            return {}
        results = {}
        algos = [
            ("FCFS",         lambda: run_fcfs(processes)),
            ("SJF",          lambda: run_sjf_preemptive(processes)),
            ("Round Robin",  lambda: run_round_robin(processes, quantum)),
            ("Priority",     lambda: run_priority_preemptive(processes)),
        ]
        for name, fn in algos:
            _, procs = fn()
            avg_wt  = sum(p.waiting_time for p in procs) / len(procs)
            avg_tat = sum(p.turnaround_time for p in procs) / len(procs)
            avg_rt  = sum(p.response_time for p in procs) / len(procs)
            results[name] = {"avg_wt": avg_wt, "avg_tat": avg_tat, "avg_rt": avg_rt}

        best_wt  = min(results, key=lambda k: results[k]["avg_wt"])
        best_tat = min(results, key=lambda k: results[k]["avg_tat"])
        best_rt  = min(results, key=lambda k: results[k]["avg_rt"])

        # Composite score (lower is better)
        scores = {}
        for alg in results:
            r = results[alg]
            scores[alg] = r["avg_wt"] * 0.4 + r["avg_tat"] * 0.35 + r["avg_rt"] * 0.25
        best_overall = min(scores, key=scores.get)

        # Workload characteristics
        burst_vals    = [p.burst for p in processes]
        arrival_vals  = [p.arrival for p in processes]
        priority_vals = [p.priority for p in processes]
        burst_std = (sum((b - sum(burst_vals)/len(burst_vals))**2 for b in burst_vals) / len(burst_vals)) ** 0.5
        has_diverse_priority = len(set(priority_vals)) > 2
        all_same_arrival     = len(set(arrival_vals)) == 1
        burst_variance_label = "high" if burst_std > 3 else ("medium" if burst_std > 1 else "low")

        return {
            "results": results,
            "scores": scores,
            "best_overall": best_overall,
            "best_wt":  best_wt,
            "best_tat": best_tat,
            "best_rt":  best_rt,
            "burst_variance": burst_variance_label,
            "has_diverse_priority": has_diverse_priority,
            "all_same_arrival": all_same_arrival,
            "process_count": len(processes),
        }

    def get_recommendation_text(self, analysis: dict) -> str:
        if not analysis:
            return "Add processes to receive recommendations."
        best = analysis["best_overall"]
        bv   = analysis["burst_variance"]
        dp   = analysis["has_diverse_priority"]
        sa   = analysis["all_same_arrival"]
        pc   = analysis["process_count"]

        lines = [
            f"🏆  RECOMMENDED ALGORITHM:  {best}",
            "",
            "━" * 46,
            "📊  WORKLOAD PROFILE",
            f"   • Processes:        {pc}",
            f"   • Burst variance:   {bv.upper()}",
            f"   • Priority spread:  {'Diverse' if dp else 'Uniform'}",
            f"   • Arrival pattern:  {'Simultaneous' if sa else 'Staggered'}",
            "",
            "━" * 46,
            "🔍  WHY THIS ALGORITHM?",
        ]

        if best == "FCFS":
            lines += [
                "   FCFS excels when processes arrive and",
                "   execute in a predictable batch order.",
                "   Simple, fair, and zero overhead.",
            ]
        elif best == "SJF":
            lines += [
                "   Preemptive SJF (SRTF) achieves the",
                "   theoretical minimum average wait time",
                "   by always running the shortest job.",
            ]
        elif best == "Round Robin":
            lines += [
                "   Round Robin gives every process a fair",
                "   time slice — ideal for interactive or",
                "   time-sharing systems.",
            ]
        else:
            lines += [
                "   Preemptive Priority immediately promotes",
                "   high-priority arrivals, minimising their",
                "   response time in real-time systems.",
            ]

        lines += [
            "",
            "━" * 46,
            "📈  ALGORITHM COMPARISON (avg wait time)",
        ]
        sorted_algs = sorted(analysis["results"], key=lambda k: analysis["results"][k]["avg_wt"])
        for i, alg in enumerate(sorted_algs):
            r = analysis["results"][alg]
            tag = "  ★" if alg == best else ""
            lines.append(f"   {i+1}. {alg:<24} {r['avg_wt']:>6.2f}s{tag}")

        lines += [
            "",
            "━" * 46,
            "💡  TIPS",
        ]
        if bv == "high":
            lines.append("   • High burst variance → SJF shines.")
        if dp:
            lines.append("   • Diverse priorities → consider Priority scheduling.")
        if sa:
            lines.append("   • All same arrival → FCFS/SJF give best results.")

        return "\n".join(lines)


# ─────────────────────────────────────────────
# GANTT CHART CANVAS
# ─────────────────────────────────────────────
class GanttCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=PALETTE["bg"], highlightthickness=0, **kwargs)
        self.gantt_blocks: List[GanttBlock] = []
        self.bind("<Configure>", self._on_resize)

    def set_blocks(self, blocks: List[GanttBlock]):
        self.gantt_blocks = blocks
        self._draw()

    def _on_resize(self, _=None):
        self._draw()

    def _draw(self):
        self.delete("all")
        if not self.gantt_blocks:
            self.create_text(self.winfo_width() // 2, 55,
                text="Run a simulation to see the Gantt chart",
                fill=PALETTE["muted"], font=("Consolas", 11))
            return

        W = self.winfo_width() or 900
        PAD_L, PAD_R = 12, 12
        BAR_Y, BAR_H = 24, 40
        LABEL_Y = BAR_Y + BAR_H + 14
        total_time = max(b.end for b in self.gantt_blocks)
        if total_time == 0:
            return

        draw_w = W - PAD_L - PAD_R
        scale = draw_w / total_time

        for b in self.gantt_blocks:
            x0 = PAD_L + b.start * scale
            x1 = PAD_L + b.end * scale
            col = b.color
            self.create_rectangle(x0, BAR_Y, x1, BAR_Y + BAR_H,
                fill=col, outline=PALETTE["bg"], width=2)
            bw = x1 - x0
            if bw > 18:
                self.create_text((x0 + x1) / 2, BAR_Y + BAR_H / 2,
                    text=b.name if b.pid != -1 else "·",
                    fill="#FFFFFF" if b.pid != -1 else PALETTE["muted"],
                    font=("Consolas", 9 if bw < 35 else 10, "bold"))
            self.create_text(x0, LABEL_Y, text=str(b.start),
                fill=PALETTE["muted"], font=("Consolas", 8), anchor="n")

        last_x = PAD_L + total_time * scale
        self.create_text(last_x, LABEL_Y,
            text=str(total_time), fill=PALETTE["muted"],
            font=("Consolas", 8), anchor="n")


# ─────────────────────────────────────────────
# MAIN APPLICATION
# ─────────────────────────────────────────────
class CPUSchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduling Simulator  ·  Smart Advisor")
        self.geometry("1360x840")
        self.minsize(1100, 720)
        self.configure(fg_color=PALETTE["bg"])

        self.processes: List[Process] = []
        self.next_pid   = 1
        self.advisor    = SmartAdvisor()
        self._pid_color = {}

        self._build_ui()

    # ── UI CONSTRUCTION ──────────────────────
    def _build_ui(self):
        hdr = ctk.CTkFrame(self, fg_color=PALETTE["surface"], corner_radius=0, height=54)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="⚙  CPU SCHEDULING SIMULATOR",
            font=ctk.CTkFont("Consolas", 17, "bold"),
            text_color=PALETTE["accent"]).pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(hdr, text="Smart Advisor Edition",
            font=ctk.CTkFont("Consolas", 11),
            text_color=PALETTE["muted"]).pack(side="left", pady=10)
        ctk.CTkLabel(hdr, text="MeowBytes",
            font=ctk.CTkFont("Consolas", 20),
            text_color=PALETTE["meow"]).pack(side="left",padx=160, pady=10)

        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=14, pady=(10, 10))
        main.columnconfigure(0, weight=0, minsize=320)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=0, minsize=310)
        main.rowconfigure(0, weight=1)

        self._build_left(main)
        self._build_center(main)
        self._build_right(main)

    def _build_left(self, parent):
        left = ctk.CTkFrame(parent, fg_color=PALETTE["surface"], corner_radius=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.rowconfigure(4, weight=1)

        ctk.CTkLabel(left, text="PROCESSES",
            font=ctk.CTkFont("Consolas", 13, "bold"),
            text_color=PALETTE["accent"]).grid(row=0, column=0, columnspan=2, padx=14, pady=(14, 6), sticky="w")

        fields = ctk.CTkFrame(left, fg_color=PALETTE["surface2"], corner_radius=8)
        fields.grid(row=1, column=0, columnspan=2, padx=10, pady=4, sticky="ew")
        fields.columnconfigure(1, weight=1)

        labels = ["Arrival Time", "Burst Time", "Priority (1=high)"]
        self._entries = {}
        for i, lbl in enumerate(labels):
            ctk.CTkLabel(fields, text=lbl, font=ctk.CTkFont("Consolas", 10),
                text_color=PALETTE["muted"]).grid(row=i, column=0, padx=(10, 6), pady=5, sticky="w")
            e = ctk.CTkEntry(fields, width=90,
                fg_color=PALETTE["surface"], border_color=PALETTE["border"],
                text_color=PALETTE["text"], font=ctk.CTkFont("Consolas", 11))
            e.grid(row=i, column=1, padx=(0, 10), pady=5, sticky="ew")
            e.insert(0, ["0", "5", "1"][i])
            self._entries[["arrival", "burst", "priority"][i]] = e

        btn_frame = ctk.CTkFrame(left, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=6, sticky="ew")
        btn_frame.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="+ Add Process",
            fg_color=PALETTE["highlight"], hover_color="#1158C7",
            font=ctk.CTkFont("Consolas", 11, "bold"),
            command=self._add_process).grid(row=0, column=0, padx=(0, 4), sticky="ew")

        ctk.CTkButton(btn_frame, text="⟳ Random",
            fg_color=PALETTE["surface2"], hover_color=PALETTE["border"],
            border_color=PALETTE["border"], border_width=1,
            font=ctk.CTkFont("Consolas", 11),
            command=self._random_processes).grid(row=0, column=1, padx=(4, 0), sticky="ew")

        ctk.CTkButton(left, text="🗑  Clear All",
            fg_color="transparent", hover_color="#3D0000",
            border_color=PALETTE["accent3"], border_width=1,
            text_color=PALETTE["accent3"],
            font=ctk.CTkFont("Consolas", 10),
            command=self._clear_processes).grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 6), sticky="ew")

        list_frame = ctk.CTkFrame(left, fg_color=PALETTE["surface2"], corner_radius=8)
        list_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        list_frame.rowconfigure(1, weight=1)

        hdr = tk.Frame(list_frame, bg=PALETTE["surface2"])
        hdr.pack(fill="x", padx=8, pady=(8, 2))
        for txt, w in [("PID", 40), ("ARR", 40), ("BURST", 48), ("PRIO", 40), ("", 28)]:
            tk.Label(hdr, text=txt, bg=PALETTE["surface2"], fg=PALETTE["muted"],
                font=("Consolas", 9, "bold"), width=w // 8, anchor="center").pack(side="left", expand=True)

        self._proc_frame = ctk.CTkScrollableFrame(list_frame,
            fg_color="transparent", scrollbar_button_color=PALETTE["border"])
        self._proc_frame.pack(fill="both", expand=True, padx=4, pady=4)

    def _build_center(self, parent):
        center = ctk.CTkFrame(parent, fg_color="transparent")
        center.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        center.rowconfigure(2, weight=1)
        center.columnconfigure(0, weight=1)

        algo_row = ctk.CTkFrame(center, fg_color=PALETTE["surface"], corner_radius=10)
        algo_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        algo_row.columnconfigure(1, weight=1)

        ctk.CTkLabel(algo_row, text="Algorithm",
            font=ctk.CTkFont("Consolas", 11),
            text_color=PALETTE["muted"]).grid(row=0, column=0, padx=(14, 8), pady=12)

        self._algo_var = ctk.StringVar(value=ALGORITHMS[0])
        algo_menu = ctk.CTkOptionMenu(algo_row,
            values=ALGORITHMS, variable=self._algo_var,
            fg_color=PALETTE["surface2"], button_color=PALETTE["highlight"],
            text_color=PALETTE["text"], font=ctk.CTkFont("Consolas", 11),
            command=self._on_algo_change)
        algo_menu.grid(row=0, column=1, padx=4, pady=12, sticky="ew")

        ctk.CTkLabel(algo_row, text="Quantum",
            font=ctk.CTkFont("Consolas", 11),
            text_color=PALETTE["muted"]).grid(row=0, column=2, padx=(8, 4), pady=12)

        self._quantum_entry = ctk.CTkEntry(algo_row, width=52,
            fg_color=PALETTE["surface2"], border_color=PALETTE["border"],
            text_color=PALETTE["text"], font=ctk.CTkFont("Consolas", 11))
        self._quantum_entry.grid(row=0, column=3, padx=(0, 6), pady=12)
        self._quantum_entry.insert(0, "2")
        self._quantum_entry.configure(state="disabled")

        ctk.CTkButton(algo_row, text="▶  RUN",
            fg_color=PALETTE["accent2"], hover_color="#2EA043",
            text_color="#0D1117",
            font=ctk.CTkFont("Consolas", 12, "bold"),
            width=90, command=self._run_simulation).grid(row=0, column=4, padx=(4, 14), pady=12)

        gantt_card = ctk.CTkFrame(center, fg_color=PALETTE["surface"], corner_radius=10)
        gantt_card.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(gantt_card, text="GANTT CHART",
            font=ctk.CTkFont("Consolas", 11, "bold"),
            text_color=PALETTE["accent"]).pack(anchor="w", padx=14, pady=(10, 4))

        self._gantt = GanttCanvas(gantt_card, height=95)
        self._gantt.pack(fill="x", padx=8, pady=(0, 10))

        results_card = ctk.CTkFrame(center, fg_color=PALETTE["surface"], corner_radius=10)
        results_card.grid(row=2, column=0, sticky="nsew")
        results_card.rowconfigure(1, weight=1)
        results_card.columnconfigure(0, weight=1)

        ctk.CTkLabel(results_card, text="RESULTS",
            font=ctk.CTkFont("Consolas", 11, "bold"),
            text_color=PALETTE["accent"]).grid(row=0, column=0, padx=14, pady=(10, 4), sticky="w")

        self._stats_frame = ctk.CTkFrame(results_card, fg_color=PALETTE["surface2"], corner_radius=8)
        self._stats_frame.grid(row=0, column=0, padx=14, pady=(0, 8), sticky="e")
        self._stat_labels = {}
        for i, (key, lbl) in enumerate([("avg_wt", "Avg Wait"), ("avg_tat", "Avg TAT"), ("avg_rt", "Avg Response"), ("cpu_util", "CPU Util")]):
            ctk.CTkLabel(self._stats_frame, text=lbl,
                font=ctk.CTkFont("Consolas", 9), text_color=PALETTE["muted"]).grid(row=0, column=i*2, padx=(10, 2), pady=6)
            lv = ctk.CTkLabel(self._stats_frame, text="—",
                font=ctk.CTkFont("Consolas", 10, "bold"), text_color=PALETTE["accent"])
            lv.grid(row=0, column=i*2+1, padx=(0, 10), pady=6)
            self._stat_labels[key] = lv

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Sched.Treeview",
            background=PALETTE["surface2"], foreground=PALETTE["text"],
            fieldbackground=PALETTE["surface2"], rowheight=26,
            font=("Consolas", 10), borderwidth=0)
        style.configure("Sched.Treeview.Heading",
            background=PALETTE["surface"], foreground=PALETTE["muted"],
            font=("Consolas", 10, "bold"), borderwidth=0, relief="flat")
        style.map("Sched.Treeview", background=[("selected", PALETTE["highlight"])])
        style.layout("Sched.Treeview", [("Sched.Treeview.treearea", {"sticky": "nswe"})])

        cols = ("PID", "Arrival", "Burst", "Priority", "Start", "Finish", "Wait", "TAT", "Response")
        self._table = ttk.Treeview(results_card, columns=cols, show="headings",
            style="Sched.Treeview")
        widths = [50, 60, 60, 60, 60, 60, 60, 60, 70]
        for col, w in zip(cols, widths):
            self._table.heading(col, text=col)
            self._table.column(col, width=w, anchor="center", stretch=True)

        scroll = ttk.Scrollbar(results_card, orient="vertical", command=self._table.yview)
        self._table.configure(yscrollcommand=scroll.set)
        self._table.grid(row=1, column=0, sticky="nsew", padx=(14, 0), pady=(0, 10))
        scroll.grid(row=1, column=1, sticky="ns", padx=(0, 8), pady=(0, 10))

    def _build_right(self, parent):
        right = ctk.CTkFrame(parent, fg_color=PALETTE["surface"], corner_radius=10)
        right.grid(row=0, column=2, sticky="nsew")
        right.rowconfigure(1, weight=1)

        ctk.CTkLabel(right, text="🤖  SMART ADVISOR",
            font=ctk.CTkFont("Consolas", 13, "bold"),
            text_color=PALETTE["accent4"]).pack(anchor="w", padx=14, pady=(14, 6))

        ctk.CTkButton(right, text="⚡  Analyze All Algorithms",
            fg_color=PALETTE["accent4"], hover_color="#B77FE0",
            text_color="#0D1117",
            font=ctk.CTkFont("Consolas", 11, "bold"),
            command=self._run_advisor).pack(fill="x", padx=10, pady=(0, 8))

        self._advisor_text = ctk.CTkTextbox(right,
            fg_color=PALETTE["surface2"], text_color=PALETTE["text"],
            font=ctk.CTkFont("Consolas", 10), corner_radius=8,
            border_color=PALETTE["border"], border_width=1,
            wrap="word")
        self._advisor_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._advisor_text.insert("end", "Add processes and click\n⚡ Analyze All Algorithms\nto receive AI-driven\nscheduling recommendations.\n\nThe advisor will:\n• Profile your workload\n• Benchmark all 4 algorithms\n• Recommend the best fit\n• Explain the reasoning")
        self._advisor_text.configure(state="disabled")

    # ── PROCESS MANAGEMENT ───────────────────
    def _get_color(self, pid: int) -> str:
        if pid not in self._pid_color:
            self._pid_color[pid] = PROCESS_COLORS[(pid - 1) % len(PROCESS_COLORS)]
        return self._pid_color[pid]

    def _add_process(self):
        try:
            arr  = int(self._entries["arrival"].get())
            bst  = int(self._entries["burst"].get())
            prio = int(self._entries["priority"].get())
            assert arr >= 0 and bst > 0 and prio >= 1
        except (ValueError, AssertionError):
            messagebox.showerror("Input Error", "Arrival ≥ 0, Burst > 0, Priority ≥ 1 (integers)")
            return

        pid = self.next_pid
        self.next_pid += 1
        col = self._get_color(pid)
        p = Process(pid, arr, bst, prio, col)
        self.processes.append(p)
        self._render_process_row(p)

    def _render_process_row(self, p: Process):
        row = ctk.CTkFrame(self._proc_frame, fg_color=PALETTE["surface"],
            corner_radius=6, height=32)
        row.pack(fill="x", pady=2, padx=2)
        row.pack_propagate(False)

        swatch = tk.Canvas(row, width=10, height=20, bg=PALETTE["surface"],
            highlightthickness=0)
        swatch.pack(side="left", padx=(8, 4))
        swatch.create_rectangle(1, 2, 9, 18, fill=p.color, outline="")

        for txt in [p.name, str(p.arrival), str(p.burst), str(p.priority)]:
            ctk.CTkLabel(row, text=txt,
                font=ctk.CTkFont("Consolas", 10),
                text_color=PALETTE["text"], width=38, anchor="center").pack(side="left", expand=True)

        ctk.CTkButton(row, text="✕", width=26, height=22,
            fg_color="transparent", hover_color="#3D0000",
            text_color=PALETTE["muted"],
            font=ctk.CTkFont("Consolas", 10),
            command=lambda: self._remove_process(p, row)).pack(side="right", padx=4)

    def _remove_process(self, p: Process, row_widget):
        self.processes.remove(p)
        row_widget.destroy()

    def _clear_processes(self):
        self.processes.clear()
        for w in self._proc_frame.winfo_children():
            w.destroy()
        self.next_pid = 1
        self._pid_color.clear()

    def _random_processes(self):
        self._clear_processes()
        n = random.randint(4, 8)
        for i in range(n):
            pid = self.next_pid
            self.next_pid += 1
            col = self._get_color(pid)
            arr  = random.randint(0, 8)
            bst  = random.randint(1, 12)
            prio = random.randint(1, 5)
            p = Process(pid, arr, bst, prio, col)
            self.processes.append(p)
            self._render_process_row(p)

    # ── SIMULATION ───────────────────────────
    def _on_algo_change(self, val):
        if "Round Robin" in val:
            self._quantum_entry.configure(state="normal")
        else:
            self._quantum_entry.configure(state="disabled")

    def _run_simulation(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add at least one process first.")
            return

        algo = self._algo_var.get()
        try:
            quantum = int(self._quantum_entry.get()) if "Round Robin" in algo else 2
            assert quantum > 0
        except (ValueError, AssertionError):
            messagebox.showerror("Input Error", "Quantum must be a positive integer.")
            return

        procs = self.processes

        if algo == "FCFS":
            gantt, result_procs = run_fcfs(procs)
        elif algo == "SJF":
            gantt, result_procs = run_sjf_preemptive(procs)
        elif algo == "Round Robin":
            gantt, result_procs = run_round_robin(procs, quantum)
        else:  # Priority
            gantt, result_procs = run_priority_preemptive(procs)

        self._gantt.set_blocks(gantt)
        self._update_table(result_procs)
        self._update_stats(gantt, result_procs)

    def _update_table(self, procs: List[Process]):
        for row in self._table.get_children():
            self._table.delete(row)
        for p in sorted(procs, key=lambda x: x.pid):
            self._table.insert("", "end", values=(
                p.name, p.arrival, p.burst, p.priority,
                p.start_time, p.finish_time,
                p.waiting_time, p.turnaround_time, p.response_time
            ))

    def _update_stats(self, gantt: List[GanttBlock], procs: List[Process]):
        n = len(procs)
        avg_wt  = sum(p.waiting_time for p in procs) / n
        avg_tat = sum(p.turnaround_time for p in procs) / n
        avg_rt  = sum(p.response_time for p in procs) / n

        total_time = max(b.end for b in gantt) if gantt else 1
        busy_time  = sum(b.end - b.start for b in gantt if b.pid != -1)
        cpu_util   = busy_time / total_time * 100

        self._stat_labels["avg_wt"].configure(text=f"{avg_wt:.2f}")
        self._stat_labels["avg_tat"].configure(text=f"{avg_tat:.2f}")
        self._stat_labels["avg_rt"].configure(text=f"{avg_rt:.2f}")
        self._stat_labels["cpu_util"].configure(text=f"{cpu_util:.1f}%")

    # ── ADVISOR ──────────────────────────────
    def _run_advisor(self):
        if not self.processes:
            messagebox.showwarning("No Processes", "Add at least one process first.")
            return
        try:
            quantum = int(self._quantum_entry.get())
            assert quantum > 0
        except (ValueError, AssertionError):
            quantum = 2

        self._advisor_text.configure(state="normal")
        self._advisor_text.delete("1.0", "end")
        self._advisor_text.insert("end", "⏳  Analyzing algorithms...")
        self._advisor_text.configure(state="disabled")
        self.update()

        def _work():
            analysis = self.advisor.analyze(self.processes, quantum)
            text = self.advisor.get_recommendation_text(analysis)
            self.after(0, lambda: self._set_advisor_text(text))

        threading.Thread(target=_work, daemon=True).start()

    def _set_advisor_text(self, text: str):
        self._advisor_text.configure(state="normal")
        self._advisor_text.delete("1.0", "end")
        self._advisor_text.insert("end", text)
        self._advisor_text.configure(state="disabled")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()