---
layout: article
title:  "A Brief Reference on Russia's Information Warfare"
date:   2020-05-07 06:30
categories: cyber
tags: [reverse,malware, ELF, packers]
author: ulexec
---


Information Warfare has evolved in the last years introducing challenges to reflect a theoretical model of this new domain in order to understand its nuances which impact a wide range of different sectors operating within the computer and information technology domain.
 
<br/>


## **Introduction**

From the beginning of malware existence, it's been usually designed towards accomplishing financial driven goals. This is still the case with most malware within the domain of cyber-crime.
However, a high ratio of cyber-espionage operations were starting to emerge observed by different private and public sector entities starting to be taken seriously from 2010 with the appearance of [Stuxnet](https://en.wikipedia.org/wiki/Stuxnet). 
 
This specific change in ecosystem does not only implies that better understanding of specific tactics and techniques leveraged by this new malware zoo is necessary, but also implies that in order to interpret and analyse cyber-espionage operations, development of a different mindset is required since threat actors conducting these operations are of higher profile having more resources and bigger budgets than cyber-crime actors, and their campaigns can also be ambiguous to interpret along with their attribution.
 
Understanding cyber-espionage campaigns is sort of intelligence work. However, professionals in this ecosystem conducting these investigations do not necessarily have an intelligence or military background (like myself), therefore it is necessary to catch up not only technically but also acquiring a more contextual rich background in regards to these kinds of operations.
 
This article is meant to be a brief reference of some of the various engagements allegedly conducted by The Russian Federation in the Information Warfare realm.
This is not necessarily crucial for Threat Intelligence work since there is no additional incentive to know from which country each campaign was conducted from, or even the reasons behind it, at least in the private sector.
 
 However, as this domain grows and matures over time, I think is important to have some historic context of different noticeable events, in particular the ones leveraged by Russian state sponsored actors which in my opinion have showed to be some of the most creative and innovative in the way they have conducted their operations not restricted to cyber-espionage. 
 
I also tried to introduce a foundation to this subject in case readers would be interested since it is in my opinion a broad and complex subject but also very interesting. A great reference is [this](https://www.youtube.com/watch?v=gvS4efEakpY&list=PLxA6YRnSzNvINyHpEL5tkDzpu_fKBAXGR&index=1https://www.youtube.com/watch?v=gvS4efEakpY&list=PLxA6YRnSzNvINyHpEL5tkDzpu_fKBAXGR&index=1) presentation by The Grugq, which is the main reference in regards to the foundational information this article is based on, and also [this](https://www.youtube.com/watch?v=2SBq8KOHlAc) presentation by Juan Andress Guerrero-Saade intended to discuss this very subject to the academic sector.
 
<br/>
 
## **Foundation**  
Is important to interpret Information Warfare as the fifth domain of warfare. In contrast with more conventional warfare domains such as Land, Sea or Air, the Cyber domain provides a wide range of capabilities that the previous domains can't provide, also subject to different rules which do not align with previously known strategic basis of the warfare realm.
 
- Actionable on light speed
- Adversary may not have a chance to react
- Relatively cheap
- High innovation involved: Accomplishing strategic goals leveraging different operational objectives can often represent a challenge since it is highly unlikely that leveraged tactics and techniques will succeed twice.
 
 Philosophically speaking, this fifth domain provides the following capabilities in regards to what kind of activities can be leveraged:
 
* **Active** - Direct way of manipulating target's information - eg: Unit8200 was fighting with the PLO. They broke into the computers where the PLO processed all the finances and they transferred money around to make it appear as if there was deep corruption. This strategy worked because there was a degree of real corruption. So this operation spiked the corruption awareness of the [PLO](https://www.ft.com/content/1b870488-7940-11d9-89c5-00000e2511c8). This caused a degree of degradation of capability within the PLO. 
 
* **Passive** - Ability to monitor target's information - Some states are heavily relying on this capability. eg: Snowden [Leaks](https://en.wikipedia.org/wiki/Global_surveillance_disclosures_(2013%E2%80%93present)) NSA's secret global surveillance program to the public. FEYES, PRISM ... etc.
 
* **Physical** - Direct impact on physical targets - eg: Operation Olympic Games or also known as [Stuxnet](https://en.wikipedia.org/wiki/Stuxnet), was deployed to cause substantial damage to Iran's nuclear program by compromising PLCs in Iranian Uranium enrichment facilities, collecting information on industrial systems and causing the fast-spinning centrifuges to tear themselves apart. Another example is the case of Industroyer, involved in the 2016 Ukranian Power Grid blackout.
 
* **Cognitive** - Ability to modify a target's behavior with information - Based on the same foundations as Marketing or Propaganda. Not restricted to distribution of untruthful information or disiniformation, sometimes a target's behavior can be changed by supplying unknown truths. I highly suggest reading about Reflexive Control Theory to know more about the strategies that can be applied with these specific types of operations. Some examples are such as Guccifer 2.0, DCLeaks or the Shadow Brokers.
 
These types of actions are not mutually exclusive, meaning overlaps of these types of activities is likely to happen. 
Based on this information, we can build a high level theoretical overview of the capabilities and realistic outcomes of what can be achieved relying on operations in the fifth domain.
 
<br/>
 
## **Teams**  
Is important to understand that Information Warfare is not just about how computers can be leveraged to achieve a specific strategic outcome, but is also about people and information. These types of operations are conducted by private and public sector companies, with managers, salaries, budgets, ... etc. 
This is an important factor to understand in order to make sense of the dynamics of this domain in terms of toolsets, team capacity and efficacy of operations.
 
A common denominator within all the various types of actors conducting cyber operations is bureaucracy. Bureaucracy enables teams to work at maximum capacity making it fundamental to understand operations, teams and their hierarchy. 
 
*'One may not think that such a thing as Bureaucracy would improve the efficiency of cyber operations, but it does'* - The Grugq. 
 
Based on bureaucracy we can measure the efficiency of a team's capacity on a series of factors. We can call these characteristics the Factors of Team Capacity (based on The Grugq).
 
### **Factors of Team Capacity**  
* **Adaptability** - How well a team can adapt new technologies to be leveraged as part of the team's toolset on cyber conflict and aid to meet specific strategic goals.
 
* **Agility** - How rapid a team can change an operational strategy to achieve a common strategic goal.
 
* **Speed** - How fast a team can implement and execute an idea. Usually a measure of bureaucracy flexibility in terms of the number of abstraction layers (usually denoted in meetings) needed to approve and implement an idea.
 
* **Creativity** - How well and fast a team comes up with newer innovative techniques to achieve operational and tactical outcomes.
 
* **Cohesion** - How well a team works together individually and collectively with other teams and how good they follow the executive order.
 
High cohesion may negatively impact creativity capacity. If there is a very strict set of commands to execute a specific action or a high priority on a finite operational ROI and no investment in innovation, creativity capacity will be damaged consequently.
 
The previous factors serve as a good theoretical standard to measure a given team's efficiency on conducted operations. Likely important is to know that there are various styles in which to organise operational teams. The following table shows Dave Aitel's (former NSA cyber-operative) Meta - operational team structures: 
 
<br/>
<div style="text-align:center"><img src ="https://github.com/ulexec/ulexec.github.io/raw/master/images/dave_aitel_meta.png" /></div>
<br/>
 
A pallet of gray scales exist within these different structure styles, however it is important to understand that for each of these different styles a different degree of bureaucracy, resources and budget is required.
In addition, not all organizations in charge of managing their teams have the same level of bureaucracy. As an example, a private company would not have the same politics as a public sector agency, and even among public sector agencies will have different politics based on various factors, such as state geopolitical status, resources, dedicated budget, ... etc.
 
Bureaucracy is a key enabler to help to interpret different team structures and the reasons why they are grouped the way they are. A good understanding of teams will lead to a good interpretation of their operations and vice versa.
 
<br/>
<br/>
 
## **Russia** 🇷🇺
The Russian Federation existence started with the dissolution of the Soviet Union, which began in the second half of the 1980s with growing unrest in the national republics and ended on 26 December 1991.
According to the Constitution of Russia, the country is an asymmetric federation and semi-presidential republic, wherein the President (Vladimir Putin) is the head of state and the Prime Minister (Dmitry Medvedev) is the head of government.
 
Russia has the largest stockpile of nuclear weapons in the world, the second largest fleet of ballistic missile submarines, and the only modern strategic bomber force outside the United States. More than 90% of the world's 14,000 nuclear weapons are owned by Russia and the United States.
 
There is so much that could be said about Russia in regards to its cultural, political, social and economic aspects which really are far out of the scope of this article.
However, in order to have a naive understanding of Russia's social and economic status the following statistics are supplied based on The CIA's [World Factbook](https://www.cia.gov/library/publications/the-world-factbook/geos/rs.html):
 
<br/>
 
#### **Overview on Modern Russia:**
* Population (July 2018 est.): 142,122,776 
* Gross Domestic Product: $1.578 trillion (2017 est.)
* Gross Domestic Product per Capita: $27,900 (2017 est.)
* Government type: semi-presidential federation
* Ethnic groups (2010 est.):
    * Russian 77.7%
    * Tatar 3.7%
    * Ukrainian 1.4%
    * Bashkir 1.1%
    * Chuvash 1%
    * Chechen 1%
    * other 10.2%
    * unspecified 3.9%
* Languages (2010 est.):
    * Russian (official) 85.7%
    * Tatar 3.2%
    * Chechen 1%
    * other 10.1% 
* Religions (2006 est.):
    * Russian Orthodox 15-20%, 
    * Muslim 10-15%, 
    * other Christian 2% 
* Exports: $353 billion (2017 est.)
    * Commodities: 
        * Petroleum and Petroleum products
        * Natural gas
        * Metals,
        * Wood and wood products
        * Chemicals, 
        * Variety of civilian and military manufactures
    * Partners (2017):
        * China 10.9%
        * Netherlands 10%
        * Germany 7.1%
        * Belarus 5.1%
        * Turkey 4.9% 
* Imports: $238 billion (2017 est.)
    * Commodities: 
        * Machinery
        * Vehicles
        * Pharmaceutical products
        * Plastic
        * Semi-finished metal products
        * Meat
        * Fruits and Nuts
        * Optical and Medical Instruments
        * Iron
        * Steel
    * Partners (2017):
        * China 21.2%
        * Germany 10.7%
        * US 5.6%
        * Belarus 5%
        * Italy 4.5%
        * France 4.2%
 
<br/>
 
 
#### **Intelligence Agencies involved in Cyber Warfare:**
 
Not much is known of private contractors sponsored by the state in order to conduct Information Warfare operations. However it is known that Russian intelligence agencies have engaged in Information Warfare.
A brief overview of these agencies are the following:
 
*   [FSB](https://en.wikipedia.org/wiki/Federal_Security_Service) - The FSB, which Putin briefly ran prior to becoming president, is often described as the main successor agency to the Soviet KGB. Established in 1995, the FSB handles domestic security, cyber security, information operations, and counterterrorism efforts, and, according to a report by the U.S. Senate Committee on Foreign Relations, is the most powerful Russian intelligence agency. The FSB has three main objectives, namely countering foreign intelligence services, combating organized crime, and ensuring economic and financial security.
 
*   [GRU](https://en.wikipedia.org/wiki/GRU_(G.U.)) - The Main Directorate of the General Staff of the Armed Forces of the Russian Federation. The GRU was established by Joseph Stalin′s order of 16 February 1942. The GRU, which dates back to the Soviet era, is the Russian military intelligence agency. In concert with its civilian counterpart, the SVR, the GRU handles external intelligence gathering and operates human intelligence officers. Additionally, it provides military intelligence for the Russian government and oversees Russian special forces (Spetsnaz).
 
*   [SVR](https://themoscowproject.org/explainers/russias-three-intelligence-agencies-explained/) - The SVR, like the FSB, is considered a successor to the Soviet-era KGB and is perhaps the Russian intelligence agency with the lowest profile. Headed by Sergey Naryshkin, the SVR is the civilian counterpart to the GRU, and the two agencies are similar in their responsibilities. Like the GRU, the SVR handles external intelligence gathering and operates human intelligence officers, both under diplomatic cover and as covert officers. More generally, it focuses on collecting intelligence, conducting espionage, implementing active measures, and performing electronic surveillance in foreign countries.
 
It's important to highlight that these Agencies are in a constant state of rivalry. 
 
*'These agencies have been historically competing. Stalin was terrified by the potential formation of a political coup run by the Intelligence Community (the KGB back then) while in times of the Soviet Union, so he created a Military Intelligence Agency (GRU) with the idea to make these agencies compete to prevent the formation of this coup.'* - The Grugq (paraphrased).
 
This rivalry obviously benefits the state in terms of the outcome of their cyber operations, since the high level of competition has a direct impact on innovation and therefore on operational performance.
 
<br/>
 
#### **Teams**
 
Russia uses several small teams of contractors to conduct their cyber operations. These teams are formed from a mix of private, and state and military intelligence actors: 
 
*   [APT28](https://www2.fireeye.com/rs/fireye/images/rpt-apt28.pdf)
*   [APT29](https://www2.fireeye.com/rs/848-DID-242/images/rpt-apt29-hammertoss.pdf)
*   [Turla](https://www.first.org/resources/papers/tbilisi2014/turla-operations_and_development.pdf)
*   [Sandworm](https://www.welivesecurity.com/wp-content/uploads/2017/06/Win32_Industroyer.pdf)
*   [Cyber Berkut](https://en.wikipedia.org/wiki/CyberBerkut)
*   [Gamaredon](https://www.securityweek.com/russian-gamaredon-hackers-back-targeting-ukraine-officials?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+Securityweek+%28SecurityWeek+RSS+Feed%29)
 
<br/>
 
#### **Popular Operations**:
 
Among the different cyber operations conducted by The Russian Federation, we can highlight the following ones:
 
*   [Cuckoo’s Egg](https://en.wikipedia.org/wiki/The_Cuckoo%27s_Egg) - (1986) This was one of the first ⁠— ⁠if not the first ⁠— documented cases of a computer break-in. An intrusion in Lawrence Berkeley National Laboratory (LBNL) in California led to the discovery of a threat actor penetrating military bases around the United States. Later on it was found that the intrusion was coming from West Germany via satellite, West Germany was known to be a proxy of the Soviet Union, and it was later found out that this operation was being funded by the KGB. This operation is important to understand the Russian mindset since it was the first documented case of a nation-sponsored cyber operation. 
 
*   [Moonlight Maze](https://en.wikipedia.org/wiki/Moonlight_Maze) - (1996) This was a government investigation into a massive cyber-espionage operation affecting NASA, the Pentagon, military contractors, civilian academics, the DOE, and numerous other American government agencies. By the end of 1999, the Moonlight Maze task force was composed of forty specialists from Law Enforcement, Military, and Government. The Russian government was blamed for the attacks, although there was initially little hard evidence to back up the US’ accusations besides a Russian IP address that was traced to the hack. However in 2016 Kasperky GReAT found connections that linked Turla with the operation. This operation shows the degree of OPSEC of russian teams, since it took 10 years to achieve concrete attribute conclusions for this specific operation.
 
*   [Attacks Against Estonia](https://en.wikipedia.org/wiki/2007_cyberattacks_on_Estonia) - (2007) series of cyberattacks which began on 27 April 2007 and targeted websites of Estonian organizations, including Estonian parliament, banks, ministries, newspapers and broadcasters, amid the country's disagreement with Russia about the relocation of the Bronze Soldier of Tallinn, an elaborate Soviet-era grave marker, as well as war graves in Tallinn. This operation showcases the first Cyber Deterrence operation exhibited by Russia against a target state. This will become a common operation of the Russian Federation to utilize several more times in coming years. In addition is also a great showcase of cyber adaptability capacity. 
 
*   [Attacks Against Ukranian Power Grid](https://en.wikipedia.org/wiki/December_2015_Ukraine_power_grid_cyberattack) - (2015-2016) Took place on 23 December 2015 and is considered to be the first known successful cyberattack on a power grid. Threat actors were able to successfully compromise information systems of three energy distribution companies in Ukraine and temporarily disrupt electricity supply to the end consumers. Cyber attacks on the energy distribution companies took place during an ongoing conflict in the Ukraine and is attributed to a Russian advanced persistent threat (APT) group known as Sandworm. This operation is a great example of adaptability capacity implemented by Russian operatives, being the first example of a successful breach in Power Grids. Evidence regarding Industroyer, the piece of malware in charge of the latest blackout [reported](https://www.youtube.com/watch?v=TH17hSH1PGQ) by ESET and Dragos show that more features were implemented in the malware despite the capabilities leveraged in this intrusion, constructing a hypothesis that maybe threat actors behind Industroyer were using The Ukranian's Power Grid as a testing ground to evaluate their capabilities.
 
*   [Attack to the Democratic National Convention](https://en.wikipedia.org/wiki/Democratic_National_Committee_cyber_attacks) - (2015-2016) Cyber attacks that successfully penetrated the DNC computing system began in 2015. Attacks by APT29 (FSB/SVR) began in the summer of 2015. Attacks by APT28 (GRU) began in April 2016. It was after the APT28 group began their activities that the compromised system became apparent. The groups were presumed to have been spying on communications, stealing personal accounts of Clinton Campaign employees and volunteers including John Podesta, a former White House chief of staff and chair of Hillary Clinton's 2016 U.S. Both groups of intruders were successfully expelled from the DNC systems within hours after detection. These attacks are considered to be part of a group of recent attacks targeting U.S. government departments and several political organizations, including 2016 campaign organizations. This denotes that different Russian sponsored teams are not necessarily aware of each other's operations.
 
    * [Guccifer 2.0](https://en.wikipedia.org/wiki/Guccifer_2.0) Disinformation Campaign. "Guccifer 2.0" is a persona which claimed to be the hacker(s) that hacked into the Democratic National Committee (DNC) computer network and then leaked its documents to the media, the website WikiLeaks, and a conference event. Some of the documents "Guccifer 2.0" released to the media appear to be forgeries cobbled together from public information and previous hacks, which had been mixed with disinformation.
    According to indictments in February 2018, the persona is operated by Russian military intelligence agency GRU. This is an example of Russia's team agility and creativity capacity leveraging their flexible bureaucracy in order to **transform an unsuccessful espionage operation into a successful disinformation operation**.
 
<br/>
 
*   [2016 US Election Disinformation Campaigns](https://en.wikipedia.org/wiki/Russian_interference_in_the_2016_United_States_elections) - (2016) The Russian government interfered in the 2016 U.S. presidential election with the goal of harming the campaign of Hillary Clinton, boosting the candidacy of Donald Trump, and increasing political and social discord in the United States. According to the special counsel investigation's Mueller Report (officially named "Report on the Investigation into Russian Interference in the 2016 Presidential Election"), the first method of Russian interference used the Internet Research Agency (IRA), a Kremlin-linked troll farm, to wage "a social media campaign that favored presidential candidate Donald J. Trump and disparaged presidential candidate Hillary Clinton". Russian use of social media to disseminate propaganda content was very broad. Facebook and Twitter were used, but also Reddit, Tumblr, Pinterest, Medium, YouTube, Vine, Instagram and Google+ (among other sites). 
This is yet another example of adaptability capacity by Russia's operatives to use different technologies to deploy cognitive based cyber operations following a common strategic goal.
 
* [NotPetya](https://en.wikipedia.org/wiki/Petya_(malware)#Operation) - (2017) A major global cyberattack took place in 2017, utilizing a new variant of a ransomware called Petya, which was later named NotPetya since the malware in question masqueraded as a ransomware and show a high ratio of similarity with Petya, however it was later found out that it was a wiper with no decryption functionality and seems the similarity was meant to disguise. The majority of infections targeted Russia and Ukraine, however there were also infections in France, Germany, Italy, Poland, the United Kingdom, and the United States. It is believed this was a politically-motivated attack against Ukraine, since it occurred on the eve of the Ukrainian holiday Constitution Day. The reason that it became a global cyberattack is believed to be the result of an uncontrolled proliferation of the malware. This shows that this specific sabotage operation was executed poorly although the main strategic goal was accomplished. This could be due to high cohesion executed for this operation but it's just speculation. Estimated losses from Notpetya range the $10 billion, being one of the most disruptive cyber-attacks in history. 
 
* [Olympic Destoryer](https://www.wired.com/story/untold-story-2018-olympics-destroyer-cyberattack/) - (2018) 2018's Winter Olympic Games took place in Pyeongchang, South Korea. Several media outlets reported that technical issues – believed to be caused by a cyber attack – had occurred during the opening ceremony. Cisco Talos, Kaspersky and Intezer cybersecurity firms reported various overlaps the subject piece of malware contained across various pieces of malware linked to DPRK, China and Russia. Wired reported that uncovered further evidence showed that attribution pointed that the operation was work of the FSB, although this is subject to speculation even to this day. Furthermore, this sort of false flags seem to have been also leveraged by Turla as [presented](https://www.youtube.com/watch?v=i_mK13nCOWI) by Brian Bartholomew and Juan Andress Guerrero-Saade, and we've seen something similar with NotPetya masquerading as the ransomware Petya, which in reality was a wiper not really known if it was necessarily related to Petya to this day. This shows the level of awareness of these threat actors of the current Threat Intelligence ecosystem, and how they can disrupt on-going investigations of their operations. This shows great creativity capacity, being Russian threat actors some of the first publicly known actors to have leveraged false flags on a code level granularity to disrupt direct attribution. 
 
For a more detailed overview of most of the engagements by the Russian Federation with offensive cyber capabilities please check this spreadsheet. (On Course)
 
<br/>
 
 
#### **Team Capacity Overview**
 
*   Several Teams competing. Diversity induces innovation.
*   Formal and Informal information sharing within these teams.
*   Certain degree of freedom to fail exercising innovation.
*   Multiple funding sources.
*   Great creativity.
*   Great agility.
*   Great speed.
*   Low/medium cohesion.
*   Excellent adaptability.
 
<br/>
 
#### Remarks of Russia's approach to Cyber Warfare:
*   Offensive Defensive approach.
*   Several small teams style.
*   Conduct disinformation operations by releasing stolen information or leaks introducing falsehoods.
*   Disrupt direct attribution by introducing false flags on their toolsets/operations.
*   Deploy DDoS attacks to conduct deterrence campaigns.
*   Design deterrence/influence operations around target state's political election campaigns or national holidays.
*   Hybrid Warfare - combining military and non-military as well as covert and overt means including disinformation, kinetic actions and cyber-attacks to accomplish a subject strategic outcome.
*   Active Measures - actions of political warfare designed to change the course of world events via influence operations based on disinformation campaigns.
*   Reflexive Control - to influence rival states on their decision making capabilities in a way that the strategic outcome is aligned with the state's interest while the adversary often is not aware of it. Also leveraged via disinformation campaigns.
 
<br/>
 
#### Further Reading:
*   [Russia's approach to Cyber Warfare](https://github.com/n4x0r/n4x0r.github.io/raw/master/files/papers/russia_cyber.pdf)
+   [Cyber and Information warfare in the Ukrainian conflict](https://github.com/n4x0r/n4x0r.github.io/raw/master/files/papers/cyber-and-info-warfare-ukraine.pdf)
*   [Unmasking Maskirovka](https://www.amazon.co.uk/Unmasking-Maskirovka-Russias-Influence-Operations/dp/0578451425/ref=pd_sbs_14_5/262-0245731-1271608?_encoding=UTF8&pd_rd_i=0578451425&pd_rd_r=394b6d92-785e-4921-bb23-da7d79c7bf26&pd_rd_w=zTEx8&pd_rd_wg=faeNa&pf_rd_p=f4a31d1d-8f61-48f5-b6f4-a22ba06df575&pf_rd_r=RFVT85K78X8QZWQ6WG8W&psc=1&refRID=RFVT85K78X8QZWQ6WG8W)
*   [Sandworm: A New Era of Cyberwar and the Hunt for the Kremlin's Most Dangerous Hackers](https://www.amazon.com/Sandworm-Cyberwar-Kremlins-Dangerous-Hackers/dp/0385544405)
*   [Active Measures: The Secret History of Disinformation and Political Warfare](https://www.amazon.com/Active-Measures-History-Disinformation-Political/dp/0374287260)
<br/>
<br/>
<br/>

<!---- 

## China 🇨🇳

<br/>

#### Remarkable Ops: 
*   GhostNet 
*   Byzantine Hades
*   Titan Rain
*   Operation Aurora
*   Shadow Network
*   Cloud Hopper

<br/>

#### Major Related Groups
* [APT1](https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf)
* [APT3](https://www.fireeye.com/current-threats/apt-groups.html#apt3)
* [APT10](https://www.fireeye.com/current-threats/apt-groups.html#apt10)
* [APT15](https://www.welivesecurity.com/wp-content/uploads/2019/07/ESET_Okrum_and_Ketrican.pdf)
* [APT30](https://www.fireeye.com/current-threats/apt-groups.html#apt30)
* [APT41](https://www.fireeye.com/current-threats/apt-groups.html#apt41)
* [APT40](https://www.fireeye.com/current-threats/apt-groups.html#apt40)

<br/>

#### Intelligence Agencies:
*   3rd or 4th department of PLA’s GSD (General Staff Department) - Military intelligence
    *   4th dept - Electronic Cyber Warfare - Offensive Operations 
    *   3rd dept - USD’s NSA equivalent - SIGINT capabilities
*   PLA Unit 61398
*   PLA Unit 61486
*   PLA Unit 78020
*   NMS - (USD’s CIA - FBI equivalent) HUMMINT - non military
*   NPS - CCP. Police Authority. Authors of Great Firewall of China - non military

<br/>

#### Approach on Cyber Warfare:
*   1991 Gulf War loss against Iraq as motivation. Introduction of Netcentric Warfare.
*   Asymmetrical Warfare - asymmetric threats are designed to weaken the security of the Alliance and individual allies, as well as destabilize allied governments and societies.
*   ISR and logistic systems as primary target, since USA heavily relies on them.
*   Informationalization of China to enforce control over their citizens.
*   Goals on Global Information control superiority
*   USA - China military parity by 2050
*   Space based CNC disruption since usd relies on this technology for their logistic operations.
*   Deep understanding of USA technology achieved by reconnaissance and espionage operations.

<br/>

#### Further Reading:
* [China's approach to Cyber Warfare](https://github.com/n4x0r/n4x0r.github.io/raw/master/files/papers/china_cyber.pdf)

<br/>
<br/>
<br/>

## Iran 🇮🇷

<br/>

#### Remarkable Ops:
*   IRGC Cyber Warfare Program 
*   Shammon - attacks on Saudi Arabia
*   Operation Ababil
*   Bowman Dam
*   Rye Brook Dam ICS attack
*   Stuxnet Retaliation
*   Nuclear weapon treaty lifted sanctions on importing advance technology - Jan 2016

<br/>

#### Intelligence Agencies involved in Cyber warfare:
*   IRGC
*   ICA - Iranian Cyber Army
*   Iran support for Hezbollah -  anti IL/USA propaganda.
*   Islamic Cyber Resistance - Hezbollah sponsored

<br/>

#### Approach on Cyber Warfare:
*   Ensure regime survival by surveillance operations
*   Develop a strong cybersecurity task force
*   Reconnaissance operations regarding foreign critical infrastructure architecture on enemy states as potential targets for offensive operations.
*   Scans country to find best students and send them to cyber oriented universities.
*   Stuxnet retaliation as motivation.

<br/>

#### Further Reading:
* [Iran's approach to Cyber Warfare](https://github.com/n4x0r/n4x0r.github.io/raw/master/files/papers/iran_cyber.pdf)

<br/>
<br/>
<br/>

## North Korea 🇰🇵

<br/>

#### Remarkable Ops
*   Sony attack on Oct 2014 - The Guardians of Peace
*   Bangladesh bank breach - 10M dollar theft
*   WannaCry 
*   Money Laundry via Crypto-currency transactions

<br/>

#### Intelligence Agencies involved in Cyber Warfare:
*   RGB - Illegal and clandestine foreign operations - 2017 Kim Jong Un brother assesination.
*   Bureau 121 - US/South korean CNC disruption.
*   GSD - Electronic warfare - Psychological Operations.
*   Command Automation Bureau - Offensive Operations.
*   Korean Computer Center - KCC - Hard/Software research - student recruitment

<br/>

#### Approach on Cyber Warfare:
*   Protect Image of the state and leader of DPRK.
*   Target Logistic and CNC communications to prevent USA additional support on potential conflict in the Korean Peninsula.
*   To Scan the Country to find best talented students aligned with state views to send them to cyber focused universities.
*   Provide a means to engage in illegal and clandestine foreign operations using cybersecurity capabilities to provide economic growth to fund critical state projects for regime survival such as DPRK Nuclear program.

<br/>

#### Further Reading:
* [DPRK's approach to Cyber Warfare](https://github.com/n4x0r/n4x0r.github.io/raw/master/files/papers/NK_cyber.pdf)

 ---!>

