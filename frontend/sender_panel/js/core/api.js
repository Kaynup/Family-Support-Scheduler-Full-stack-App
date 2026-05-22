export {
  requestJson,
  fetchUpcomingBills,
  fetchExpiredBills,
  fetchAllBills,
  fetchAllBillsForBeneficiary,
  fetchUsers,
  searchBills,
  payBill,
} from '../../../shared/js/core/api_client.js';

import { fetchRemittanceHistoryByRole } from '../../../shared/js/core/api_client.js';

export function fetchRemittanceHistory() {
  return fetchRemittanceHistoryByRole('sender');
}
