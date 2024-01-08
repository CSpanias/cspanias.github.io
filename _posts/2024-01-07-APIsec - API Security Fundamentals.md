---
title: API Security Fundamentals
date: 2024-01-07
categories: [APIsec, APISEC Fundamentals]
tags: [apisec, api, api-testing]
img_path: /assets/apisec/apisec_fund
published: true
---

> [API Security Fundamentals](https://university.apisec.ai/products/api-security-fundamentals)

## Intro to API Security

**API** stands for ***Application Programming Interface*** and can be used both externally and internally. For example, booking a taxi ride through Google maps or sending money through a payment app, would represent the **external** use of APIs: they are ***shared across organizations***. APIs also power our **internal** apps, the **microservices**. For instance, an authentication microservice can be exposed to third parties, to trusted partners and customers who may want to integrate with your platform.

The image below shows reasons of why API Security should be carefully considered:

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/510155-4c2b-1c8c-ef0-3e0dfe4aa7a5_7.jpg){: width="70%"}

In the schematic below, we have the **backend app** where all the data lives along with the app's functionality. The latter gets exposed to the users through APIs. Thus, **APIs represent a central choke point** via which the data is flowing between the interfaces and the backend.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/41ef8c-d3c-af4d-dfe0-61f2dea565c2_9.jpg){: width="70%"}

Unlike attacking a web app, an attacker can directly find and attack an API, and if successful, would be able to access sensitive data.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/1d2ccf-ddc-a280-07bb-ae5050d026_10.jpg){: width="70%"}

## Anatomy of Real-World API Breaches

Below are some examples of real-world API breaches along with some brief details of their main causes.

### Coinbase

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/8f565-638-87fe-72b6-3e2caea318a_14.jpg){: width="70%"}

In this case, the research intercepted the traffic between the web interface and the backend and identified the API calls. He was able to discover 4 transaction parameters that he was able to manipulate (image below): 

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/0a87883-7b05-36fe-de70-b8627604552_15.jpg){: width="70%"}

He essentially overwrote the `source_account_id` with an acc that did not belong to him ([API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)). This bug cause was a missing logic validation check: the app wasn't confirming that the user submitting the transaction owned the accs related to the transaction.

### Peloton

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/5ee3da8-e0-76a3-2dc6-435471364fee_18.jpg){: width="70%"}

In this example, an API was active that the company did not expect anyone to use as it requested no authentication for calling it ([API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)). In addition, a user can ignore the `private` marking of the acc via the API and gain full access to the entire database ([API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)). A researcher reported this issues: the former issue was fixed by adding authentication, but the latter was not addressed at all.

### Venmo

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/0fe8eb-abe1-f6-6dd-6f8826fed1b_19.jpg){: width="70%"}

The app's homepage had a feature that showed the more recent real-time transactions (without revealing any PII). A researched intercepted the traffic between the homepage and the backend and found the API that this feature was based on. He could call it directly without authentication ([API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)). In addition, the API would return PII instead of stripped data ([API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)). The cause of that was that the filtering was happening at the UI instead on the app level. Futhermore, the researcher was able to call the server up to 115k times per day and harvest 200 million transactions in full detail ([API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)).

### Instagram

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/5a658e1-8fba-58c-0fc-7e510eb2daa3_Instagram.jpg){: width="70%"}

The app had an API linked for the password reset functionality. If a user tried to reset the password, the app would send an email to that user with a 6-digit code. It turned out that the 6-digit code could be supplied through an API back to the app's server in order to reset the acc ([API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)).

The attacker could request to reset the password of another user. The 6-digit code would go to the acc's legimate owner, but the attacker was able to **brute-force** all 1 million combinations of that code. Instagram had some **rate controls** which limited the number of guesses to 200 per IP address, but they did not have any limitation on the number of guesses across multiple IP addressess for the same acc. The attacker simply rotated IP addresses after every 200 guesses, utilizing up to 5,000 different IPs to get through all 1 million combinations and take over a user's acc ([API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)).

