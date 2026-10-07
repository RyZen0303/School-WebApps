# School-WebApps
A repository for my school WebApps project, aim to modernize the current one.

Status: Unfinished

| Project Overview: Modernizing the Benjamarachutit Ratchaburi School Grade Inquiry System |
|:---|

| 5W |
|:---|
| Who: All students and faculty members who rely on the school's information system. |
| What: The current UI/UX is overly complex and unintuitive for new users. The interface lacks a modern design, and the system frequently experiences significant bottlenecks during peak traffic periods. |
| Where: The primary issues originate at the website’s entry point, affecting the overall user journey. |
| When: Performance degradation occurs primarily during the release of exam results, when high volumes of users attempt to access the system simultaneously. |
| Why: The legacy system relies too heavily on centralized server-side processing for data retrieval. The backend architecture is not optimized to handle massive concurrent requests, causing server load and time complexity to skyrocket, ultimately leading to system crashes.|

| 1H |
|:---|
| How: We are migrating to a Serverless / Static File Distribution architecture to eliminate the risk of centralized server failure. Key improvements include:
Client-Side Data Processing: We use Python (Pandas) to pre-process student data, generating individual grade files for each student. These files are distributed so that the client (the user’s device) handles the data retrieval and rendering locally. This effectively decentralizes the load, eliminating the bottleneck at the server level. |
| Data Encryption & Integrity: To ensure data security and prevent unauthorized tampering, our Python scripts encrypt the grade data and convert it into a secure format (e.g., Encrypted JSON or Binary) before uploading. This ensures that students can only access their own specific records and prevents any unauthorized modifications to the source data. |
