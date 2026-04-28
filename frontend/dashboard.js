const API_URL = "http://127.0.0.1:8000";
const billsEl = document.getElementById("bills");
const paidBillsEl = document.getElementById("paid-bills");
const statusEl = document.getElementById("status");
const selectedText = document.getElementById("selected-text");
const daysInput = document.getElementById("days");
const loadButton = document.getElementById("load");
const markPaidButton = document.getElementById("mark-paid");
const deleteButton = document.getElementById("delete-bill");
const createBillForm = document.getElementById("create-bill-form");
const dueDateInput = document.getElementById("bill-due");
const createModal = document.getElementById("create-modal");
const closeCreateModalButton = document.getElementById("close-create-modal");

let selectedBill = null;

function showStatus(message) {
  statusEl.textContent = message;
}

function selectBill(bill) {
  selectedBill = bill;
  selectedText.textContent = `${bill.name} · ₹${bill.total_amount} · due ${bill.due_date} · ${bill.status}`;

  if (bill.status === "PAID") {
    markPaidButton.textContent = "Mark UNPAID";
  } else {
    markPaidButton.textContent = "Mark PAID";
  }

  markPaidButton.disabled = false;
  deleteButton.disabled = false;
}

function renderList(container, bills, emptyText) {
  container.textContent = "";

  const table = document.createElement("table");
  table.className = "bill-table";

  const headerRow = document.createElement("tr");
  headerRow.innerHTML = "<th>Name</th><th>Amount</th><th>Due</th>";

  const thead = document.createElement("thead");
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");

  if (!bills.length) {
    const noteRow = document.createElement("tr");
    const noteCell = document.createElement("td");
    noteCell.colSpan = 3;
    noteCell.className = "bill-empty-note";
    noteCell.textContent = emptyText;
    noteRow.appendChild(noteCell);
    tbody.appendChild(noteRow);
  } else {
    bills.forEach((bill) => {
      const row = document.createElement("tr");
      row.className = "bill-row";
      row.innerHTML = `
        <td>${bill.name}</td>
        <td>₹${bill.total_amount}</td>
        <td>${bill.due_date}</td>
      `;
      row.addEventListener("click", () => {
        selectBill(bill);
        const previousSelected = document.querySelector(".selected");
        if (previousSelected) {
          previousSelected.classList.remove("selected");
        }
        row.classList.add("selected");
      });
      tbody.appendChild(row);
    });
  }

  if (container.id === "bills") {
    const addRow = document.createElement("tr");
    addRow.className = "bill-add-row";
    addRow.innerHTML = `
      <td colspan="3">
        <button type="button" class="bill-add-button">+</button>
      </td>
    `;
    addRow.querySelector(".bill-add-button").addEventListener("click", openCreateModal);
    tbody.appendChild(addRow);
  }

  table.appendChild(tbody);
  container.appendChild(table);
}

async function fetchBills() {
  const days = Math.max(1, Number(daysInput.value) || 1);
  showStatus("Loading bills...");
  billsEl.textContent = "";
  paidBillsEl.textContent = "";
  selectedText.textContent = "Select a bill to see actions.";
  selectedBill = null;
  document.querySelectorAll(".selected").forEach((row) => row.classList.remove("selected"));
  markPaidButton.disabled = true;
  deleteButton.disabled = true;

  try {
    const upcomingResponse = await fetch(`${API_URL}/bills/upcoming?days=${days}`);
    if (!upcomingResponse.ok) {
      throw new Error(`Upcoming returned ${upcomingResponse.status}`);
    }
    const upcomingResult = await upcomingResponse.json();
    const upcomingBills = Array.isArray(upcomingResult)
      ? upcomingResult
      : upcomingResult.data || [];

    const allResponse = await fetch(`${API_URL}/bills/all`);
    if (!allResponse.ok) {
      throw new Error(`All returned ${allResponse.status}`);
    }
    const allResult = await allResponse.json();
    const allBills = Array.isArray(allResult)
      ? allResult
      : allResult.data || [];

    const paidBills = allBills.filter((bill) => bill.status === "PAID");

    renderList(billsEl, upcomingBills, "No current bills found.");
    renderList(paidBillsEl, paidBills, "No paid bills found.");

    showStatus(`Showing ${upcomingBills.length} due bill(s) and ${paidBills.length} paid bill(s).`);
  } catch (error) {
    showStatus(`Unable to load bills: ${error.message}`);
    console.error(error);
  }
}

