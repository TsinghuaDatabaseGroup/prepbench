## Context

Tableau Conference 2021 includes “Brain Date” sessions where attendees meet to share knowledge. The objective is to model how knowledge can spread through the conference by identifying, for each attendee and subject area, (1) the people they meet directly in sessions they attend and (2) additional people they can be connected to indirectly via the prior direct connections of the people they meet.

## Requirements

- Input the data.
  - Use the three session files as the event log (one file per day) and the lookup file to translate Attendee IDs to Attendee names.
  - The three session files correspond to three consecutive days: input_01.csv represents Day 1, input_02.csv represents Day 2, and input_03.csv represents Day 3.
- Create a DateTime field for each Session.
  - Build a session ordering field that makes sessions comparable across all three days.
  - Sessions must be processed in chronological order across days and times; if two sessions share the same day and time, use Session ID as a tie-breaker to ensure a deterministic order.
  - When using Session ID as a tie-breaker, sort Session IDs numerically (treat them as integers) in ascending order.
- Create a row for each Attendee and Join on the Lookup Table.
  - Split each session’s “Attendee IDs” list so each attendee appears as its own row at the session level, and use the lookup table to map Attendee IDs to Attendee names for the final output.
- Create a Direct Contact Field for each Attendee
  - These are people they directly meet in the brain dates they attend.
  - For a given subject and session, each attendee’s direct contacts are all other attendees listed in that same session (excluding themselves).
  - Direct contacts are accumulated across all sessions for that subject (an attendee may gain new direct contacts in later sessions).
- Make sure Attendees don't have their own names listed as Direct Contacts.
  - Exclude self-pairs (an attendee cannot be a contact of themselves).
- Create an Indirect Contact field for each Attendee
  - These will be the Direct Contacts for each Attendee's Direct Contacts, for sessions that have happened prior to the session where they meet.
  - Remember: order of sessions is important!
  - Compute indirect contacts separately within each Subject (do not allow contacts to cross subject areas).
  - For each subject, process sessions in chronological order. For a given session where attendee **A** meets attendees **B** directly:
    - For each directly-met attendee **B**, take **B**’s direct contacts from sessions strictly earlier than the current session (within the same subject).
    - The union of those prior direct contacts becomes **A**’s indirect contact candidates for that session.
    - Exclude **A** themselves from indirect contacts.
    - Exclude anyone **A** meets directly in the same session from being counted as an indirect contact for that session.
    - Exclude anyone who is already a direct contact of **A** (from any session within the subject) from being counted as an indirect contact.
  - Accumulate indirect contacts across sessions for the subject.
- If another attendee is classified as both a Direct and an Indirect Contact, classify them as a Direct Contact.
  - Ensure the final classification is exclusive: any (Subject, Attendee, Contact) pair that is direct must not appear as indirect.
- Reshape the data so that each row represents an attendee and a contact they've made, either Directly or Indirectly, for each subject matter
  - The output grain must be one row per **Subject × Attendee × Contact Type × Contact**.
  - **Ambiguity resolution for Contact Type labels**: Use "Direct Contact" and "Indirect Contact" as the Contact Type values (not abbreviated forms like "Direct" or "Indirect").
  - Ensure there are no duplicates for the same Subject, Attendee, Contact Type, and Contact.
  - Use the lookup table to output names (Attendee and Contact) rather than IDs; exclude any rows that cannot be mapped to names.
- Output the data.

## Output

- output_01.csv
  - 4 fields:
    - Subject
    - Attendee
    - Contact Type
    - Contact