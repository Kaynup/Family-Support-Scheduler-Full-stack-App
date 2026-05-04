import * as UI from './ui.js';
import { state } from '../core/state.js';

const MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];
const DAY_HEADERS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

export function renderCalendar(allBills, onDateClick) {
  const gridEl = UI.elements.calendarGridEl;
  gridEl.textContent = '';
  UI.elements.calendarMonthYearEl.textContent = `${MONTH_NAMES[state.currentMonth]} ${state.currentYear}`;

  const todayStr = new Date().toLocaleDateString('en-CA');
  const dateInfoMap = buildDateInfoMap(allBills, todayStr);

  renderCalendarHeaders(gridEl);

  const firstDayIndex = new Date(state.currentYear, state.currentMonth, 1).getDay();
  renderCalendarPadding(gridEl, firstDayIndex);

  const daysInMonth = new Date(state.currentYear, state.currentMonth + 1, 0).getDate();
  for (let i = 1; i <= daysInMonth; i++) {
    renderCalendarDay(gridEl, i, todayStr, dateInfoMap, onDateClick);
  }
}

function buildDateInfoMap(allBills, todayStr) {
  const dateInfoMap = {};
  allBills.forEach(bill => {
    if (!dateInfoMap[bill.due_date]) {
      dateInfoMap[bill.due_date] = { statuses: new Set(), hasExpired: false };
    }
    dateInfoMap[bill.due_date].statuses.add(bill.status);

    if (bill.is_expired === 'Y' || (bill.status === 'UNPAID' && bill.due_date < todayStr)) {
      dateInfoMap[bill.due_date].hasExpired = true;
    }
  });
  return dateInfoMap;
}

function renderCalendarHeaders(gridEl) {
  DAY_HEADERS.forEach(headerText => {
    const headerEl = document.createElement('div');
    headerEl.textContent = headerText;
    headerEl.style.textAlign = 'center';
    headerEl.style.fontWeight = 'bold';
    headerEl.style.fontSize = '0.7rem';
    gridEl.appendChild(headerEl);
  });
}

function renderCalendarPadding(gridEl, paddingCount) {
  for (let i = 0; i < paddingCount; i++) {
    gridEl.appendChild(document.createElement('div'));
  }
}

function renderCalendarDay(gridEl, dayNum, todayStr, dateInfoMap, onDateClick) {
  const dayEl = document.createElement('div');
  dayEl.className = 'calendar-day';
  dayEl.textContent = dayNum;
  dayEl.style.cursor = 'pointer';

  const dateStr = `${state.currentYear}-${String(state.currentMonth + 1).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;

  if (dateStr === todayStr) {
    dayEl.classList.add('today');
  }

  if (dateStr === state.selectedDate) {
    dayEl.style.background = '#dbeafe';
    dayEl.style.borderColor = '#2563eb';
  }

  applyDayGlowEffect(dayEl, dateInfoMap[dateStr]);

  dayEl.addEventListener('click', () => onDateClick(dateStr));
  gridEl.appendChild(dayEl);
}

function applyDayGlowEffect(dayEl, info) {
  if (!info) return;
  
  if (info.hasExpired) {
    dayEl.classList.add('glow-expired');
  } else if (info.statuses.has('UNPAID') && info.statuses.has('PAID')) {
    dayEl.classList.add('glow-mixed');
  } else if (info.statuses.has('UNPAID')) {
    dayEl.classList.add('glow');
  } else if (info.statuses.has('PAID')) {
    dayEl.classList.add('glow-paid');
  }
}

export function handleMonthChange(delta, onUpdate) {
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
