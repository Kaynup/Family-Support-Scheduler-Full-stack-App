export {
  requestJson,
  fetchUpcomingBills,
  fetchExpiredBills,
  fetchAllBills,
  updateBillStatus,
  deleteBillById,
  createBill,
  searchBills,
} from '../../../shared/js/core/api_client.js';

import { fetchRemittanceHistoryByRole } from '../../../shared/js/core/api_client.js';

export function fetchRemittanceHistory() {
  return fetchRemittanceHistoryByRole('beneficiary');
}
