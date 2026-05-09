export function getDaysUntilDue(bill) {
  const due = new Date(`${bill.due_date}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const diffMs = due.getTime() - today.getTime();
  return Math.ceil(diffMs / (1000 * 60 * 60 * 24));
}

export function filterBillsForDisplay(bills) {
  // Just remove PAID bills. The DB only holds one active instance per recurring bill.
  // Projections are handled separately for the calendar.
  return bills.filter(b => b.status !== 'PAID');
}

export function getProjectedBills(bills, projectionCount = 12) {
  const allBills = [...bills];
  const latestInstances = findLatestInstances(bills);

  Object.values(latestInstances).forEach(bill => {
    generateProjectionsForBill(bill, projectionCount, allBills, bills);
  });

  return allBills;
}

function findLatestInstances(bills) {
  const recurringBills = bills.filter(b => b.recurring_interval && b.recurring_interval !== 'NONE');
  const latestInstances = {};

  recurringBills.forEach(b => {
    if (!latestInstances[b.name] || b.due_date > latestInstances[b.name].due_date) {
      latestInstances[b.name] = b;
    }
  });

  return latestInstances;
}

function generateProjectionsForBill(bill, projectionCount, allBills, existingBills) {
  let current = new Date(`${bill.due_date}T12:00:00`);
  const anchorDay = current.getDate();

  for (let i = 0; i < projectionCount; i++) {
    if (bill.recurring_interval === 'WEEKLY') {
      current.setDate(current.getDate() + 7);
    } else if (bill.recurring_interval === 'MONTHLY') {
      current.setMonth(current.getMonth() + 1);
      if (current.getDate() !== anchorDay) {
        current.setDate(0);
      }
    } else {
      break;
    }

    const dateStr = current.toLocaleDateString('en-CA');
    const exists = existingBills.some(b => b.name === bill.name && b.due_date === dateStr);

    if (!exists) {
      allBills.push({
        ...bill,
        id: `proj-${bill.id}-${dateStr}`,
        due_date: dateStr,
        status: 'UNPAID',
        isProjected: true
      });
    }
  }
}
