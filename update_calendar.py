import urllib.request
import re

SOURCE = "https://www.shadysideacademy.org/cf_calendar/feed.cfm?type=ical&feedID=F3A24357A5EE4E3A8F9CF4CB74DE53A9"
OUTPUT = "calendar.ics"

# Download the current SSA calendar
request = urllib.request.Request(
    SOURCE,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request) as response:
    data = response.read().decode("utf-8")

# Add Eastern Time zone definition if the feed doesn't already contain one.
timezone = """BEGIN:VTIMEZONE
TZID:America/New_York
X-LIC-LOCATION:America/New_York
BEGIN:DAYLIGHT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
TZNAME:EDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
TZNAME:EST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE
"""

if "TZID:America/New_York" not in data:
    data = data.replace(
        "CALSCALE:GREGORIAN",
        "CALSCALE:GREGORIAN\n" + timezone,
        1
    )

# Convert only timezone-less timed events.
# All-day events use YYYYMMDD and are left unchanged.
data = re.sub(
    r"(?m)^(DTSTART|DTEND):(\d{8}T\d{6})$",
    r"\1;TZID=America/New_York:\2",
    data
)

with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
    f.write(data)
