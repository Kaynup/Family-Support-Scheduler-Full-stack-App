import * as ui from './ui.js';
import { state } from './state.js';

export function renderCalendar(allBills, onDateClick) {
  ui.elements.calendarGrid.textContent = '';
  
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  ui.elements.calendarMonthYear.textContent = `${monthNames[state.currentMonth]} ${state.currentYear}`;
  
  const daysInMonth = new Date(state.currentYear, state.currentMonth + 1, 0).getDate();
  const todayStr = new Date().toISOString().slice(0, 10);
  
  // Create a map of date -> set of statuses and expiration info
  const dateInfo = {};
  allBills.forEach(b => {
    if (!dateInfo[b.due_date]) dateInfo[b.due_date] = { statuses: new Set(), hasExpired: false };
    dateInfo[b.due_date].statuses.add(b.status);
    
    // Mark as expired if DB says so, OR if it's UNPAID and the date is in the past
    if (b.is_expired === 'Y' || (b.status === 'UNPAID' && b.due_date < todayStr)) {
      dateInfo[b.due_date].hasExpired = true;
    }
  });
  
  // Headers
  const dayHeaders = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
  dayHeaders.forEach(d => {
    const el = document.createElement('div');
    el.textContent = d;
    el.style.textAlign = 'center';
    el.style.fontWeight = 'bold';
    el.style.fontSize = '0.7rem';
    ui.elements.calendarGrid.appendChild(el);
  });
  
  // Padding for first day
  const firstDay = new Date(state.currentYear, state.currentMonth, 1).getDay();
  for (let i = 0; i < firstDay; i++) {
    const el = document.createElement('div');
    ui.elements.calendarGrid.appendChild(el);
  }
  
  // Days
  for (let i = 1; i <= daysInMonth; i++) {
    const el = document.createElement('div');
    el.className = 'calendar-day';
    el.textContent = i;
    el.style.cursor = 'pointer';
    
    const dateStr = `${state.currentYear}-${String(state.currentMonth + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
    
    // Highlight if today
    if (dateStr === todayStr) {
      el.classList.add('today');
    }

    // Highlight if selected
    if (dateStr === state.selectedDate) {
      el.style.background = '#dbeafe';
      el.style.borderColor = '#2563eb';
    }

    // Determine glow color
    const info = dateInfo[dateStr];
    if (info) {
      if (info.hasExpired) {
        el.classList.add('glow-expired');
      } else if (info.statuses.has('UNPAID') && info.statuses.has('PAID')) {
        el.classList.add('glow-mixed');
      } else if (info.statuses.has('UNPAID')) {
        el.classList.add('glow');
      } else if (info.statuses.has('PAID')) {
        el.classList.add('glow-paid');
      }
    }

    el.addEventListener('click', () => onDateClick(dateStr));
    
    ui.elements.calendarGrid.appendChild(el);
  }
}

export function changeMonth(delta, onUpdate) {
  state.currentMonth += delta;
  if (state.currentMonth > 11) {
    state.currentMonth = 0;
    state.currentYear++;
  } else if (state.currentMonth < 0) {
    state.currentMonth = 11;
    state.currentYear--;
  }
  onUpdate();
}
