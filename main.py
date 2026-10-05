from pathlib import Path
import mailbox
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from datetime import datetime

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
        "offre"
    ]
    excluded_keywords = [
        "alerte",
        "alert",
        "job alert",
        "job alerts",
        "nouveaux emplois",
        "nous avons repéré",
        "offres à pourvoir",
        "postes vacants",
        "Suggestions d'offres d'emploi",
        "Nouvelles offres d'emploi",
        "Plus d'emplois",
        "votre profil correspond peut-être",
        "déposez votre candidature",
        "Création de ",
        "Offre à pourvoir",
    ]

    excluded_senders = [
        "no-reply@alerts.talent.com",
        "hello@news.fidme.com",
        "fidme@newsletter.fidme.com",
        "support.candidats@talents-handicap.com",
        "admissions@ecandidats.fr",
        "info@news.yves-rocher.fr",
        "admin@aerocontact.com",
        "visorando@visonews.visorando.com",
        "offres@alertes.cadremploi.fr",
        "no-reply@people-doc.com",
        "lisa@hobbii.com",
        "no-reply@frmkt.lge.com",
        "communication@info.conforama.fr",
        "hello@actu.nexa.fr",
        "laposte@info.laposte.fr",
        "youralerts@jobtomealert.com",
        "alerte@emails.hellowork.com",
        "ne-pas-repondre@meteojob.com",
        "jobs@meilleursjobs.com",
        "sonyeurope@bmail.sony-europe.com",
        "googleplaypromo-noreply@google.com",
        "news@informations.picard.fr",
        "no-reply@vinted.fr",
        "info@news.leboncoin.fr",
        "laposte@news.laposte.info",
        "noreply@lws.fr",
        "candidat@my.jobup.ch",
    ]

    date_debut = datetime(2026, 6, 1).date()

    for key in mbox.iterkeys():
        message = mbox.get_message(key)

        date_mail = message["Date"]

        if not date_mail:
            continue

        try:
            date_mail = parsedate_to_datetime(date_mail).date()
        except (TypeError, ValueError):
            continue

        if date_mail < date_debut:
            continue

        subject = message["Subject"]

        if not subject:
            continue

        sender = message["From"]

        if not sender:
            continue

        sender = str(make_header(decode_header(sender))).lower()

        if any(excluded in sender for excluded in excluded_senders):
            continue

        subject = str(make_header(decode_header(subject)))
        subject_lower = subject.lower()

        if any(keyword in subject_lower for keyword in keywords):
            if any(keyword in subject_lower for keyword in excluded_keywords):
                continue

            print("Date :", date_mail)
            print("Expéditeur :", sender)
            print("Sujet :", subject)
            print("-" * 50)


path = get_path()
print(path)
print(path.exists())

load_mails(path)
