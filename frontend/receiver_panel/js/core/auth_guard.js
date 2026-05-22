import { requireRole } from '../../../shared/js/core/auth.js';

export function guardRoute() {
  return requireRole('beneficiary');
}
