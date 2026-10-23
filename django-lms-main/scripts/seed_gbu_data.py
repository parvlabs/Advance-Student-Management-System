import os
import sys

# Ensure django-lms-main is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import django
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from core.models import Session, Semester, NewsAndEvents
from course.models import Program, Course
from accounts.models import User

print("--- Populating Gautam Buddha University (GBU) Data ---")

# 1. Academic Sessions & Semesters from GBU Academic Calendar 2026-2027 (Office Order GBU.-010/Acad./021/2026-123)
Session.objects.filter(is_current_session=True).update(is_current_session=False)
gbu_session, created = Session.objects.get_or_create(
    session="2026-2027",
    defaults={
        "is_current_session": True,
        "next_session_begins": datetime.date(2027, 8, 2)
    }
)
gbu_session.is_current_session = True
gbu_session.save()

# Monsoon Semester (First Semester)
Semester.objects.filter(session=gbu_session).update(is_current_semester=False)
monsoon_sem, _ = Semester.objects.get_or_create(
    semester="First",
    session=gbu_session,
    defaults={
        "is_current_semester": True,
        "next_semester_begins": datetime.date(2027, 1, 11)
    }
)
monsoon_sem.is_current_semester = True
monsoon_sem.save()

# Winter Semester (Second Semester)
winter_sem, _ = Semester.objects.get_or_create(
    semester="Second",
    session=gbu_session,
    defaults={
        "is_current_semester": False,
        "next_semester_begins": datetime.date(2027, 8, 2)
    }
)

print("Sessions and Semesters populated successfully.")

# 2. News and Events from GBU Academic Calendar & Official University Announcements
news_data = [
    {
        "title": "GBU Academic Calendar 2026-2027 Released (Dean Academics)",
        "summary": "Office Order GBU.-010/Acad./021/2026-123: Dean Academics Prof. Rajeev Varshney has notified the approved Academic Calendar for Session 2026-2027 covering Monsoon & Winter semesters.",
        "posted_as": "News"
    },
    {
        "title": "Monsoon Semester 2026: Registration & Class Commencement",
        "summary": "Fee submission opens 10-20 July 2026. Reporting & registration for 2nd year onwards: 27-31 July 2026. Classes commence 3rd August 2026 (2nd yr+) and 10th August 2026 (1st yr).",
        "posted_as": "Event"
    },
    {
        "title": "Mid-Semester Examination Schedule - Monsoon 2026",
        "summary": "Mid Semester Examinations for all undergraduate and postgraduate schools will take place from Wed, 07th October 2026 to Fri, 16th October 2026.",
        "posted_as": "News"
    },
    {
        "title": "Annual Cultural Fest (Abhivyanjana) & Sports (Shauryautsav)",
        "summary": "Preparations are underway for GBU's flagship cultural extravaganza Abhivyanjana and annual inter-school sports meet Shauryautsav. Schedules will be notified separately.",
        "posted_as": "Event"
    },
    {
        "title": "Winter Semester 2027 Academic Schedule Notification",
        "summary": "Fee submission for Winter Semester opens 26 Dec 2026 - 5 Jan 2027. Registration on 9th Jan 2027. Classes for all years commence Mon, 11th January 2027.",
        "posted_as": "News"
    },
    {
        "title": "Digital Campus & LMS Platform Engineering Credits: Parvlabs",
        "summary": "The GBU Advanced Student Management & Academic Information System is proudly engineered, modernized, and maintained in partnership with Parvlabs (https://github.com/parvlabs).",
        "posted_as": "News"
    }
]

for item in news_data:
    obj, created = NewsAndEvents.objects.get_or_create(
        title=item["title"],
        defaults={
            "summary": item["summary"],
            "posted_as": item["posted_as"]
        }
    )
    if not created:
        obj.summary = item["summary"]
        obj.posted_as = item["posted_as"]
        obj.save()

print(f"Populated {len(news_data)} News & Events items.")

