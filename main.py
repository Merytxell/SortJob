import sys
from pathlib import Path
import mailbox
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

def get_path():
    project_root = Path(__file__).parent.parent
    path = project_root /"datas_of_JobSort" / "mails" / "Takeout" / "Mail" / "applications.mbox"
    return path

def load_mails(path):
    mbox = mailbox.mbox(path, create=False)

    keywords = [
        "candidature",
        "alternance",
        "entretien",
        "recrutement",
        "poste",
        "emploi",
    ]

    date_debut = datetime(2026, 6, 1).date()

    for key in mbox.iterkeys():
        message = mbox.get_message(key)

        date_mail = message["Date"]

        if not date_mail:
            continue

        date_mail = parsedate_to_datetime(date_mail).date()

        if date_mail < date_debut:
            continue

        subject = message["Subject"]

        if not subject:
            continue

        subject = str(make_header(decode_header(subject)))
        subject_lower = subject.lower()

        if any(keyword in subject_lower for keyword in keywords):
            print(subject)


path = get_path()
print(path)
print(path.exists())

load_mails(path)
