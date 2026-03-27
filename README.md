# Assignments README
### Error Handling, Logging & Microservices

---

## Assignment 1 — Microservices Research

**File:** `Assignment1_Microservices.docx`

This document covers a research study on microservices architecture across five major companies:

- **Netflix** — How they migrated from a monolith to thousands of microservices after a 3-day outage in 2008, and how their architecture works today.
- **Uber** — How microservices helped them scale globally to 1,300 independent services.
- **Amazon** — How the "two-pizza team" rule and microservices transformed their entire business model and gave birth to AWS.
- **Amazon Prime Video** — Why they abandoned microservices and moved back to a monolith, saving 90% on their AWS bill.
- **Shopify** — Why they chose a modular monolith over microservices and how it handles 80,000+ requests per second on Black Friday.

---

## Assignment 2 — Practical: InstaStore Error Handling Analysis

**Open-source project used:** https://github.com/Rakesh9100/InstaStore
An Instagram photo, video, and profile picture downloader built in Python.

---

### Files Overview

#### Assignment2_Report.docx
The full written report covering all 4 steps of the assignment — analysis, fixes, logging, and the AI vs human comparison table.

---

#### step1_original_with_issues.py
The original InstaStore source code with inline comments marking every problem found.

Issues identified:
1. Bare except AttributeError — too vague, only catches one type of failure
2. No error handling on requests.get() calls — network failures crash the app
3. Content-Length header assumed to always exist — causes a KeyError crash
4. download_dp() has zero error handling — any failure crashes the program
5. Logic bug in the main menu — else: sys.exit() exits even on valid input like A, B, or C

---

#### step2_improved_exceptions.py
The fixed version of the code with targeted exception handling improvements.

Fixes applied:
1. Replaced bare AttributeError with specific exceptions: ConnectionError, Timeout, HTTPError, KeyError, and a catch-all Exception at the bottom
2. Added timeout=10 and raise_for_status() to every requests.get() call
3. Used headers.get('Content-Length', 0) as a safe fallback instead of direct key access
4. Wrapped download_dp() in a full try/except with instaloader-specific errors: ProfileNotExistsException and PrivateProfileNotFollowedException
5. Fixed the main menu from a broken if/if/if/else chain to a proper if/elif/elif/elif/else structure

---

#### step3_with_logging.py
The final version of the code with meaningful logging added throughout.

Logging setup:
- Uses Python's built-in logging module
- Logs are written to both the console and a file called instastore.log
- Format: timestamp - log level - message

Log levels used:
- INFO     — Successful operations: internet verified, download started, file saved
- WARNING  — Non-critical issues: invalid URL, private account, bad menu input
- ERROR    — Recoverable failures: network error, HTTP error, missing header
- CRITICAL — Fatal issues: no internet connection at startup
- EXCEPTION — Unexpected errors with full stack trace captured automatically

---

### Step 4 Summary — AI vs Human Logging

Aspect              | AI Suggestion                              | Human Developer
--------------------|--------------------------------------------|------------------------------------------
Log levels          | Used correctly throughout                  | Often defaults to just print()
Context in messages | Includes URL, filename, username           | Often vague — "Error occurred"
Log to file         | Set up from the start                      | Often forgotten until debugging is painful
Stack traces        | Uses logger.exception() for full traceback | Often uses logger.error() and loses trace
Privacy awareness   | Logs usernames and URLs without flagging   | Would mask sensitive data in production

Key takeaway: AI logging is consistent and structured but lacks the human judgment
to know what should NOT be logged — such as usernames and URLs, which can be
sensitive in production environments.

---

Submitted for the Software Engineering practical module — Uganda Christian University.
