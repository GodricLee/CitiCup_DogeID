# DogeID For Citi Cup

## Project Notification

The project **DogeID** is developed for [Citi Cup](http://citicup-nju.njhc.cn/), aiming to provide a **DLT-based digital identity verification system** tailored to financial services. This solution uses cutting-edge technologies like **Hyperledger Indy** to facilitate secure, decentralized, and compliant identity management. 

By leveraging Decentralized Identifiers (DIDs), Blockchain security, and Zero-Knowledge Proofs (ZKPs), DogeID offers a highly secure, automated system for identity verification. It is designed to help **Financial Institutions** (such as banks, payment processors, and other service providers) and **End Users** (individuals and businesses) engage in cross-border transactions with confidence, ensuring privacy, compliance, and fraud prevention.

### Key Features & Innovations

- **DID (Decentralized Identifiers):** Users have full control over their identities. This ensures privacy and security, removing reliance on centralized authorities. 
- **Blockchain Security:** Hyperledger Indy guarantees data immutability, preventing unauthorized changes or access, while maintaining a high level of security through its decentralized nature. 
- **ZKP for Verification:** Identity verification through Zero-Knowledge Proof, providing tamper-proof and reliable validation in real-time.
  
### Project Demonstration

The **DogeID** system includes both frontend and backend components, each serving a unique function in the identity verification process. These components are divided into three key roles:

#### 1. **Financial Institutions (FIs)**

Financial Institutions act as the administrators of the system. They are responsible for onboarding users and verifying the authenticity of decentralized identities. Their key responsibilities include:

- Verifying and approving end-user credentials.
- Issuing credentials in the form of Verifiable Credentials (VCs).
- Enabling secure, cross-border financial transactions for both individual and business customers.
  
#### 2. **Customers**

End Users, referred to as Customers in our system, represent individuals or businesses involved in cross-border transactions. Customers use the system to manage and verify their digital identity in a secure, private manner. Their key responsibilities include:

- Storing and managing personal credentials in their Decentralized Identity wallet.
- Using their DID and VCs to prove their identity to Financial Institutions without exposing unnecessary personal data.
- Engaging in secure and convenient cross-border transactions.

#### 3. **Stewards**

Stewards are the administrators of the system, typically responsible for overall system governance and maintenance. They ensure the integrity and operational smoothness of the system by:

- Overseeing system health and ensuring security protocols are adhered to.
- Managing access controls and user roles for both Financial Institutions and End Users.
- Acting as intermediaries in case of system disputes or failures.

### System Workflow

The following is a brief overview of the system workflow:

1. **Identity Creation:** A Customer creates their DID and manages their personal credentials through a Decentralized Identity wallet.
2. **Credential Issuance:** A Financial Institution issues Verifiable Credentials (VCs) to the Customer after verifying their identity.
3. **Transaction Verification:** For a cross-border transaction, the Customer presents their DID and VCs to the Financial Institution for automated, secure identity verification using Zero-Knowledge Proofs (ZKPs).
4. **Transaction Completion:** Upon successful verification, the transaction is processed securely and efficiently, ensuring compliance with local and international regulations.

### Benefits

- **Privacy & Control:** End Users maintain full control over their identity without relying on centralized identity providers.
- **Reduced Fraud:** Blockchain's immutability and the ZKPs ensure tamper-proof, real-time verification, reducing fraudulent activity in cross-border transactions.
- **Compliance & Security:** The system ensures compliance with industry standards for identity verification, making it a reliable choice for financial institutions worldwide.

### Technology Stack

- **Hyperledger Indy:** A decentralized ledger for managing DIDs and Verifiable Credentials.
- **Blockchain Technology:** To guarantee data integrity and ensure immutability.
- **ZKP (Zero-Knowledge Proofs):** To allow identity verification without exposing sensitive personal data.

### How to Run the Project

To set up the project locally, follow the steps below:

#### Prerequisites

- Node.js v14.x or later
- Hyperledger Indy SDK

#### 1. Clone the repository

```bash
git clone https://github.com/GodricLee/CitiCup_DogeID.git
cd CitiCup_DogeID
```

#### 2. Run the frontend

Go to each identity's server folder.

```bash
python server.py
```

#### 3. Run the backend

For each unique identity,

```bash
npm install
npm run serve
```

## Contact

Email us at 231502004@smail.nju.edu.cn.