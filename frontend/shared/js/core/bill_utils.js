export function getDaysUntilDue(bill) {
  const due = new Date(`${bill.due_date}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const diffMs = due.getTime() - today.getTime();
  return Math.ceil(diffMs / (1000 * 60 * 60 * 24));
}

export function isBillExpired(bill) {
  return new Date(bill.due_date) < new Date(new Date().toDateString());
}

export function filterBillsForDisplay(bills) {
  return bills.filter((bill) => bill.status !== 'PAID');
}
