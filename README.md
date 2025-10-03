# 📚 Data Dictionary — Problem Resolution System


# 📦 Model Overview

This system tracks customer problems and how they’re resolved using predefined solutions delivered by providers. It’s modular, scalable, and designed for clarity.

| Model        | Purpose                                                                 |
|--------------|-------------------------------------------------------------------------|
| `Customer`   | Represents a client or organization                                     |
| `Problem`    | A specific issue the customer is experiencing                           |
| `Category`   | Groups services into logical domains                                    |
| `Service`    | A group of related solutions                                            |
| `Solution`   | A predefined solution we offer                                          |
| `Provider`   | A company that delivers one or more solutions                           |
| `Resolution` | Records what was done, why, how, and by whom for a specific problem     |

---

# 🧬 Entity Relationship Diagram (ERD)

This diagram shows how the models relate to each other:


## 🧍 Customer

| Field           | Type         | Description                          |
|----------------|--------------|--------------------------------------|
| `id`            | AutoField    | Primary key                          |
| `name`          | CharField    | Customer name                        |
| `main_contact`  | CharField    | Main contact person                  |
| `email`         | EmailField   | Contact email                        |
| `phone`         | CharField    | Contact phone number                 |
| `notes`         | TextField    | Additional notes                     |
| `archived`      | BooleanField | Marks customer as inactive           |
| `created_at`    | DateTime     | Timestamp of creation                |

**Relationships:**  
- One-to-many with `Problem` (`Customer → Problem`)

---

## ❗ Problem

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| `id`          | AutoField    | Primary key                          |
| `customer`    | FK → Customer| The customer experiencing the issue  |
| `title`       | CharField    | Short title of the problem           |
| `description` | TextField    | Detailed description                 |
| `impact`      | TextField    | Business impact                      |
| `root_cause`  | TextField    | Identified root cause                |
| `urgency`     | ChoiceField  | Low / Medium / High / Critical       |
| `status`      | ChoiceField  | Open / In Progress / Resolved / Closed |
| `notes`       | TextField    | Internal notes                       |
| `created_at`  | DateTime     | Timestamp of creation                |

**Relationships:**  
- Many-to-one with `Customer`  
- One-to-many with `Resolution`

---

## 🗂️ Category

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| `id`          | AutoField    | Primary key                          |
| `name`        | CharField    | Category name                        |
| `description` | TextField    | Optional description                 |

**Relationships:**  
- One-to-many with `Service`

---

## 🛠️ Service

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| `id`          | AutoField    | Primary key                          |
| `name`        | CharField    | Service name                         |
| `category`    | FK → Category| Category this service belongs to     |
| `description` | TextField    | Optional description                 |

**Relationships:**  
- Many-to-one with `Category`  
- One-to-many with `Solution`



---

## 🧪 Solution

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| `id`          | AutoField    | Primary key                          |
| `name`        | CharField    | Solution name                        |
| `service`     | FK → Service | Service this solution belongs to     |
| `description` | TextField    | Optional description                 |
| `providers`   | M2M → Provider| Providers who can deliver this       |

**Relationships:**  
- Many-to-one with `Service`  
- Many-to-many with `Provider`  
- One-to-many with `Resolution`

---

## 🤝 Provider

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| `id`          | AutoField    | Primary key                          |
| `name`        | CharField    | Provider name                        |
| `type`        | ChoiceField  | Internal / External / Partner        |
| `contact_name`| CharField    | Contact person                       |
| `email`       | EmailField   | Contact email                        |
| `phone`       | CharField    | Contact phone                        |
| `address`     | CharField    | Address                              |
| `city`        | CharField    | City                                 |
| `country`     | CharField    | Country                              |
| `notes`       | TextField    | Additional notes                     |
| `website`     | URLField     | Optional website                     |
| `archived`    | BooleanField | Marks provider as inactive           |
| `created_by`  | FK → User    | Who added this provider              |

**Relationships:**  
- Many-to-many with `Solution`  
- One-to-many with `Resolution`

---

## ✅ Resolution

| Field         | Type         | Description                          |
|---------------|--------------|--------------------------------------|
| `id`          | AutoField    | Primary key                          |
| `problem`     | FK → Problem | The problem being resolved           |
| `what`        | CharField    | Brief title of the action taken      |
| `why`         | TextField    | Detailed explanation of the action   |
| `solution`    | FK → Solution| Which solution was implemented       |
| `provider`    | FK → Provider| Who delivered the solution           |
| `created_at`  | DateTime     | Timestamp of resolution              |

**Relationships:**  
- Many-to-one with `Problem`  
- Many-to-one with `Solution`  
- Many-to-one with `Provider`