function getDaysUntilDue(bill) {
  const due = new Date(bill.due_date + "T00:00:00");
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const diffMs = due.getTime() - today.getTime();
  return Math.ceil(diffMs / (1000 * 60 * 60 * 24));
}

async function patchBill(status) {
  if (!selectedBill) return;

  showStatus(`Updating ${selectedBill.name}...`);

  try {
    const response = await fetch(`${API_URL}/bills/${selectedBill.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    selectedBill.status = status;

    if (status === "UNPAID") {
      const dueDays = getDaysUntilDue(selectedBill);
      const currentDays = Math.max(1, Number(daysInput.value) || 1);
      if (dueDays > currentDays) {
        daysInput.value = dueDays;
        showStatus(`Bill updated to UNPAID. Adjusted due filter to ${dueDays} day(s) so it appears.`);
      }
    }

    await fetchBills();
  } catch (error) {
    showStatus("Unable to update bill.");
    console.error(error);
  }
}

async function deleteBill() {
  if (!selectedBill) return;

  showStatus(`Deleting ${selectedBill.name}...`);

  try {
    const response = await fetch(`${API_URL}/bills/${selectedBill.id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    await fetchBills();
  } catch (error) {
    showStatus("Unable to delete bill.");
    console.error(error);
  }
}

loadButton.addEventListener("click", fetchBills);
markPaidButton.addEventListener("click", () => {
  if (!selectedBill) return;
  const nextStatus = selectedBill.status === "PAID" ? "UNPAID" : "PAID";
  patchBill(nextStatus);
});
deleteButton.addEventListener("click", deleteBill);
createBillForm.addEventListener("submit", createBill);
closeCreateModalButton.addEventListener("click", closeCreateModal);
createModal.addEventListener("click", (event) => {
  if (event.target === createModal) {
    closeCreateModal();
  }
});

function openCreateModal() {
  createModal.classList.remove("hidden");
  setDueDateDefaults();
  createBillForm.name.focus();
}

function closeCreateModal() {
  createModal.classList.add("hidden");
}

function setDueDateDefaults() {
  if (!dueDateInput) return;
  const today = new Date();
  const defaultDue = new Date(today);
  defaultDue.setDate(defaultDue.getDate() + 3);
  const isoDate = defaultDue.toISOString().slice(0, 10);
  dueDateInput.min = today.toISOString().slice(0, 10);
  dueDateInput.value = isoDate;
}

async function createBill(event) {
  event.preventDefault();

  const name = createBillForm.name.value.trim();
  const total_amount = parseFloat(createBillForm.total_amount.value);
  const due_date = createBillForm.due_date.value;
  const category = createBillForm.category.value.trim() || null;

  if (!name || !due_date || Number.isNaN(total_amount) || total_amount < 0) {
    showStatus("Please provide valid bill name, amount, and due date.");
    return;
  }

  showStatus("Creating bill...");

  try {
    const response = await fetch(`${API_URL}/bills/new`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        due_date,
        total_amount,
        category,
      }),
    });

    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.detail || result.message || response.statusText);
    }

    showStatus("Bill created successfully.");
    createBillForm.reset();
    closeCreateModal();
    setDueDateDefaults();
    await fetchBills();
  } catch (error) {
    showStatus(`Unable to create bill: ${error.message}`);
    console.error(error);
  }
}

setDueDateDefaults();
fetchBills();
