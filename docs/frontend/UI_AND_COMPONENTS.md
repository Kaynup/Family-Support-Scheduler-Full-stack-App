# UI and Components

The UI is built using responsive CSS grid and flexbox layouts.

## Components
- **Bill Table**: Rendered dynamically. Clicking a row highlights it and updates the `selectedBill` state.
- **Calendar**: A visual representation of bills due in the current month. Colors indicate status (e.g., green for paid, yellow for unpaid, red for expired).
- **Modals**: Used for destructive actions (Delete confirmation) and high-friction flows (Payment confirmation).

## CSS Variables
Shared design tokens are located at the top of `styles.css`. This ensures consistent colors, typography, and spacing across both the Sender and Receiver panels.
