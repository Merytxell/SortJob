import sys
from pathlib import Path
import mailbox
from email.header import decode_header, make_header



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
    for key in mbox.iterkeys():
        message = mbox.get_message(key)
        subject = message["Subject"]

        if subject:
            subject = str(make_header(decode_header(subject)))
            subject_lower = subject.lower()

            if any(keyword in subject_lower for keyword in keywords):
                print(subject)


path = get_path()
print(path)
print(path.exists())

load_mails(path)
