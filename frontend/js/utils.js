export function getDaysUntilDue(bill) {
  const due = new Date(`${bill.due_date}T00:00:00`);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const diffMs = due.getTime() - today.getTime();
  return Math.ceil(diffMs / (1000 * 60 * 60 * 24));
}

export function getProjectedBills(bills, targetYear, targetMonth, projectionCount = 12) {
  const allBills = [...bills];
  const recurringBills = bills.filter(b => b.recurring_interval && b.recurring_interval !== 'NONE');
  
  // Group by name to find the latest real instance to project from
  const latestInstances = {};
  recurringBills.forEach(b => {
    // Only project from "real" bills or the latest known instance
    if (!latestInstances[b.name] || b.due_date > latestInstances[b.name].due_date) {
      latestInstances[b.name] = b;
    }
  });

  Object.values(latestInstances).forEach(bill => {
    // Let JS handle the parsing - use T12:00:00 to keep it safe from DST
    let current = new Date(`${bill.due_date}T12:00:00`);
    const anchorDay = current.getDate();
    
    for (let i = 0; i < projectionCount; i++) {
      if (bill.recurring_interval === 'WEEKLY') {
        current.setDate(current.getDate() + 7);
      } else if (bill.recurring_interval === 'MONTHLY') {
        current.setMonth(current.getMonth() + 1);
        // Correct for month-end drift (e.g., Jan 31 -> Feb 28)
        if (current.getDate() !== anchorDay) {
          current.setDate(0); 
        }
      } else {
        break;
      }

      // Automatically get YYYY-MM-DD using the Canadian locale
      const dateStr = current.toLocaleDateString('en-CA');
      
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

