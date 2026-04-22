# Daily tasks

## Day 1 – MySQL Schema & Database

* [✔️] Created `bills` table
* [✔️] Wrote `schema.sql`
* [✔️] Inserted sample data
* [✔️] Validated everything
* [✔️] Setup DB connection
  * with connection pooling
* [✔️] Initialized FastAPI backend
* [✔️] Connection of backend to DB

---

## Day 2 – Python Core Logic

* [✔️] Created queries
  * [✔️] Data Selection
  * [✔️] Data Insertion
  * [✔️] Data Deletion with bill id
  * [✔️] Data Updation of status
* [✔️] Test queries
  * [✔️] created test scripts for automated testing
* [✔️] Create services
  * [✔️] Implement business logic wrapper over queries
* [✔️] Test services
  * [✔️] create test scripts for automated testing

---

## Day 3 – API Development

* [ ] Create API routes
  * [ ] POST /bills
  * [ ] GET /bills
  * [ ] GET /bills/upcoming
  * [ ] PUT /bills/{id}
* [ ] Add request validation (`schemas.py` using Pydantic)

* [ ] Implement response formatting (JSON)

* [ ] Error handling:
  * invalid input
  * missing fields
  * DB connection failure
  * record not found

* [ ] Test endpoints:
  * curl / Postman

* [ ] Validate:
  * upcoming bills logic (< 3 days working correctly)

---