### Bumble

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/3cc1f88-051e-72e-58a-fd335f677eb_Bumble.jpg){: width="70%"}

In this case, the API completely lacked authentication ([API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)). In addition, it was using **incremental IDs** for its users, and not alphanumeric randomized IDs which cannot be easily predicted ([API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)). What's more, the data returned was very detailed and included the distance from the requested to the user being searched. The attacker was able to pinpoint a user's location by creating 3 different accs (**triangulation**).Finally, the attacker had **function-level access**, such as `UPDATE` and `DELETE`, functions that should not be available to end users at all ([API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)).

### Experian

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/61b2a2f-a7c5-b11e-4e11-075ec422fff7_Experian.jpg){: width="70%"}

This case reveals the exposure risk that APIs can have from third parties ([API9:2023 Improper Inventory Management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)). Experian created an API to provide to their financial partners, but one of them decided to expose it directly through their website. A researcher could call the API directly, and not through the website, without authentication ([API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)). Furthermore, they could find a user's credit score using just a name and address (the existing DOB field was just a placeholder and would accept any value).

### Conclusion

Most of these breaches was caused by [API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) and/or [API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/), which it is odd in the sense that these should be first vulnerabilities to test against when developing/testing an API!

## [OWASP Top 10 API Security Risks – 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/c4d6627-72c6-cba4-cded-3e8e64462f_27.jpg){: width="70%"}

1. [API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/#:~:text=Attackers%20can%20exploit%20API%20endpoints,is%20sent%20within%20the%20request.)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/fd1a46e-cf6d-88a-cf84-2b221736b1e8_API1BrokenObjectLevel.jpg){: width="70%"}

    The most common and most damaging vulnerability. An **authorization issue**: `userA` is properly authenticated, but instead of having access on just his own data, he has access in `userB`'s data as well.

2. [API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/0dcaf0-0634-c670-2150-6aef636ae2_API2_BrokenAuthentication.jpg){: width="70%"}

    Not just non-existent authentication, but also **weak authentication practices**.

3. [API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/ffb0cfc-cbd3-86d-77ed-3b087cd845_API3_BrokenObjectProperty.jpg){: width="70%"}

    The merge of **mass assignment** (_ability to update object elements_) and **excessive data exposure** (_revealing unnecassary sensitive data_).

4. [API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/c21abe-5015-7366-dec7-6b0f2f144f18_API4_UnrestrictedResource.jpg){: width="70%"}

    Formerly known as **Lack of Resources and Rate Limiting**: _abuse of APIs due to high volumes of API calls, large requests, etc._. Can lead to DoS attacks and mass data harvesting.

5. [API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/aaf713-11c1-0c2b-4534-ef365de185_API5_BrokenFunctionLevelAuth.jpg){: width="70%"}

    Abuse of API functionality to improperly modify objects (similar to **mass assignment** (API3)).

6. [API6:2023 Unrestricted Access to Sensitive Business Flows](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/70ed453-c0c3-8b0a-5e88-c27a64d4cc3_API_Security_Fundamentals_-_v1.1.jpg){: width="70%"}

    Abuse of a legitimate business workflow through excessive, automated use. Examples: mass automated ticket purchasing (buying all inventory as soon as it is published and locking other users out).

7. [API7:2023 Server Side Request Forgery (SSRF)](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/c1aa0b-71b4-8d53-b6eb-db6705aad22_API_Security_Fundamentals_-_v1.1_1_.jpg){: width="70%"}

8. [API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/dcc0173-068-c8-e2a-01dd7b7ec2a0_API_Security_Fundamentals_-_v1.1_2_.jpg){: width="70%"}

9. [API9:2023 Improper Inventory Management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/aa3f0f-60e4-41e5-cb27-134a00408045_API9_ImproperInventoryManagement.jpg){: width="70%"}

    You need to have a comprehensive and accurate view of your API environment - all the APIs that are running, all the endpoints, versions, older versions, who's accessing them, etc.

10. [API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)

    ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/fedf200-f550-6353-4e82-35a60cf3d57_API10_UnsafeConsumption.jpg){: width="70%"}

    Exposure via the use of third party APIs. Example: an attacker inserts malicious data on the third party API that you use and then submit a request via your API to specifically pull that data.

