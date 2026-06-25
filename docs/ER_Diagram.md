# Entity Relationship Diagram

Welth utilizes PostgreSQL with Prisma ORM. Below is the relational structure of the database containing 18 tables.

```mermaid
erDiagram
    User ||--o{ Account : owns
    User ||--o{ Transaction : executes
    User ||--o{ Budget : plans
    User ||--o{ Goal : targets
    User ||--o{ Loan : owes
    User ||--o{ Insurance : registers
    User ||--o{ Bill : pays
    User ||--o{ Subscription : registers
    User ||--o{ Receipt : uploads
    User ||--o{ Report : views
    User ||--o{ Notification : receives
    User ||--o{ AIHistory : queries
    User ||--o{ AuditLog : generates
    User ||--o{ Session : maintains
    User ||--|| Settings : configures

    Account ||--o{ Transaction : logs
    Account ||--o{ Investment : contains
    Goal ||--o{ Savings : aggregates

    User {
        string id PK
        string email UNIQUE
        string passwordHash
        string firstName
        string lastName
        string role
        datetime createdAt
        datetime updatedAt
    }

    Account {
        string id PK
        string userId FK
        string name
        string type
        float balance
        string currency
        string institution
        datetime createdAt
        datetime updatedAt
    }

    Transaction {
        string id PK
        string userId FK
        string accountId FK
        float amount
        string currency
        string category
        string description
        datetime date
        string type
        string status
        boolean isFraud
        string source
        datetime createdAt
        datetime updatedAt
    }

    Budget {
        string id PK
        string userId FK
        string category
        float amount
        string period
        datetime startDate
        datetime endDate
        datetime createdAt
        datetime updatedAt
    }

    Goal {
        string id PK
        string userId FK
        string name
        float targetAmount
        float currentAmount
        datetime deadline
        string status
        datetime createdAt
        datetime updatedAt
    }

    Savings {
        string id PK
        string goalId FK
        float amount
        datetime date
        datetime createdAt
    }

    Investment {
        string id PK
        string accountId FK
        string symbol
        string name
        string type
        float shares
        float buyPrice
        float currentPrice
        string currency
        datetime createdAt
        datetime updatedAt
    }

    Loan {
        string id PK
        string userId FK
        string name
        string type
        float principalAmount
        float interestRate
        int termMonths
        datetime startDate
        float outstandingBalance
        float monthlyPayment
        datetime createdAt
        datetime updatedAt
    }

    Insurance {
        string id PK
        string userId FK
        string provider
        string policyName
        string policyNumber
        string type
        float premiumAmount
        string premiumFrequency
        float coverageAmount
        datetime startDate
        datetime expiryDate
        datetime createdAt
        datetime updatedAt
    }

    Bill {
        string id PK
        string userId FK
        string name
        float amount
        datetime dueDate
        string status
        string category
        string recurrence
        datetime createdAt
        datetime updatedAt
    }

    Subscription {
        string id PK
        string userId FK
        string name
        float cost
        string billingCycle
        datetime nextBillingDate
        string category
        string status
        datetime createdAt
        datetime updatedAt
    }

    Receipt {
        string id PK
        string userId FK
        string fileName
        string filePath
        string rawText
        float parsedAmount
        string parsedMerchant
        datetime parsedDate
        string status
        datetime createdAt
        datetime updatedAt
    }

    Report {
        string id PK
        string userId FK
        string type
        string title
        string contentJson
        datetime createdAt
    }

    Notification {
        string id PK
        string userId FK
        string title
        string message
        string type
        boolean isRead
        datetime createdAt
    }

    AIHistory {
        string id PK
        string userId FK
        string prompt
        string response
        string type
        datetime createdAt
    }

    AuditLog {
        string id PK
        string userId FK
        string action
        string ipAddress
        string userAgent
        string details
        datetime createdAt
    }

    Session {
        string id PK
        string userId FK
        string token UNIQUE
        datetime expiresAt
        datetime createdAt
    }

    Settings {
        string id PK
        string userId FK UNIQUE
        string theme
        string currency
        boolean emailNotifications
        boolean smsNotifications
        boolean pushNotifications
        datetime updatedAt
    }
```
