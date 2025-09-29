# Phrases & Microcopy (Version 0.1.0)

Consistent wording helps users understand actions quickly and avoids mistranslations. This guide collects reusable phrases for dialogs, empty states, confirmations, and notifications.

## Confirmation Dialogs
- **Delete item** – “Are you sure you want to delete this entry? This action cannot be undone.”
- **Discard changes** – “Discard unsaved changes?”
- **Sign out** – “Do you really want to sign out?”

Keep primary actions explicit, e.g. buttons labelled “Delete”, “Keep item”.

## Success Messages
- “Changes saved successfully.”
- “Invitation sent.”
- “Settings updated.”

Pair them with next-step guidance when applicable (“You can view the report in the Analytics section.”).

## Error Messages
- “Something went wrong. Please try again.”
- “We couldn’t load the data. Retry in a moment.”
- “Form validation failed. Check the highlighted fields.”

Provide actionable steps whenever possible and avoid blame (“You entered wrong…”). Use collective responsibility (“We couldn’t…”).

## Empty States
- “No records found yet. Create your first entry using the button above.”
- “There are no active filters. Adjust the settings on the left.”
- “This dashboard will populate once data becomes available.”

Empty states should guide users to the next action.

## Loading & Progress
- “Loading, please wait…”
- “Fetching latest data…”
- “Preparing your download…”

## Accessibility Considerations
- Keep sentences concise for screen readers.
- Translate phrases in `django.po` files and avoid hard-coded strings.
- When messages repeat, reuse translation keys (`_(
