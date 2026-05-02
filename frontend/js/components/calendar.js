import * as ui from './ui.js';
import { state } from '../core/state.js';

const MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];
const DAY_HEADERS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

export function renderCalendar(allBills, onDateClick) {
  const gridEl = ui.elements.calendarGrid;
  gridEl.textContent = '';
  ui.elements.calendarMonthYear.textContent = `${MONTH_NAMES[state.currentMonth]} ${state.currentYear}`;

  const todayStr = new Date().toLocaleDateString('en-CA');
  const dateInfo = buildDateInfoMap(allBills, todayStr);

  renderHeaders(gridEl);

  const firstDay = new Date(state.currentYear, state.currentMonth, 1).getDay();
  renderPadding(gridEl, firstDay);

  const daysInMonth = new Date(state.currentYear, state.currentMonth + 1, 0).getDate();
  for (let i = 1; i <= daysInMonth; i++) {
    renderDay(gridEl, i, todayStr, dateInfo, onDateClick);
  }
}

function buildDateInfoMap(allBills, todayStr) {
  const dateInfo = {};
  allBills.forEach(b => {
    if (!dateInfo[b.due_date]) dateInfo[b.due_date] = { statuses: new Set(), hasExpired: false };
    dateInfo[b.due_date].statuses.add(b.status);

    if (b.is_expired === 'Y' || (b.status === 'UNPAID' && b.due_date < todayStr)) {
      dateInfo[b.due_date].hasExpired = true;
    }
  });
  return dateInfo;
}

function renderHeaders(gridEl) {
  DAY_HEADERS.forEach(d => {
    const el = document.createElement('div');
    el.textContent = d;
    el.style.textAlign = 'center';
    el.style.fontWeight = 'bold';
    el.style.fontSize = '0.7rem';
    gridEl.appendChild(el);
  });
}

function renderPadding(gridEl, count) {
  for (let i = 0; i < count; i++) {
    gridEl.appendChild(document.createElement('div'));
  }
}

function renderDay(gridEl, dayNum, todayStr, dateInfo, onDateClick) {
  const el = document.createElement('div');
  el.className = 'calendar-day';
  el.textContent = dayNum;
  el.style.cursor = 'pointer';

  const dateStr = `${state.currentYear}-${String(state.currentMonth + 1).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;

  if (dateStr === todayStr) {
    el.classList.add('today');
  }

  if (dateStr === state.selectedDate) {
    el.style.background = '#dbeafe';
    el.style.borderColor = '#2563eb';
  }

  applyGlowEffect(el, dateInfo[dateStr]);

  el.addEventListener('click', () => onDateClick(dateStr));
  gridEl.appendChild(el);
}

function applyGlowEffect(el, info) {
  if (!info) return;
  
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
