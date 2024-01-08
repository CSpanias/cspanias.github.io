---
title: 1. Intro to API Security & 2. Anatomy of Real-World API Breaches
date: 2024-01-07
categories: [APISEC, APISEC Fundamentals]
tags: [apisec, api]
img_path: /assets/apisec/apisec_fund
published: true
---

## Intro to API Security

### Why API Security

**API** stands for ***Application Programming Interface*** and can be used both externally and internally. For example, booking a taxi ride through Google maps or sending money through a payment app, would represent the **external** use of APIs: they are ***shared across organizations***. APIs also power our **internal** apps, the **microservices**. For instance, an authentication microservice can be exposed to third parties, to trusted partners and customers who may want to integrate with your platform.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/510155-4c2b-1c8c-ef0-3e0dfe4aa7a5_7.jpg){: .normal width="70%"}

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/41ef8c-d3c-af4d-dfe0-61f2dea565c2_9.jpg)

In the schematic above, you have got the **backend app** where all the data lives along with the functionality. This functionality gets exposed to the users through APIs. Thus, **APIs represent a central choke point** via which the data is flowing between the interfaces and the backend.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/1d2ccf-ddc-a280-07bb-ae5050d026_10.jpg)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/b46d648-cb6b-5447-6518-f363e68a04b_11.jpg)

### Anatomy of Real-World API Breaches

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/1cf6738-722-281-b8c-a7425a687dfb_BreachOverviewSlide.jpg)

#### Coinbase

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/8f565-638-87fe-72b6-3e2caea318a_14.jpg)

- The researcher could sell crypto he did not own.
- Intercepted the traffic between the web interface and the backend and identified the API calls.
- He identified 4 transaction parameters that was able to manipulate and achieve the above.

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/0a87883-7b05-36fe-de70-b8627604552_15.jpg)

- He essentially overwrote the `source_account_id` with an acc that did not belong to him ([**Broken Object Level Authorization (BOLA)**](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)).
- The bug cause was a missing logic validation check: the app wasn't confirming that the user submitting the transaction owned the accs related to the transaction.

#### Peloton

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/5ee3da8-e0-76a3-2dc6-435471364fee_18.jpg)

- An API that they have not expected anyone to use as it had no authentication on it ([**Broken Authentication vulnerability**](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)).
- The `private` marking of the acc could be ignored by the API and gain full access to the entire database ([**Broken Object Level Authorization (BOLA)**](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)).
- Researched reported this issue, and it was fixed by adding authentication, but the **BOLA** vuln was not addressed.

#### Venmo

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/0fe8eb-abe1-f6-6dd-6f8826fed1b_19.jpg)

- On the app's homepage were showing real-time transactions for the most recent 10-20 transactions, but they had stripped out PII.
- A researched intercepted the traffic between the homepage and the backend and found the API that was behind this feature. He could call it directly without authentication ([**Broken Authentication vulnerability**](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)).
- In addition, the API would return PII instead of stripped data ([**Broken Object Property Level Authorization**](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)). That was because the filtering was happening at the UI instead on the app level.
- Finally, the researched could ping the server up to 115k times per day and was able to harvest 200 million transactions in full detail ([Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)).

#### Instagram

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/5a658e1-8fba-58c-0fc-7e510eb2daa3_Instagram.jpg)

- An API was exploited to help reset a user's password. If a user clicked the **reset password functionality**, Instagram it would send an email to that user with a 6-digit code. It turned out that the 6-digit code could be supplied through an API back to the Instagram server in order to reset the acc ([**Broken Object Property Level Authorization**](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)).
- The attacker requested a reset code of another user. They code went to the acc's legimate owner, but the attacker **brute-forced** all 1 million combinations of that code. Instagram had some **rate controls** which limited the number of guesses to 200 per IP address, but they did not have any limitation on the number of guesses across multiple IP addressess for the same acc. The attacker simply rotated IP addresses after every 200 guesses, utilizing up to 5,000 different IPs to get through all 1 million combinations and take over a user's acc ([**Broken Authentication vulnerability**](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)).
- What was needed here, was an expiration of the reset code, and a prevention of mass requests on that same account from multiple IP addresses.

#### Bumble

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/3cc1f88-051e-72e-58a-fd335f677eb_Bumble.jpg)

- API lacked authentication ([**Broken Authentication vulnerability**](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)).
- The website was using incremental IDs for its users, and not alphanumeric randomized IDs which cannot be easily predicted ([**Broken Object Level Authorization (BOLA)**](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)).
- The data returned was very detailed and included the distance from the requested to the user being searched. The attacker was able to pinpoint a user's location by creating 3 different accs (**triangulation**).
- Beyond the BOLA vuln, the attacker had function-level access, such as `UPDATE` and `DELETE`, functions that should not be available to end users at all. In addition, he could change the account type from a free unpaid acc to a premium paid acc for any platform user [**Broken Function Level Authorization**](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/).

#### T-Mobile

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/cd3c54a-027d-dbfa-e0c-6dc28b20df64_22.jpg)

- An attacker was able to obtain data through a single API without authorization ([**Broken Authentication vulnerability**](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)).

#### Experian

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/61b2a2f-a7c5-b11e-4e11-075ec422fff7_Experian.jpg)

- Interesting case as it reveals the exposure risk that APIs can have from third parties ([**Improper Inventory Management**](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)). Experian created an API to provide to their financial partners, but one of them decided to expose it directly through their website.
- A researcher could call the API directly and not through the website without authentication ([**Broken Object Level Authorization (BOLA)**](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)).
- They could find a user's credit score using just a name and address (and a DOB in theory but it was just a placeholder).

---

<center> <a href="https://cspanias.github.io/posts/APISEC-Fund-3.-OWASP-Top-10-Background/">[3. OWASP Top 10 Background]</a> </center>

---


