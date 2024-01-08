---
title: 4. The 3 Pillars of API Security
date: 2024-01-08
categories: [APISEC, APISEC Fundamentals]
tags: [apisec, api]
img_path: /assets/apisec/apisec_fund
published: true
---

---

<center> <a href="https://cspanias.github.io/posts/APISEC-Fund-1.-Intro-to-API-Security-&-2.-Anatomy-of-Real-World-API-Breaches/">1. Intro to API Security & 2. Anatomy of Real-World API Breaches</a> </center>

---

## OWASP Top 10 Background

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/c4d6627-72c6-cba4-cded-3e8e64462f_27.jpg)

> [OWASP Top 10 API Security Risks – 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)

## API1:2023 Broken Object Level Authorization

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/fd1a46e-cf6d-88a-cf84-2b221736b1e8_API1BrokenObjectLevel.jpg)

- The most common and most damaging vulnerability.
- An **authorization issue**: `userA` is properly authenticated, but instead of having access on just his own data, he has access in `userB`'s data as well.

## API2:2023 Broken Authentication

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/0dcaf0-0634-c670-2150-6aef636ae2_API2_BrokenAuthentication.jpg)

- Not just non-existent authentication, but also **weak authentication practices**. 

## API3:2023 Broken Object Property Level Authorization

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/ffb0cfc-cbd3-86d-77ed-3b087cd845_API3_BrokenObjectProperty.jpg)

- The merge of **mass assignment** (_ability to update object elements_) and **excessive data exposure** (_revealing unnecassary sensitive data_).

## API4:2023 Unrestricted Resource Consumption

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/c21abe-5015-7366-dec7-6b0f2f144f18_API4_UnrestrictedResource.jpg)

- Formerly known as **Lack of Resources and Rate Limiting**: _abuse of APIs due to high volumes of API calls, large requests, etc._.
- Can lead to DoS attacks and mass data harvesting.

## API5:2023 Broken Function Level Authorization

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/aaf713-11c1-0c2b-4534-ef365de185_API5_BrokenFunctionLevelAuth.jpg)

- Abuse of API functionality to improperly modify objects (similar to **mass assignment** (API3)).

## API6:2023 Unrestricted Access to Sensitive Business Flows

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/70ed453-c0c3-8b0a-5e88-c27a64d4cc3_API_Security_Fundamentals_-_v1.1.jpg)

- Abuse of a legitimate business workflow through excessive, automated use.
- Examples: mass automated ticket purchasing (buying all inventory as soon as it is published and locking other users out).

## API7:2023 Server Side Request Forgery (SSRF)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/c1aa0b-71b4-8d53-b6eb-db6705aad22_API_Security_Fundamentals_-_v1.1_1_.jpg)

## API8:2023 Security Misconfiguration

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/dcc0173-068-c8-e2a-01dd7b7ec2a0_API_Security_Fundamentals_-_v1.1_2_.jpg)

## API9:2023 Improper Inventory Management

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/aa3f0f-60e4-41e5-cb27-134a00408045_API9_ImproperInventoryManagement.jpg)

- You need to have a comprehensive and accurate view of your API environment - all the APIs that are running, all the endpoints, versions, older versions, who's accessing them, etc.

## API10:2023 Unsafe Consumption of APIs

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/fedf200-f550-6353-4e82-35a60cf3d57_API10_UnsafeConsumption.jpg)

- Exposure via the use of third party APIs.
- Example: an attacker inserts malicious data on the third party API that you use and then submit a request via your API to specifically pull that data.

<!--
---

<center> <a href="">[Level 0-10]</a> </center>

---
-->