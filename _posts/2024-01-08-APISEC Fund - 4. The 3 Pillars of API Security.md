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

## The 3 Pillas of API Security

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/38125e-ff77-313-43d5-458d643f215d_Slide11.jpeg)

- **Governace** is about defining, establishing and enforcing the processes of developing APIs, testing APIs, and getting them into production in a consistent and secure way.
- **Testing** is about ensuring that your APIs perform as expected and are free of flaws.
- **Monitoring** is about checking if they are behaving as expected during runtime.

## First Pillar: Governance

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/55b75b5-bac-5f-8203-321bc1b0ab73_Pillars1_Governance1.jpg)

### Documentation

**OpenAPI Specification (OAS)**, aka **Swagger**, is the industry standard for documenting REST APIs. Below is a raw YAML/JSON file of a Swagger (left) and how it looks like in a visual interface (right).

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/0224d80-cdd6-c2a1-dfb6-bf42c16ce_53.jpg)

> [API Documentation Best Practices](https://www.apisecuniversity.com/courses/api-documentation-best-practices)

## Second Pillar: Testing

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/186ef2-ab1-17d6-fd8b-73355edea2c7_Pillars2_Testing1.jpg)

- Best practice is to make API testing part of your overall testing program alongside unit testing, functionality, performance, etc.
- The "**standard playbook**" tests tends to look at things that are not so common in practice, such as XSS, buffer overflow attacks, injections, etc. The most common cause of real-world breaches comes from **logic flaws** in the app.
- **API First-Testing**: historically, app testing has focused on the UI layer itself, but attackers can simply ignore that and attack the APIs directly. It's not really an abuse of the UI layer but an abuse of the API layer that causes breaches, such as lack of authentication, lack of authorization, etc.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/d6e7668-2645-217e-78b-fc5bdd6647_Pillars2_Testing2.jpg)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/da86f17-4380-8ecd-1a52-eff4e256872_Pillars2_Testing4.jpg)

> [API Penetration Testing Course](https://www.apisecuniversity.com/courses/api-penetration-testing).

## Third Pillar: Monitoring

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/e663b1c-a433-3354-3b1f-570d41624beb_65.jpg)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/750d255-e5ff-714b-ddd-386ffe2c546f_66.jpg)

### Monitoring Appoaches

- **Proactive - Blocking**: you can enforce policy.
- **Reactive - Alerting**: you might not have enough context to make judgements about the traffic's nature. For instance, in the Coinbase breach, the HTTP request had nothing abnormal in it.

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/750d255-e5ff-714b-ddd-386ffe2c546f_66.jpg)

## Cybersecurity Landscape

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/25e4e-f8d4-100c-4bc-73dc5f5caa_70.jpg)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/3221cf-2e61-463-c680-a5cae1b2c4f_71.jpg)

In the middle is where the biggest gap has existed in terms of security: API security testing. Web app scanners are designed to interact with web/mobile interfaces, but APIs don't have any. So you need to implement comprehensive, effective security testing at the API level. And you want to accomplish this "left" of this dotted line.

## Conclusion and Best Practices

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/d8fe40-624-0738-7e40-7c20dad14ca_73.jpg)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/bf5b7c0-32bf-ee4-567-34d183ea5068_74.jpg)

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2147573912/products/62b3047-51c4-60bc-6f64-324375d7c20_75.jpg)

<!--
---

<center> <a href="">[Level 0-10]</a> </center>

---
-->