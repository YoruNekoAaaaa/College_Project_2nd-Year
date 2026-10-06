 College Projects

Two Python projects I made for my Computer Engineering classes at ICCT Antipolo. Both use CustomTkinter for the GUI.

 CPU Scheduling Simulator

File: CPU_Scheduler_Final.py

A program that simulates CPU scheduling. You add processes (arrival time, burst time, priority), pick an algorithm,
and it shows a Gantt chart with the waiting, turnaround, and response times.

Algorithms: FCFS, SJF (preemptive), Round Robin, Priority (preemptive).

There is also a Smart Advisor button that runs all four algorithms on your processes and tells you which one worked best. I was the lead developer on this one.

To run it:


pip install customtkinter
python CPU_Scheduler_Final.py




 Hospital Triage System

Folder: hospital_triage

A triage program for a hospital. You add patients with their symptoms and pain level, and the program decides who should be treated first. 
I worked on the back-end data structures.

The waiting list is a min-heap (Python's heapq), so the most urgent patient is always on top. Priority goes from 1 (most urgent) to 9. 
The program checks the symptoms first, and if none match, it uses the pain level.

Other features: login and register, search patients by ID or name, treat the next patient, treatment history, and a dashboard. Data is saved in SQLite.

To run it:


pip install customtkinter
cd hospital_triage
python main.py


 Notes

These are school projects, so the triage rules are simplified and it isn't real medical software.

Joseph Ken Macarubbo
