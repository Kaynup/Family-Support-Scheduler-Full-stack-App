export function createAppState(overrides = {}) {
  return {
    currentUser: null,
    selectedBill: null,
    currentMonth: new Date().getMonth(),
    currentYear: new Date().getFullYear(),
    selectedDate: null,
    projectionCount: 12,
    ...overrides,
  };
}
