export function getDaysUntilDue(bill) {
  const due = new Date(`${bill.due_date}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const diffMs = due.getTime() - today.getTime();
  return Math.ceil(diffMs / (1000 * 60 * 60 * 24));
}

export function getProjectedBills(bills, targetYear, targetMonth) {
  const allBills = [...bills];
  // Project until the end of the year after the current view
  const horizon = new Date(targetYear + 1, 11, 31);

  const recurringBills = bills.filter(b => b.recurring_interval && b.recurring_interval !== 'NONE');
  
  // Group by name to find the latest instance to project from
  const latestInstances = {};
  recurringBills.forEach(b => {
    if (!latestInstances[b.name] || b.due_date > latestInstances[b.name].due_date) {
      latestInstances[b.name] = b;
    }
  });

  Object.values(latestInstances).forEach(bill => {
    let currentDue = new Date(`${bill.due_date}T00:00:00`);
    
    while (true) {
      if (bill.recurring_interval === 'WEEKLY') {
        currentDue.setDate(currentDue.getDate() + 7);
      } else if (bill.recurring_interval === 'MONTHLY') {
        currentDue.setMonth(currentDue.getMonth() + 1);
      } else {
        break;
      }

      if (currentDue > horizon) break;

      const dateStr = currentDue.toISOString().slice(0, 10);
      
      // Only project if this date doesn't already have an entry for this bill in the database
      const exists = bills.some(b => b.name === bill.name && b.due_date === dateStr);
      
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
  });

  return allBills;
}