# 3. GBU Schools & Academic Programs
programs_data = [
    {
        "title": "School of Information & Communication Technology (SoICT) - B.Tech CSE",
        "summary": "Specializations in Software Engineering, Artificial Intelligence, Cyber Security, and Cloud Computing at GBU SoICT."
    },
    {
        "title": "School of Information & Communication Technology (SoICT) - B.Tech AI & Data Science",
        "summary": "Comprehensive curriculum covering Machine Learning, Neural Networks, Deep Learning, and Big Data Analytics."
    },
    {
        "title": "School of Engineering (SoE) - B.Tech Civil Engineering",
        "summary": "Core engineering focus on Structural Engineering, Geotechnical, Transportation, and Environmental Engineering."
    },
    {
        "title": "School of Engineering (SoE) - B.Tech Mechanical Engineering",
        "summary": "Advanced design, Thermal Systems, CAD/CAM, Robotics, and Manufacturing Technology."
    },
    {
        "title": "School of Management (SoM) - Master of Business Administration (MBA)",
        "summary": "Dual specialization MBA in Finance, Marketing, Human Resources, and Business Analytics."
    },
    {
        "title": "School of Biotechnology (SoBT) - B.Tech Biotechnology",
        "summary": "Cutting-edge research in Genetic Engineering, Molecular Biology, Bioinformatics, and Industrial Fermentation."
    },
    {
        "title": "School of Law, Justice and Governance (SoLJG) - BA LLB (Hons)",
        "summary": "Five-year integrated honors program covering Constitutional Law, Corporate Jurisprudence, and International Law."
    },
    {
        "title": "School of Buddhist Studies and Civilization (SoBSC) - MA Buddhist Studies",
        "summary": "Pali and Buddhist Philology, Buddhist Philosophy, Buddhist Art, Archeology, and Comparative Religion."
    }
]

program_objs = {}
for p in programs_data:
    prog, created = Program.objects.get_or_create(
        title=p["title"],
        defaults={"summary": p["summary"]}
    )
    program_objs[p["title"]] = prog

print(f"Populated {len(programs_data)} GBU Schools & Programs.")

# 4. GBU Courses
courses_data = [
    {
        "program": "School of Information & Communication Technology (SoICT) - B.Tech CSE",
        "title": "Data Structures and Algorithms",
        "code": "CST-201",
        "credit": 4,
        "summary": "Linear & non-linear data structures, trees, graphs, sorting, searching, and algorithm complexity.",
        "level": "Bachelor",
        "year": 2,
        "semester": "First"
    },
    {
        "program": "School of Information & Communication Technology (SoICT) - B.Tech CSE",
        "title": "Database Management Systems",
        "code": "CST-203",
        "credit": 4,
        "summary": "Relational algebra, SQL, normalization, concurrency control, and transaction management.",
        "level": "Bachelor",
        "year": 2,
        "semester": "First"
    },
    {
        "program": "School of Information & Communication Technology (SoICT) - B.Tech AI & Data Science",
        "title": "Machine Learning and Neural Networks",
        "code": "AID-301",
        "credit": 4,
        "summary": "Supervised, unsupervised learning, gradient descent, deep networks, and computer vision foundations.",
        "level": "Bachelor",
        "year": 3,
        "semester": "First"
    },
    {
        "program": "School of Biotechnology (SoBT) - B.Tech Biotechnology",
        "title": "Recombinant DNA Technology & Genetic Engineering",
        "code": "BT-305",
        "credit": 4,
        "summary": "Cloning vectors, PCR, gene expression systems, CRISPR Cas9, and transgenic technologies.",
        "level": "Bachelor",
        "year": 3,
        "semester": "First"
    },
    {
        "program": "School of Management (SoM) - Master of Business Administration (MBA)",
        "title": "Corporate Finance & Investment Analysis",
        "code": "MBA-102",
        "credit": 3,
        "summary": "Capital budgeting, cost of capital, portfolio theory, and valuation models.",
        "level": "Master",
        "year": 1,
        "semester": "First"
    },
    {
        "program": "School of Law, Justice and Governance (SoLJG) - BA LLB (Hons)",
        "title": "Constitutional Law of India",
        "code": "LAW-101",
        "credit": 4,
        "summary": "Fundamental rights, directive principles, judicial review, and federal structure.",
        "level": "Bachelor",
        "year": 1,
        "semester": "First"
    },
    {
        "program": "School of Buddhist Studies and Civilization (SoBSC) - MA Buddhist Studies",
        "title": "Pali Literature and Buddhist Epistemology",
        "code": "BSC-101",
        "credit": 4,
        "summary": "Analysis of Nikayas, Vinaya Pitaka, Abhidhamma, and early Buddhist philosophical traditions.",
        "level": "Master",
        "year": 1,
        "semester": "First"
    }
]

for c in courses_data:
    prog = program_objs.get(c["program"])
    if prog:
        course, created = Course.objects.get_or_create(
            code=c["code"],
            defaults={
                "program": prog,
                "title": c["title"],
                "credit": c["credit"],
                "summary": c["summary"],
                "level": c["level"],
                "year": c["year"],
                "semester": c["semester"],
                "is_elective": False
            }
        )

print("GBU Courses successfully populated.")
print("--- Gautam Buddha University Seeding Completed Successfully ---")