## The 3 Pillars of API Security

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/38125e-ff77-313-43d5-458d643f215d_Slide11.jpeg){: width="70%"}

### First Pillar: Governance

**Governace** is about defining, establishing and enforcing the processes of developing APIs, testing APIs, and getting them into production in a consistent and secure way.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/55b75b5-bac-5f-8203-321bc1b0ab73_Pillars1_Governance1.jpg){: width="70%"}

**Documentation**** should be mandatory and well-defined. **OpenAPI Specification (OAS)**, aka **Swagger**, is the industry standard for documenting REST APIs. Below is a raw YAML/JSON file of a Swagger (left) and how it looks like in a visual interface (right).

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/0224d80-cdd6-c2a1-dfb6-bf42c16ce_53.jpg){: width="70%"}

> [API Documentation Best Practices](https://www.apisecuniversity.com/courses/api-documentation-best-practices)

### Second Pillar: Testing

**Testing** is about ensuring that your APIs perform as expected and are free of flaws.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/186ef2-ab1-17d6-fd8b-73355edea2c7_Pillars2_Testing1.jpg){: width="70%"}

Best practice is to make API testing part of your overall testing program alongside unit testing, functionality, performance, etc. The "**standard playbook**" tests tends to look at things that are not so common in practice, such as XSS, buffer overflow attacks, injections, etc. The most common cause of real-world breaches comes from **logic flaws** in the app. **API First-Testing** changes what's historically being done: app testing has focused on the UI layer itself, but attackers can simply ignore that and attack the APIs directly. It's not really an abuse of the UI layer but an abuse of the API layer that causes breaches, such as lack of authentication, lack of authorization, etc.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/d6e7668-2645-217e-78b-fc5bdd6647_Pillars2_Testing2.jpg){: width="70%"}

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/da86f17-4380-8ecd-1a52-eff4e256872_Pillars2_Testing4.jpg){: width="70%"}

> [API Penetration Testing Course](https://www.apisecuniversity.com/courses/api-penetration-testing).

### Third Pillar: Monitoring

**Monitoring** is about checking if they are behaving as expected during runtime.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/e663b1c-a433-3354-3b1f-570d41624beb_65.jpg){: width="70%"}

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/750d255-e5ff-714b-ddd-386ffe2c546f_66.jpg){: width="70%"}

Monitoring appoaches can be:
- **Proactive - Blocking**: you can enforce policy.
- **Reactive - Alerting**: you might not have enough context to make judgements about the traffic's nature. For instance, in the Coinbase breach, the HTTP request had nothing abnormal in it.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/750d255-e5ff-714b-ddd-386ffe2c546f_66.jpg){: width="70%"}

## Cybersecurity Landscape

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/25e4e-f8d4-100c-4bc-73dc5f5caa_70.jpg){: width="70%"}

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/3221cf-2e61-463-c680-a5cae1b2c4f_71.jpg){: width="70%"}

In the middle is where the biggest gap has existed in terms of security: API security testing. Web app scanners are designed to interact with web/mobile interfaces, but APIs don't have any. So you need to implement comprehensive, effective security testing at the API level. And you want to accomplish this "left" of this dotted line.

## Conclusion and Best Practices

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/d8fe40-624-0738-7e40-7c20dad14ca_73.jpg){: width="70%"}

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/bf5b7c0-32bf-ee4-567-34d183ea5068_74.jpg){: width="70%"}

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/62b3047-51c4-60bc-6f64-324375d7c20_75.jpg){: width="70%"}