# Table 'bills'
To create table schema, run from project root: 

```bash
sudo mysql -u root -p< database/schema.sql
```

To seed database with sample data, run from project root:

```bash
sudo mysql -u root -p < database/sample-data.sql
```

> enter password: {look under .env}

**NOTE:** SQL scripts drop the table/delete the bills before creating it/seeding data.