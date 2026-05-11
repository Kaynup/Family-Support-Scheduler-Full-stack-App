export function getDaysUntilDue(bill) {
  const due = new Date(`${bill.due_date}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const diffMs = due.getTime() - today.getTime();
  return Math.ceil(diffMs / (1000 * 60 * 60 * 24));
}

export function filterBillsForDisplay(bills) {
  // Just remove PAID bills. The DB only holds one active instance per recurring bill.
  return bills.filter(b => b.status !== 'PAID');
}
