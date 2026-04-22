# Validation with Pydantic

- BillListResponse : validates all bills with BillResponses
- BillResponses: validates values in bills, keeps category optional
- BillUpdateRequest: Field declares the datatype of status and field validator adds logic to check if status is 'PAID' or 'UNPAID'
- BillCreateRequest: creates name, amount (greater than 0) and status fields as Fields for datatype checking and due date and category as string. Field validator:
    - ensures name is a mandatory string, Field ensures name has more than one character
    - ensures due date if in ISO format, and is valid
    - ensures status is 'PAID' or 'UNPAID'