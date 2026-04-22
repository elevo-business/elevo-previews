# TAG 2 EXECUTION GUIDE — April 21, 2026

## Quick Start

**5 Emails to send | 5 Pipedrive Deals to create | 5 Follow-up Sequences to setup**

---

## Method 1: Via Pipedrive UI (Manual)

### Step 1: Create Deals (9:00 AM)
Go to Pipedrive → Deals → Add Deal (repeat 5x)

| Contact | Company | Email | Preview URL |
|---------|---------|-------|-------------|
| 6 | Immobilia Deutschland | contact@mein-immobilienmakler.de | preview.llevo.de/immobilia-deutschland |
| 7 | CASA Immobilien | info@casa-id.de | preview.llevo.de/casa-immobilien |
| 8 | Appelhans Immobilien | info@appelhansimmobilien.de | preview.llevo.de/appelhans-immobilien |
| 9 | FREIESLEBEN GmbH | muenster@immobilienmakler12.de | preview.llevo.de/freiesleben-gmbh |
| 10 | Boenighausen Immobilien | info@boenighausen-immobilien.de | preview.llevo.de/boenighausen-immobilien |

**Deal Fields:**
- Stage: "Preview Requested"
- Expected close date: 2026-04-28 (7 days)
- Owner: Outreach Lead
- Add contact/organization info

### Step 2: Send Emails (08:45 AM)
For each contact, compose email via Pipedrive activity:

**Subject:** `Exposé-Erstellung bei Ihnen: Das müssen Sie schneller haben`

**Body:**
```
Hallo {{FIRMENNAME}},

Ihre Website ist noch nicht optimiert für Exposé-Erstellung und Kundenakquisition.

Wir haben einen kostenlosen Website-Entwurf für {{FIRMENNAME}} erstellt – basierend auf Ihrer aktuellen Website und Best Practices Ihrer Branche.

🔍 Schauen Sie sich an, was möglich ist:
{{PREVIEW_URL}}

⏱️ Dieser Entwurf zeigt:
- Moderne Design & UX
- Optimierte Exposé-Präsentation
- Mobile-first Darstellung
- Call-to-Action für Kundenakquisition

Das ist selbstverständlich nur ein Entwurf. Wir passen jede Website vollständig nach Ihren individuellen Anforderungen und Geschäftszielen an.

Feedback? Fragen? Einfach antworten – wir sind hier! 👋

Beste Grüße,
Elevo Outreach
```

### Step 3: Setup Follow-up Sequences (09:30 AM)
In Pipedrive, add workflow/automation:
- Day 3: Follow-up 1 (value-add insight)
- Day 7: Follow-up 2
- Day 14: Follow-up 3
- Day 21: Follow-up 4
- Day 28: Follow-up 5

---

## Method 2: Via CSV Import (If Available)

1. Use `tag2_ready_to_send.csv` in this folder
2. Import into Pipedrive via bulk action (if supported)
3. Verify all deals created
4. Send emails from bulk email tool if available

---

## Method 3: Via API (If Credentials Available)

```bash
# For each contact, call:
POST https://api.pipedrive.com/v1/deals
{
  "title": "{{FIRMENNAME}} - Website Preview",
  "stage_id": "{{STAGE_ID}}",
  "org_id": "{{ORG_ID}}",
  "person_id": "{{CONTACT_ID}}",
  "expected_close_date": "2026-04-28",
  "owner_id": "{{OUTREACH_LEAD_ID}}"
}

# Then send email via Pipedrive email activity
POST https://api.pipedrive.com/v1/deals/{{DEAL_ID}}/activities
{
  "type": "email",
  "subject": "Exposé-Erstellung bei Ihnen: Das müssen Sie schneller haben",
  "body": "...",
  "to": "{{EMAIL}}"
}
```

---

## Daily Checklist

- [ ] 08:45 AM: Send 5 emails
- [ ] 09:00 AM: Create 5 Pipedrive deals
- [ ] 09:15 AM: Setup 5-touch sequences
- [ ] 09:30 AM: Enable email tracking
- [ ] 16:00 PM: Daily report

---

## Metrics to Track

| Metric | Target |
|--------|--------|
| Emails sent | 5 |
| Deals created | 5 |
| Sequences active | 5 |
| Open rate (48h) | >40% |
| Reply rate (7d) | >5% |

---

## Next Steps

- Day 3 (2026-04-22): Repeat for 5 new contacts + Day 2 follow-ups
- Day 4 (2026-04-23): Repeat for 5 new contacts + previous follow-ups
- Day 5 (2026-04-24): Repeat for 5 new contacts + previous follow-ups
