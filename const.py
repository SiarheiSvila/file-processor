PROMPT = """You are an expert AI assistant tasked with extracting specific data points from medical and pharmacy plan documents (PDFs). Your goal is to meticulously read the document and populate a JSON structure based on the fields listed below. 
The final output must be a single JSON object with two primary keys: Medical and Pharmacy. 
 
Extraction Guidelines 
Accuracy is critical. For each field ID,
- find the corresponding value in the document. 
- If you cannot find or confidently confirm a value, omit that attribute entirely—do not invent or guess. When the attribute is present, include it in the results.
- When multiple tiers share the same alias in the reference table (e.g., in-network vs. out-of-network rows), output them for each tier-specific value.
- Ignore unrelated tables, footnotes, or marketing text unless they explicitly contain the attribute and value.

Pay attention to network tiers. Many fields are specific to a network tier (e.g.,
- INN,
- OON,
- IN1). Ensure you extract the value for the correct tier as specified in the attribute name. 

Output format
Don't include any format instructions, hust a simple json
The entire output must be a single key-value pair. It should be a JSON that contains array of attributes. Every attribute contains: id and value.
- id is a referenced original id
- value is extracted value exactly as written in the PDF text, but remove currency symbols, percent signs, and unit abbreviations (strip $, %, per day, per visit, days, etc.). Keep the word “None” as-is. Retain other words that are part of the stated benefit. 

Output example format:
[
  {
    "id": 1,
    "value": "value 1"
  },
  {
    "id": 2,
    "value": "value 2"
  }
]

Data Schema 
Below is the detailed schema for the data extraction. Each section includes a description of the attribute type and a list of all fields to be extracted,
- categorized for clarity. 

1. Medical Description: 
This section pertains to the medical benefits of the plan. It covers aspects like overall plan design,
- deductibles,
- out-of-pocket expenses,
- and cost-sharing for various medical services including physician visits,
- hospital stays,
- and emergency services.

Plan: 
1630: Variable Coinsurance Applies (INN-OON)
1631: Coinsurance (INN)
1633: Coinsurance (OON)
1635: Combined Medical/RX Deductible/OOP (INN-OON)

Plan Deductible: 
1638: Plan Deductible - Order of Applicability (INN-OON)
2689: Collective Deductible (INN-OON)
1639: Individual Plan - Indiv Ded Max Amount (INN)
1641: Individual Plan - Indiv Ded Max Amount (OON)
2848: Family Plan - Indiv Ded Max Amount (INN)
2849: Family Plan - Indiv Ded Max Amount (OON)
1642: Family Plan - Family Ded Max Amount (INN)
1644: Family Plan - Family Ded Max Amount (OON)
3609: Individual Plan - Indiv Ded Max Amount (Tier 1) (INN)
3610: Family Plan - Indiv Ded Max Amount (Tier 1) (INN)
3611: Family Plan - Family Ded Max Amount (Tier 1) (INN)
1645: Pharmacy Individual Deductible Cap Amount (INN)
1646: Pharmacy Individual Deductible Cap Amount (OON)
1647: Pharmacy Family Deductible Cap Amount (INN)
1648: Pharmacy Family Dedu ctible Cap Amount (OON)
1649: 3 Month Carryover (INN-OON)
2708: Up Front Individual - Max Amount (IN1)
2709: Up Front Individual - Max Amount (OON)
2710: Up Front Family - Max Amount (IN1)
2711: Up Front Family - Max Amount (OON)

Plan Out of Pocket: 
2690: Collective OOP (INN-OON)
2694: Individual Plan - Indiv OOP Max Amount (INN)
2696: Individual Plan - Indiv OOP Max Amount (OON)
2691: Family Plan - Indiv OOP Max Amount (INN)
2692: Family Plan - Indiv OOP Max Amount (OON)
2697: Family Plan - Family OOP Max Amount (INN)
2699: Family Plan - Family OOP Max Amount (OON)
3612: Individual Plan - Indiv OOP Max Amount (Tier 1) (INN)
3613: Family Plan - Indiv OOP Max Amount (Tier 1) (INN)
3614: Family Plan - Family OOP Max Amount (Tier 1) (INN)
2244: OOP Max Copays Accumulation (INN)
2246: OOP Max Copays Accumulation (OON)
2247: OOP Max Plan Deductible Accumulation (INN)
2249: OOP Max Plan Deductible Accumulation (OON)

Physician Services - Office Visit:
2432: Tiered Services Include (INN)
2688: Cost Share Option (INN)
2427: Non-Reviewed Specialist (INN)
2428: Tier 1 Coinsurance (INN)
2430: Non-Tier 1 Coinsurance (INN)
1657: Combined PCP and Specialist (INN)
1659: Combined PCP and Specialist (OON)
2433: Primary Care Physician Service Tier 1 Copay (INN)
2434: Primary Care Physician Service Tier 1 Coinsurance (INN)
2436: Plan Deductible Applies to Primary Care Physician Service Tier 1 (INN)
1673: Primary Care Physician Service Copay (INN)
1675: Primary Care Physician Service Coinsurance (INN)
1677: Primary Care Physician Service Coinsurance (OON)
1678: Plan Deductible Applies to Primary Care Physician (INN)
1680: Plan Deductible Applies to Primary Care Physician (OON)
2438: Specialty Care Service Tier 1 Copay (INN)
2439: Specialty Care Service Tier 1 Coinsurance (INN)
2441: Plan Deductible Applies to Specialty Care Service Tier 1 (INN)
1700: Specialty Care Service Copay (INN)
1702: Specialty Care Service Coinsurance (INN)
1704: Specialty Care Service Coinsurance (OON)
1705: Plan Deductible Applies to Specialty Care (INN)
1707: Plan Deductible Applies to Specialty Care (OON)
1720: Office Surgery Cost Share Option (INN)
1722: Office Surgery Cost Share Option (OON)
1723: Plan Deductible Applies to Office Surgery (INN)
2679: Plan Deductible Applies to Office Surgery (OON)
3634: Office Surgery PCP Copay Tier 1 (INN)
3635: Office Surgery PCP Coinsurance Tier 1 (INN)
3636: Office Surgery Plan Ded Applies to PCP Tier 1 (INN)
3624: Office Surgery PCP Copay (INN)
3625: Office Surgery PCP Coinsurance (INN)
3626: Office Surgery PCP Coinsurance (OON)
3627: Office Surgery Plan Ded Applies to PCP (INN)
3628: Office Surgery Plan Ded Applies to PCP (OON)
3637: Office Surgery SPC Copay Tier 1 (INN)
3638: Office Surgery SPC Coinsurance Tier 1 (INN)
3639: Office Surgery Plan Ded Applies to SPC Tier 1 (INN)
3629: Office Surgery SPC Copay (INN)
3630: Office Surgery SPC Coinsurance (INN)
3631: Office Surgery SPC Coinsurance (OON)
3632: Office Surgery Plan Ded Applies to SPC (INN)
3633: Office Surgery Plan Ded Applies to SPC (OON)
2673: Alternative Care Annual Maximum (OR/WA Situs States Only) Cost Share Options (INN-OON)

Physician Services - Virtual Care: 
3422: Benefit Steerage Approved (2021 Filing) (INN)
3601: Virtual Primary Care Physician Tier 1 Cost Share Option (INN)
3602: Virtual Primary Care Physician Tier 1 Copay (INN)
3603: Virtual Primary Care Physician Tier 1 Coinsurance (INN)
3604: Plan Deductible Applies to Virtual Primary Care Physician Tier 1 (INN)
3423: Virtual Primary Care Physician Cost Share Option (INN)
3434: Virtual Primary Care Physician Cost Share Option (OON)
3424: Virtual Primary Care Physician Copay (INN)
3425: Virtual Primary Care Physician Coinsurance (INN)
3426: Virtual Primary Care Physician Coinsurance (OON)
3427: Plan Deductible Applies to Virtual Primary Care Physician (INN)
3428: Plan Deductible Applies to Virtual Primary Care Physician (OON)
3605: Virtual Specialty Care Tier 1 Cost Share Option (INN)
3606: Virtual Specialty Care Tier 1 Copay (INN)
3607: Virtual Specialty Care Tier 1 Coinsurance (INN)
3608: Plan Deductible Applies to Virtual Specialty Care Tier 1 (INN)
3599: Virtual Specialty Care Cost Share Option (INN)
3600: Virtual Specialty Care Cost Share Option (OON)
3429: Virtual Specialty Care Copay (INN)
3430: Virtual Specialty Care Coinsurance (INN)
3431: Virtual Specialty Care Coinsurance (OON)
3432: Plan Deductible Applies to Virtual Specialty Care (INN)
3433: Plan Deductible Applies to Virtual Specialty Care (OON)

Inpatient Hospital: 
1775: Copay Options (INN)
1778: Copay Options (OON)
1785: Per Admit Copay (INN)
1787: Per Admit Copay (OON)
1788: Per Day Copay (INN)
1790: Per Day Copay (OON)
1791: Annual Day Limit (INN)
1793: Annual Day Limit (OON)
1782: Coinsurance (INN)
1784: Coinsurance (OON)
1779: Plan Deductible Applies (INN)
1781: Plan Deductible Applies (OON)

Outpatient Facility Services: 
1797: Copay (INN)
1799: Copay (OON)
1794: Coinsurance (INN)
1796: Coinsurance (OON)
1800: Plan Deductible Applies (INN)
1802: Plan Deductible Applies (OON)

Emergency Services: 
1837: Emergency Room (ER) Copay (INN-OON)
1838: Emergency Room (ER) Coinsurance (INN-OON)
1847: Plan Deductible Applies (ER) (INN-OON)
2685: Urgent Care Cost Share Option (INN)
2686: Urgent Care Cost Share Option (OON)
1848: Urgent Care Facility (UC) Copay (INN)
1850: Urgent Care Facility (UC) Copay (OON)
1851: Urgent Care Facility (UC) Coinsurance (INN)
1853: Urgent Care Facility (UC) Coinsurance (OON)
1854: Plan Deductible Applies (UC) (INN)
1856: Plan Deductible Applies (UC) (OON)
3381: Ambulance Coinsurance (INN)
3382: Ambulance Coinsurance (OON)
3384: Ambulance Plan Deductible Applies (INN)
3385: Ambulance Plan Deductible Applies (OON)
1858: Ambulance Day Limit Amount (INN-OON)
3650: Ambulance MHSUD Coinsurance (INN)
3651: Ambulance MHSUD Coinsurance (OON)
3652: Ambulance MHSUD Plan Deductible Applies (INN)
3653: Ambulance MHSUD Plan Deductible Applies (OON)

Laboratory Services: 
1870: Physicians Services - Office Visit (INN)
1872: Physicians Services - Office Visit (OON)
2378: Physicians Services - Office Visit Coinsurance (INN)
2498: Physicians Services - Office Visit Coinsurance (OON)
1873: Plan Deductible Applies at Physicians Services - Office Visit (INN)
2495: Plan Deductible Applies at Physicians Services - Office Visit (OON)
2572: Outpatient Facility Cost Share (INN)
1874: Outpatient Facility Coinsurance (INN)
1876: Outpatient Facility Coinsurance (OON)
1880: Plan Deductible Applies at Outpatient Facility (INN)
1882: Plan Deductible Applies at Outpatient Facility (OON)
1883: Independent Lab Facility Cost Share (INN)
1885: Independent Lab Facility Coinsurance (INN)
1887: Independent Lab Facility Coinsurance (OON)
1891: Plan Deductible Applies at Independent Lab Facility (INN)
1893: Plan Deductible Applies at Independent Lab Facility (OON)

Medical Pharmaceuticals: 
2019: Covered at Inpatient Facility (INN)
2021: Covered at Inpatient Facility (OON)
3469: Cigna Pathwell Specialty Network Included (INN)
3470: Cigna Pathwell Specialty Drugs Covered (INN)
3471: Cigna Pathwell Specialty Drugs Covered (OON)
3472: Cigna Pathwell Specialty Drugs Pricing (INN)
3473: Cigna Pathwell Specialty Drugs Preferred Pricing Option (INN)
3474: Cigna Pathwell Specialty Drugs Copay (INN)
3475: Cigna Pathwell Specialty Drugs Coinsurance (INN)
3590: Cigna Pathwell Specialty Drugs Coinsurance (OON)
3476: Plan Deductible Applies to Cigna Pathwell Specialty Drugs (INN)
3591: Plan Deductible Applies to Cigna Pathwell Specialty Drugs (OON)
3477: Other Medical Pharmaceutical Drugs Covered (INN)
3478: Other Medical Pharmaceutical Drugs Covered (OON)
3479: Other Medical Pharmaceutical Drugs Copay (INN)
3480: Other Medical Pharmaceutical Drugs Coinsurance (INN)
3481: Other Medical Pharmaceutical Drug Coinsurance (OON)
3482: Plan Deductible Applies to Other Medical Pharmaceutical Drugs (INN)
3483: Plan Deductible Applies to Other Medical Pharmaceutical Drugs (OON)
2022: Covered at Outpatient Facility (INN)
2024: Covered at Outpatient Facility (OON)
2025: Outpatient Facility Coinsurance (INN)
2027: Outpatient Facility Coinsurance (OON)
2028: Plan Deductible Applies at Outpatient Facility (INN)
2030: Plan Deductible Applies at Outpatient Facility (OON)
2031: Covered at Physician's Office Setting (INN)
2033: Covered at Physician's Office Setting (OON)
2912: Physician Office Cost Share Options (INN)
2034: Physician Office Coinsurance (INN)
2036: Physician Office Coinsurance (OON)
2037: Plan Deductible Applies at Physician's Office (INN)
2039: Plan Deductible Applies at Physician's Office (OON)
2040: Covered at Home Setting (INN)
2042: Covered at Home Setting (OON)
2043: Home Setting Coinsurance (INN)
2045: Home Setting Coinsurance (OON)
2046: Plan Deductible Applies at Home Setting (INN)
2048: Plan Deductible Applies at Home Setting (OON)

2. Pharmacy Description: This section pertains to the pharmacy benefits of the plan. It includes details on the pharmacy network,
- drug formulary,
- cost-sharing for different drug tiers (generic,
- brand),
- supply limits,
- home delivery options,
- and various clinical programs related to prescriptions.

Plan: 
2717: Pharmacy Plan Design (IN1)
2250: Pharmacy Network (IN1)
3641: Client Anchor (IN1)
3592: Precision Network (INN)
2252: Formulary/Prescription Drug List (IN1)
2251: Tier Selection (IN1)
3597: Generic Tiering (INN)
3598: Specialty Tiering (INN)
2253: Dispensing Requirement (IN1)
3211: Cost Share Processing Logic (IN1)
2254: Out-of-network Pharmacy Benefits (OON)
2255: Pharmacy Deductible - Individual (IN1)
2256: Pharmacy Deductible - Individual (OON)
2257: Pharmacy Deductible - Family (IN1)
2258: Pharmacy Deductible - Family (OON)
2259: Pharmacy OOP Maximum - Individual (IN1)
2260: Pharmacy OOP Maximum - Individual (OON)
2261: Pharmacy OOP Maximum - Family (IN1)
2262: Pharmacy OOP Maximum - Family (OON)
2263: Pharmacy Deductible Accumulates to Pharmacy OOP (IN1)
2264: Home Delivery Accumulates to Pharmacy OOP (IN1)
2907: Pharmacy Discount Option (IN1)
3215: Pharmacy Rebate Option (IN1)
3670: EnReachRx for Cigna Healthcare (INN)
2368: Pharmacy Pricing (IN1)
2908: Combined Med/RX Ded/OOP (IN1)

Supply Limit:
2281: Non-Specialty Drugs - Day Supply Limit - Retail (IN1)
2282: Non-Specialty Drugs - Day Supply Limit - Home Delivery (IN1)
2283: Specialty Drugs - Day Supply Limit - Retail (IN1)
2284: Specialty Drugs - Day Supply Limit - Home Delivery (IN1)
3386: Clinical Day Supply Program (INN)
3387: Up to 15 Days Supply (Split Fill) (INN)
3388: 30-90 Days Supply Maximums (INN)
3389: Customer Cost Proration (INN)

Retail Cost Share:
2285: Retail Cost Share Type (IN1)
2286: Retail Cost Share Type (OON)
2287: Retail Min/Max Option for Coinsurance (IN1)
2289: Oral Specialty Drugs Cost Share (IN1)
2872: Retail Flat Customer Coinsurance (IN1)
2290: Retail Flat Customer Coinsurance (OON)
2291: Retail Generic Copay (IN1)
2293: Retail Generic Customer Coinsurance (IN1)
2295: Retail Generic Minimum Copay (IN1)
2297: Retail Generic Maximum Copay (IN1)
2299: Deductible Applies to In Network Retail - Generic (IN1)
3500: Retail Pref Generic Copay (INN)
3501: Retail Pref Generic Customer Coinsurance (INN)
3502: Retail Pref Generic Minimum Copay (INN)
3503: Retail Pref Generic Maximum Copay (INN )
3504: Deductible Applies to In Network Retail - Pref Generic (INN)
3505: Retail Non Pref Generic Copay (INN)
3506: Retail Non Pref Generic Customer Coinsurance (INN)
3507: Retail Non Pref Generic Minimum Copay (INN)
3508: Retail Non Pref Generic Maximum Copay (INN)
3509: Deductible Applies to In Network Retail - Non Pref Generic (INN)
2300: Retail Pref Brand Copay (IN1)
2302: Retail Pref Brand Customer Coinsurance (IN1)
2304: Retail Pref Brand Minimum Copay (IN1)
2306: Retail Pref Brand Maximum Copay (IN1)
2308: Deductible Applies to In Network Retail - Pref Brand (IN1)
2309: Retail Non Pref Brand Copay (IN1)
2311: Retail Non Pref Brand Customer Coinsurance (IN1)
2313: Retail Non Pref Brand Minimum Copay (IN1)
2315: Retail Non Pref Brand Maximum Copay (IN1)
2317: Deductible Applies to In Network Retail - Non Pref Brand (IN1)
2318: Retail Specialty Copay (IN1)
2320: Retail Specialty Customer Coinsurance (IN1)
2322: Retail Specialty Minimum Copay (IN1)
2324: Retail Specialty Maximum Copay (IN1)
2326: Deductible Applies to In Network Retail - Specialty (IN1)
3510: Retail Pref Specialty Copay (INN)
3511: Retail Pref Specialty Customer Coinsurance (INN)
3512: Retail Pref Specialty Minimum Copay (INN)
3513: Retail Pref Specialty Maximum Copay (INN)
3514: Deductible Applies to In Network Retail - Pref Specialty (INN)
3515: Retail Non Pref Specialty Copay (INN)
3516: Retail Non Pref Specialty Customer Coinsurance (INN)
3517: Retail Non Pref Specialty Minimum Copay (INN)
3518: Retail Non Pref Specialty Maximum Copay (INN)
3519: Deductible Applies to In Network Retail - Non Pref Specialty (INN)
2763: 90 Day Retail Benefit Cost Share (copay multiplier) (IN1)
2764: Retail Generic Copay (90 Days) (IN1)
2765: Retail Generic Customer Coinsurance (90 Days) (IN1)
2766: Retail Generic Minimum Copay (90 Days) (IN1)
2767: Retail Generic Maximum Copay (90 Days) (IN1)
2768: Deductible Applies to In Network Retail - Generic (90 Days) (IN1)
3520: Retail Pref Generic Copay (90 Days) (INN)
3521: Retail Pref Generic Customer Coinsurance (90 Days) (INN)
3522: Retail Pref Generic Minimum Copay (90 Days) (INN)
3523: Retail Pref Generic Maximum Copay (90 Days) (INN)
3524: Deductible Applies to In Network Retail - Pref Generic (90 Days) (INN)
3525: Retail Non Pref Generic Copay (90 Days) (INN)
3526: Retail Non Pref Generic Customer Coinsurance (90 Days) (INN)
3527: Retail Non Pref Generic Minimum Copay (90 Days) (INN)
3528: Retail Non Pref Generic Maximum Copay (90 Days) (INN)
3529: Deductible Applies to In Network Retail - Non Pref Generic (90 Days) (INN)
2769: Retail Pref Brand Copay (90 Days) (IN1)
2770: Retail Pref Brand Customer Coinsurance (90 Days) (IN1)
2771: Retail Pref Brand Minimum Copay (90 Days) (IN1)
2772: Retail Pref Brand Maximum Copay (90 Days) (IN1)
2773: Deductible Applies to In Network Retail - Pref Brand (90 Days) (IN1)
2774: Retail Non Pref Brand Copay (90 Days) (IN1)
2775: Retail Non Pref Brand Customer Coinsurance (90 Days) (IN1)
2776: Retail Non Pref Brand Minimum Copay (90 Days) (IN1)
2777: Retail Non Pref Brand Maximum Copay (90 Days) (IN1)
2778: Deductible Applies to In Network Retail - Non Pref Brand (90 Days) (IN1)
2819: Retail Specialty Copay (90 Days) (IN1)
2815: Retail Specialty Customer Coinsurance (90 Days) (IN1)
2816: Retail Specialty Minimum Copay (90 Days) (IN1)
2817: Retail Specialty Maximum Copay (90 Days) (IN1)
2818: Deductible Applies to In Network Retail - Specialty (90 Days) (IN1)
3530: Retail Pref Specialty Copay (90 Days) (INN)
3531: Retail Pref Specialty Customer Coinsurance (90 Days) (INN)
3532: Retail Pref Specialty Minimum Copay (90 Days) (INN)
3533: Retail Pref Specialty Maximum Copay (90 Days) (INN)
3534: Deductible Applies to In Network Retail - Pref Specialty (90 Days) (INN)
3535: Retail Non Pref Specialty Copay (90 Days) (INN)
3536: Retail Non Pref Specialty Customer Coinsurance (90 Days) (INN)
3537: Retail Non Pref Specialty Minimum Copay (90 Days) (INN)
3538: Retail Non Pref Specialty Maximum Copay (90 Days) (INN)
3539: Deductible Applies to In Network Retail - Non Pref Specialty (90 Days) (INN)
2909: Retail Individual Deductible (IN1)

90 Day Program:
2779: 90 Day Program Type (IN1)
2780: Number of 30 Day Fills Allowed (IN1)

Home Delivery Cost Share:
2327: Home Delivery Cost Share Type (IN1)
2328: Home Delivery Cost Share Type (OON)
2873: Home Delivery Flat Customer Coinsurance (IN1)
2329: Home Delivery Min/Max Option for Coinsurance (IN1)
2781: Home delivery Benefit Cost Share (copay multiplier) (IN1)
2330: Home Delivery Generic Copay (IN1)
2331: Home Delivery Generic Customer Coinsurance (IN1)
2332: Home Delivery Generic Minimum Copay (IN1)
2333: Home Delivery Generic Maximum Copay (IN1)
2334: Deductible Applies to In Network Home Delivery - Generic (IN1)
3540: Home Delivery Pref Generic Copay (INN)
3541: Home Delivery Pref Generic Customer Coinsurance (INN)
3542: Home Delivery Pref Generic Minimum Copay (INN)
3543: Home Delivery Pref Generic Maximum Copay (INN)
3544: Deductible Applies to In Network Home Delivery - Pref Generic (INN)
3545: Home Delivery Non Pref Generic Copay (INN)
3546: Home Delivery Non Pref Generic Customer Coinsurance (INN)
3547: Home Delivery Non Pref Generic Minimum Copay (INN)
3548: Home Delivery Non Pref Generic Maximum Copay (INN)
3549: Deductible Applies to In Network Home Delivery - Non Pref Generic (INN)
2335: Home Delivery Pref Brand Copay (IN1)
2336: Home Delivery Pref Brand Customer Coinsurance (IN1)
2337: Home Delivery Pref Brand Minimum Copay (IN1)
2338: Home Delivery Pref Brand Maximum Copay (IN1)
2339: Deductible Applies to In Network Home Delivery - Pref Brand (IN1)
2340: Home Delivery Non Pref Brand Copay (IN
2341: Home Delivery Non Pref Brand Customer Coinsurance (IN1)
2342: Home Delivery Non Pref Brand Minimum Copay (IN1)
2343: Home Delivery Non Pref Brand Maximum Copay (IN1)
2344: Deductible Applies to In Network Home Delivery - Non Pref Brand (IN1)
2345: Home Delivery Specialty Copay (IN1)
2346: Home Delivery Specialty Customer Coinsurance (IN1)
2347: Home Delivery Specialty Minimum Copay (IN1)
2348: Home Delivery Specialty Maximum Copay (IN1)
2349: Deductible Applies to In Network Home Delivery Specialty (IN1)
3550: Home Delivery Pref Specialty Copay (INN)
3551: Home Delivery Pref Specialty Customer Coinsurance (INN)
3552: Home Delivery Pref Specialty Minimum Copay (INN)
3553: Home Delivery Pref Specialty Maximum Copay (INN)
3554: Deductible Applies to In Network Home Delivery - Pref Specialty (INN)
3555: Home Delivery Non Pref Specialty Copay (INN)
3556: Home Delivery Non Pref Specialty Customer Coinsurance (INN)
3557: Home Delivery Non Pref Specialty Minimum Copay (INN)
3558: Home Delivery Non Pref Specialty Maximum Copay (INN)
3559: Deductible Applies to In Network Home Delivery - Non Pref Specialty (INN)

Home Delivery Programs:
3225: Out-of-Pocket Adjuster Program (IN1)
3270: SaveOnSP Programs (IN1)
2350: Exclusive Specialty Home Delivery Program (Med Access Option) (IN1)
2351: Number of Exclusive Specialty Retail Fills Allowed (IN1)
2352: Maintenance Home Delivery Program (IN1)
2353: Number of Maintenance Retail Fills Allowed (IN1)
2354: Maintenance Drug List (IN1)

Reproductive Drug List Options:
2267: PPACA Contraceptive Devices and Drugs (IN1)
2268: Contraceptive Devices and Drugs Buy-Up (IN1)
2269: Oral Fertility Drugs (IN1)
3263: Fertility - Injectable (IN1)
3264: Fertility - Intra-Vaginal (IN1)

Preventive Drugs Cost Share Enrichment:
2355: Preventive Drugs Management (IN1)
3265: Generics (IN1)
3266: Generic Customer Cost Share (IN1)
3267: Brand Drugs (IN1)
3268: Brand Drugs Customer Cost Share (IN1)
3269: Applies When Dispensed At (IN1)
EncircleRx for Cigna Programs:

3649: EncircleRx for Cigna: Weight Management (IN1)

Drug List Options:
2271: PPACA Prenatal Vitamins (IN1)
2272: Prescription Vitamins Buy-Up (IN1)
2273: Prescription Weight Loss Drugs (IN1)
2274: PPACA Smoking Cessation (IN1)
2275: Smoking Cessation Buy-Up (IN1)
2270: Lifestyle Drugs (IN1)
2276: Insulin (IN1)
2277: Diabetic Supplies (IN1)
2278: Diabetic Pens & cartridges (IN1)
2266: Optional Self Injectable (Excludes Infertility) (INN)
2761: Proton Pump Inhibitors (Ulcer drugs) (IN1)
2762: Non-Sedating Anti-histamines (IN1)
2265: Drug Removal Table (IN1)

Clinical Program:
2820: Non-SRx Drug Management Program (IN1)
2782: Specialty Drug Management (IN1)
2363: Specialty Condition Counseling (previously TheraCare) (IN1)
2906: Pay & Communicate (Step Therapy) (IN1)
2893: Grandfathering (Step Therapy) (IN1)
2892: Grandfathering (Prior Auth - SRx and Non-SRx) (IN1)
2364: Complex Psych (IN1)
2365: Narcotic Therapy Management Program (IN1)

Patient Assurance Program:
3232: Patient Assurance Program (IN1)
3233: Cost Share Accumulates To (IN1)
3234: Pharma Mfg Discount Accumulates To (IN1)
"""


SOURCE_DATAFRAME = [
    [1630, 'Medical', 'Plan', 'Variable Coinsurance Applies', 'INN-OON'],
    [1631, 'Medical', 'Plan', 'Coinsurance', 'INN'],
    [1633, 'Medical', 'Plan', 'Coinsurance', 'OON'],
    [1635, 'Medical', 'Plan', 'Combined Medical/RX Deductible/OOP', 'INN-OON'],
    [1638, 'Medical', 'Plan Deductible', 'Plan Deductible - Order of Applicability', 'INN-OON'],
    [2689, 'Medical', 'Plan Deductible', 'Collective Deductible', 'INN-OON'],
    [1639, 'Medical', 'Plan Deductible', 'Individual Plan - Indiv Ded Max Amount', 'INN'],
    [1641, 'Medical', 'Plan Deductible', 'Individual Plan - Indiv Ded Max Amount', 'OON'],
    [2848, 'Medical', 'Plan Deductible', 'Family Plan - Indiv Ded Max Amount', 'INN'],
    [2849, 'Medical', 'Plan Deductible', 'Family Plan - Indiv Ded Max Amount', 'OON'],
    [1642, 'Medical', 'Plan Deductible', 'Family Plan - Family Ded Max Amount', 'INN'],
    [1644, 'Medical', 'Plan Deductible', 'Family Plan - Family Ded Max Amount', 'OON'],
    [3609, 'Medical', 'Plan Deductible', 'Individual Plan - Indiv Ded Max Amount (Tier 1)', 'INN'],
    [3610, 'Medical', 'Plan Deductible', 'Family Plan - Indiv Ded Max Amount (Tier 1)', 'INN'],
    [3611, 'Medical', 'Plan Deductible', 'Family Plan - Family Ded Max Amount (Tier 1)', 'INN'],
    [1645, 'Medical', 'Plan Deductible', 'Pharmacy Individual Deductible Cap Amount', 'INN'],
    [1646, 'Medical', 'Plan Deductible', 'Pharmacy Individual Deductible Cap Amount', 'OON'],
    [1647, 'Medical', 'Plan Deductible', 'Pharmacy Family Deductible Cap Amount', 'INN'],
    [1648, 'Medical', 'Plan Deductible', 'Pharmacy Family Deductible Cap Amount', 'OON'],
    [1649, 'Medical', 'Plan Deductible', '3 Month Carryover', 'INN-OON'],
    [2708, 'Medical', 'Plan Deductible', 'Up Front Individual - Max Amount', 'IN1'],
    [2709, 'Medical', 'Plan Deductible', 'Up Front Individual - Max Amount', 'OON'],
    [2710, 'Medical', 'Plan Deductible', 'Up Front Family - Max Amount', 'IN1'],
    [2711, 'Medical', 'Plan Deductible', 'Up Front Family - Max Amount', 'OON'],
    [2690, 'Medical', 'Plan Out of Pocket', 'Collective OOP', 'INN-OON'],
    [2694, 'Medical', 'Plan Out of Pocket', 'Individual Plan - Indiv OOP Max Amount', 'INN'],
    [2696, 'Medical', 'Plan Out of Pocket', 'Individual Plan - Indiv OOP Max Amount', 'OON'],
    [2691, 'Medical', 'Plan Out of Pocket', 'Family Plan - Indiv OOP Max Amount', 'INN'],
    [2692, 'Medical', 'Plan Out of Pocket', 'Family Plan - Indiv OOP Max Amount', 'OON'],
    [2697, 'Medical', 'Plan Out of Pocket', 'Family Plan - Family OOP Max Amount', 'INN'],
    [2699, 'Medical', 'Plan Out of Pocket', 'Family Plan - Family OOP Max Amount', 'OON'],
    [3612, 'Medical', 'Plan Out of Pocket', 'Individual Plan - Indiv OOP Max Amount (Tier 1)', 'INN'],
    [3613, 'Medical', 'Plan Out of Pocket', 'Family Plan - Indiv OOP Max Amount (Tier 1)', 'INN'],
    [3614, 'Medical', 'Plan Out of Pocket', 'Family Plan - Family OOP Max Amount (Tier 1)', 'INN'],
    [2244, 'Medical', 'Plan Out of Pocket', 'OOP Max Copays Accumulation', 'INN'],
    [2246, 'Medical', 'Plan Out of Pocket', 'OOP Max Copays Accumulation', 'OON'],
    [2247, 'Medical', 'Plan Out of Pocket', 'OOP Max Plan Deductible Accumulation', 'INN'],
    [2249, 'Medical', 'Plan Out of Pocket', 'OOP Max Plan Deductible Accumulation', 'OON'],
    [2432, 'Medical', 'Physician Services - Office Visit', 'Tiered Services Include', 'INN'],
    [2688, 'Medical', 'Physician Services - Office Visit', 'Cost Share Option', 'INN'],
    [2427, 'Medical', 'Physician Services - Office Visit', 'Non-Reviewed Specialist', 'INN'],
    [2428, 'Medical', 'Physician Services - Office Visit', 'Tier 1 Coinsurance', 'INN'],
    [2430, 'Medical', 'Physician Services - Office Visit', 'Non-Tier 1 Coinsurance', 'INN'],
    [1657, 'Medical', 'Physician Services - Office Visit', 'Combined PCP and Specialist', 'INN'],
    [1659, 'Medical', 'Physician Services - Office Visit', 'Combined PCP and Specialist', 'OON'],
    [2433, 'Medical', 'Physician Services - Office Visit', 'Primary Care Physician Service Tier 1 Copay', 'INN'],
    [2434, 'Medical', 'Physician Services - Office Visit', 'Primary Care Physician Service Tier 1 Coinsurance', 'INN'],
    [2436, 'Medical', 'Physician Services - Office Visit', 'Plan Deductible Applies to Primary Care Physician Service Tier 1', 'INN'],
    [1673, 'Medical', 'Physician Services - Office Visit', 'Primary Care Physician Service Copay', 'INN'],
    [1675, 'Medical', 'Physician Services - Office Visit', 'Primary Care Physician Service Coinsurance', 'INN'],
    [1677, 'Medical', 'Physician Services - Office Visit', 'Primary Care Physician Service Coinsurance', 'OON'],
    [1678, 'Medical', 'Physician Services - Office Visit', 'Plan Deductible Applies to Primary Care Physician', 'INN'],
    [1680, 'Medical', 'Physician Services - Office Visit', 'Plan Deductible Applies to Primary Care Physician', 'OON'],
    [2438, 'Medical', 'Physician Services - Office Visit', 'Specialty Care Service Tier 1 Copay', 'INN'],
    [2439, 'Medical', 'Physician Services - Office Visit', 'Specialty Care Service Tier 1 Coinsurance', 'INN'],
    [2441, 'Medical', 'Physician Services - Office Visit', 'Plan Deductible Applies to Specialty Care Service Tier 1', 'INN'],
    [1700, 'Medical', 'Physician Services - Office Visit', 'Specialty Care Service Copay', 'INN'],
    [1702, 'Medical', 'Physician Services - Office Visit', 'Specialty Care Service Coinsurance', 'INN'],
    [1704, 'Medical', 'Physician Services - Office Visit', 'Specialty Care Service Coinsurance', 'OON'],
    [1705, 'Medical', 'Physician Services - Office Visit', 'Plan Deductible Applies to Specialty Care', 'INN'],
    [1707, 'Medical', 'Physician Services - Office Visit', 'Plan Deductible Applies to Specialty Care', 'OON'],
    [1720, 'Medical', 'Physician Services - Office Visit', 'Office Surgery Cost Share Option', 'INN'],
    [1722, 'Medical', 'Physician Services - Office Visit', 'Office Surgery Cost Share Option', 'OON'],
    [1723, 'Medical', 'Physician Services - Office Visit', 'Plan Deductible Applies to Office Surgery', 'INN'],
    [2679, 'Medical', 'Physician Services - Office Visit', 'Plan Deductible Applies to Office Surgery', 'OON'],
    [3634, 'Medical', 'Physician Services - Office Visit', 'Office Surgery PCP Copay Tier 1', 'INN'],
    [3635, 'Medical', 'Physician Services - Office Visit', 'Office Surgery PCP Coinsurance Tier 1', 'INN'],
    [3636, 'Medical', 'Physician Services - Office Visit', 'Office Surgery Plan Ded Applies to PCP Tier 1', 'INN'],
    [3624, 'Medical', 'Physician Services - Office Visit', 'Office Surgery PCP Copay', 'INN'],
    [3625, 'Medical', 'Physician Services - Office Visit', 'Office Surgery PCP Coinsurance', 'INN'],
    [3626, 'Medical', 'Physician Services - Office Visit', 'Office Surgery PCP Coinsurance', 'OON'],
    [3627, 'Medical', 'Physician Services - Office Visit', 'Office Surgery Plan Ded Applies to PCP', 'INN'],
    [3628, 'Medical', 'Physician Services - Office Visit', 'Office Surgery Plan Ded Applies to PCP', 'OON'],
    [3637, 'Medical', 'Physician Services - Office Visit', 'Office Surgery SPC Copay Tier 1', 'INN'],
    [3638, 'Medical', 'Physician Services - Office Visit', 'Office Surgery SPC Coinsurance Tier 1', 'INN'],
    [3639, 'Medical', 'Physician Services - Office Visit', 'Office Surgery Plan Ded Applies to SPC Tier 1', 'INN'],
    [3629, 'Medical', 'Physician Services - Office Visit', 'Office Surgery SPC Copay', 'INN'],
    [3630, 'Medical', 'Physician Services - Office Visit', 'Office Surgery SPC Coinsurance', 'INN'],
    [3631, 'Medical', 'Physician Services - Office Visit', 'Office Surgery SPC Coinsurance', 'OON'],
    [3632, 'Medical', 'Physician Services - Office Visit', 'Office Surgery Plan Ded Applies to SPC', 'INN'],
    [3633, 'Medical', 'Physician Services - Office Visit', 'Office Surgery Plan Ded Applies to SPC', 'OON'],
    [2673, 'Medical', 'Physician Services - Office Visit', 'Alternative Care Annual Maximum (OR/WA Situs States Only) Cost Share Options', 'INN-OON'],
    [3422, 'Medical', 'Physician Services - Virtual Care', 'Benefit Steerage Approved (2021 Filing)', 'INN'],
    [3601, 'Medical', 'Physician Services - Virtual Care', 'Virtual Primary Care Physician Tier 1 Cost Share Option', 'INN'],
    [3602, 'Medical', 'Physician Services - Virtual Care', 'Virtual Primary Care Physician Tier 1 Copay', 'INN'],
    [3603, 'Medical', 'Physician Services - Virtual Care', 'Virtual Primary Care Physician Tier 1 Coinsurance', 'INN'],
    [3604, 'Medical', 'Physician Services - Virtual Care', 'Plan Deductible Applies to Virtual Primary Care Physician Tier 1', 'INN'],
    [3423, 'Medical', 'Physician Services - Virtual Care', 'Virtual Primary Care Physician Cost Share Option', 'INN'],
    [3434, 'Medical', 'Physician Services - Virtual Care', 'Virtual Primary Care Physician Cost Share Option', 'OON'],
    [3424, 'Medical', 'Physician Services - Virtual Care', 'Virtual Primary Care Physician Copay', 'INN'],
    [3425, 'Medical', 'Physician Services - Virtual Care', 'Virtual Primary Care Physician Coinsurance', 'INN'],
    [3426, 'Medical', 'Physician Services - Virtual Care', 'Virtual Primary Care Physician Coinsurance', 'OON'],
    [3427, 'Medical', 'Physician Services - Virtual Care', 'Plan Deductible Applies to Virtual Primary Care Physician', 'INN'],
    [3428, 'Medical', 'Physician Services - Virtual Care', 'Plan Deductible Applies to Virtual Primary Care Physician', 'OON'],
    [3605, 'Medical', 'Physician Services - Virtual Care', 'Virtual Specialty Care Tier 1 Cost Share Option', 'INN'],
    [3606, 'Medical', 'Physician Services - Virtual Care', 'Virtual Specialty Care Tier 1 Copay', 'INN'],
    [3607, 'Medical', 'Physician Services - Virtual Care', 'Virtual Specialty Care Tier 1 Coinsurance', 'INN'],
    [3608, 'Medical', 'Physician Services - Virtual Care', 'Plan Deductible Applies to Virtual Specialty Care Tier 1', 'INN'],
    [3599, 'Medical', 'Physician Services - Virtual Care', 'Virtual Specialty Care Cost Share Option', 'INN'],
    [3600, 'Medical', 'Physician Services - Virtual Care', 'Virtual Specialty Care Cost Share Option', 'OON'],
    [3429, 'Medical', 'Physician Services - Virtual Care', 'Virtual Specialty Care Copay', 'INN'],
    [3430, 'Medical', 'Physician Services - Virtual Care', 'Virtual Specialty Care Coinsurance', 'INN'],
    [3431, 'Medical', 'Physician Services - Virtual Care', 'Virtual Specialty Care Coinsurance', 'OON'],
    [3432, 'Medical', 'Physician Services - Virtual Care', 'Plan Deductible Applies to Virtual Specialty Care', 'INN'],
    [3433, 'Medical', 'Physician Services - Virtual Care', 'Plan Deductible Applies to Virtual Specialty Care', 'OON'],
    [1775, 'Medical', 'Inpatient Hospital', 'Copay Options', 'INN'],
    [1778, 'Medical', 'Inpatient Hospital', 'Copay Options', 'OON'],
    [1785, 'Medical', 'Inpatient Hospital', 'Per Admit Copay', 'INN'],
    [1787, 'Medical', 'Inpatient Hospital', 'Per Admit Copay', 'OON'],
    [1788, 'Medical', 'Inpatient Hospital', 'Per Day Copay', 'INN'],
    [1790, 'Medical', 'Inpatient Hospital', 'Per Day Copay', 'OON'],
    [1791, 'Medical', 'Inpatient Hospital', 'Annual Day Limit', 'INN'],
    [1793, 'Medical', 'Inpatient Hospital', 'Annual Day Limit', 'OON'],
    [1782, 'Medical', 'Inpatient Hospital', 'Coinsurance', 'INN'],
    [1784, 'Medical', 'Inpatient Hospital', 'Coinsurance', 'OON'],
    [1779, 'Medical', 'Inpatient Hospital', 'Plan Deductible Applies', 'INN'],
    [1781, 'Medical', 'Inpatient Hospital', 'Plan Deductible Applies', 'OON'],
    [1797, 'Medical', 'Outpatient Facility Services', 'Copay', 'INN'],
    [1799, 'Medical', 'Outpatient Facility Services', 'Copay', 'OON'],
    [1794, 'Medical', 'Outpatient Facility Services', 'Coinsurance', 'INN'],
    [1796, 'Medical', 'Outpatient Facility Services', 'Coinsurance', 'OON'],
    [1800, 'Medical', 'Outpatient Facility Services', 'Plan Deductible Applies', 'INN'],
    [1802, 'Medical', 'Outpatient Facility Services', 'Plan Deductible Applies', 'OON'],
    [1837, 'Medical', 'Emergency Services', 'Emergency Room (ER) Copay', 'INN-OON'],
    [1838, 'Medical', 'Emergency Services', 'Emergency Room (ER) Coinsurance', 'INN-OON'],
    [1847, 'Medical', 'Emergency Services', 'Plan Deductible Applies (ER)', 'INN-OON'],
    [2685, 'Medical', 'Emergency Services', 'Urgent Care Cost Share Option', 'INN'],
    [2686, 'Medical', 'Emergency Services', 'Urgent Care Cost Share Option', 'OON'],
    [1848, 'Medical', 'Emergency Services', 'Urgent Care Facility (UC) Copay', 'INN'],
    [1850, 'Medical', 'Emergency Services', 'Urgent Care Facility (UC) Copay', 'OON'],
    [1851, 'Medical', 'Emergency Services', 'Urgent Care Facility (UC) Coinsurance', 'INN'],
    [1853, 'Medical', 'Emergency Services', 'Urgent Care Facility (UC) Coinsurance', 'OON'],
    [1854, 'Medical', 'Emergency Services', 'Plan Deductible Applies (UC)', 'INN'],
    [1856, 'Medical', 'Emergency Services', 'Plan Deductible Applies (UC)', 'OON'],
    [3381, 'Medical', 'Emergency Services', 'Ambulance Coinsurance', 'INN'],
    [3382, 'Medical', 'Emergency Services', 'Ambulance Coinsurance', 'OON'],
    [3384, 'Medical', 'Emergency Services', 'Ambulance Plan Deductible Applies', 'INN'],
    [3385, 'Medical', 'Emergency Services', 'Ambulance Plan Deductible Applies', 'OON'],
    [1858, 'Medical', 'Emergency Services', 'Ambulance Day Limit Amount', 'INN-OON'],
    [3650, 'Medical', 'Emergency Services', 'Ambulance MHSUD Coinsurance', 'INN'],
    [3651, 'Medical', 'Emergency Services', 'Ambulance MHSUD Coinsurance', 'OON'],
    [3652, 'Medical', 'Emergency Services', 'Ambulance MHSUD Plan Deductible Applies', 'INN'],
    [3653, 'Medical', 'Emergency Services', 'Ambulance MHSUD Plan Deductible Applies', 'OON'],
    [1870, 'Medical', 'Laboratory Services', 'Physicians Services - Office Visit', 'INN'],
    [1872, 'Medical', 'Laboratory Services', 'Physicians Services - Office Visit', 'OON'],
    [2378, 'Medical', 'Laboratory Services', 'Physicians Services - Office Visit Coinsurance', 'INN'],
    [2498, 'Medical', 'Laboratory Services', 'Physicians Services - Office Visit Coinsurance', 'OON'],
    [1873, 'Medical', 'Laboratory Services', 'Plan Deductible Applies at Physicians Services - Office Visit', 'INN'],
    [2495, 'Medical', 'Laboratory Services', 'Plan Deductible Applies at Physicians Services - Office Visit', 'OON'],
    [2572, 'Medical', 'Laboratory Services', 'Outpatient Facility Cost Share', 'INN'],
    [1874, 'Medical', 'Laboratory Services', 'Outpatient Facility Coinsurance', 'INN'],
    [1876, 'Medical', 'Laboratory Services', 'Outpatient Facility Coinsurance', 'OON'],
    [1880, 'Medical', 'Laboratory Services', 'Plan Deductible Applies at Outpatient Facility', 'INN'],
    [1882, 'Medical', 'Laboratory Services', 'Plan Deductible Applies at Outpatient Facility', 'OON'],
    [1883, 'Medical', 'Laboratory Services', 'Independent Lab Facility Cost Share', 'INN'],
    [1885, 'Medical', 'Laboratory Services', 'Independent Lab Facility Coinsurance', 'INN'],
    [1887, 'Medical', 'Laboratory Services', 'Independent Lab Facility Coinsurance', 'OON'],
    [1891, 'Medical', 'Laboratory Services', 'Plan Deductible Applies at Independent Lab Facility', 'INN'],
    [1893, 'Medical', 'Laboratory Services', 'Plan Deductible Applies at Independent Lab Facility', 'OON'],
    [2019, 'Medical', 'Medical Pharmaceuticals', 'Covered at Inpatient Facility', 'INN'],
    [2021, 'Medical', 'Medical Pharmaceuticals', 'Covered at Inpatient Facility', 'OON'],
    [3469, 'Medical', 'Medical Pharmaceuticals', 'Cigna Pathwell Specialty Network Included', 'INN'],
    [3470, 'Medical', 'Medical Pharmaceuticals', 'Cigna Pathwell Specialty Drugs Covered', 'INN'],
    [3471, 'Medical', 'Medical Pharmaceuticals', 'Cigna Pathwell Specialty Drugs Covered', 'OON'],
    [3472, 'Medical', 'Medical Pharmaceuticals', 'Cigna Pathwell Specialty Drugs Pricing', 'INN'],
    [3473, 'Medical', 'Medical Pharmaceuticals', 'Cigna Pathwell Specialty Drugs Preferred Pricing Option', 'INN'],
    [3474, 'Medical', 'Medical Pharmaceuticals', 'Cigna Pathwell Specialty Drugs Copay', 'INN'],
    [3475, 'Medical', 'Medical Pharmaceuticals', 'Cigna Pathwell Specialty Drugs Coinsurance', 'INN'],
    [3590, 'Medical', 'Medical Pharmaceuticals', 'Cigna Pathwell Specialty Drugs Coinsurance', 'OON'],
    [3476, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies to Cigna Pathwell Specialty Drugs', 'INN'],
    [3591, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies to Cigna Pathwell Specialty Drugs', 'OON'],
    [3477, 'Medical', 'Medical Pharmaceuticals', 'Other Medical Pharmaceutical Drugs Covered', 'INN'],
    [3478, 'Medical', 'Medical Pharmaceuticals', 'Other Medical Pharmaceutical Drugs Covered', 'OON'],
    [3479, 'Medical', 'Medical Pharmaceuticals', 'Other Medical Pharmaceutical Drugs Copay', 'INN'],
    [3480, 'Medical', 'Medical Pharmaceuticals', 'Other Medical Pharmaceutical Drugs Coinsurance', 'INN'],
    [3481, 'Medical', 'Medical Pharmaceuticals', 'Other Medical Pharmaceutical Drug Coinsurance', 'OON'],
    [3482, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies to Other Medical Pharmaceutical Drugs', 'INN'],
    [3483, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies to Other Medical Pharmaceutical Drugs', 'OON'],
    [2022, 'Medical', 'Medical Pharmaceuticals', 'Covered at Outpatient Facility', 'INN'],
    [2024, 'Medical', 'Medical Pharmaceuticals', 'Covered at Outpatient Facility', 'OON'],
    [2025, 'Medical', 'Medical Pharmaceuticals', 'Outpatient Facility Coinsurance', 'INN'],
    [2027, 'Medical', 'Medical Pharmaceuticals', 'Outpatient Facility Coinsurance', 'OON'],
    [2028, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies at Outpatient Facility', 'INN'],
    [2030, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies at Outpatient Facility', 'OON'],
    [2031, 'Medical', 'Medical Pharmaceuticals', 'Covered at Physician\'s Office Setting', 'INN'],
    [2033, 'Medical', 'Medical Pharmaceuticals', 'Covered at Physician\'s Office Setting', 'OON'],
    [2912, 'Medical', 'Medical Pharmaceuticals', 'Physician Office Cost Share Options', 'INN'],
    [2034, 'Medical', 'Medical Pharmaceuticals', 'Physician Office Coinsurance', 'INN'],
    [2036, 'Medical', 'Medical Pharmaceuticals', 'Physician Office Coinsurance', 'OON'],
    [2037, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies at Physician\'s Office', 'INN'],
    [2039, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies at Physician\'s Office', 'OON'],
    [2040, 'Medical', 'Medical Pharmaceuticals', 'Covered at Home Setting', 'INN'],
    [2042, 'Medical', 'Medical Pharmaceuticals', 'Covered at Home Setting', 'OON'],
    [2043, 'Medical', 'Medical Pharmaceuticals', 'Home Setting Coinsurance', 'INN'],
    [2045, 'Medical', 'Medical Pharmaceuticals', 'Home Setting Coinsurance', 'OON'],
    [2046, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies at Home Setting', 'INN'],
    [2048, 'Medical', 'Medical Pharmaceuticals', 'Plan Deductible Applies at Home Setting', 'OON'],
    [2717, 'Pharmacy', 'Plan', 'Pharmacy Plan Design', 'IN1'],
    [2250, 'Pharmacy', 'Plan', 'Pharmacy Network', 'IN1'],
    [3641, 'Pharmacy', 'Plan', 'Client Anchor', 'IN1'],
    [3592, 'Pharmacy', 'Plan', 'Precision Network', 'INN'],
    [2252, 'Pharmacy', 'Plan', 'Formulary/Prescription Drug List', 'IN1'],
    [2251, 'Pharmacy', 'Plan', 'Tier Selection', 'IN1'],
    [3597, 'Pharmacy', 'Plan', 'Generic Tiering', 'INN'],
    [3598, 'Pharmacy', 'Plan', 'Specialty Tiering', 'INN'],
    [2253, 'Pharmacy', 'Plan', 'Dispensing Requirement', 'IN1'],
    [3211, 'Pharmacy', 'Plan', 'Cost Share Processing Logic', 'IN1'],
    [2254, 'Pharmacy', 'Plan', 'Out-of-network Pharmacy Benefits', 'OON'],
    [2255, 'Pharmacy', 'Plan', 'Pharmacy Deductible - Individual', 'IN1'],
    [2256, 'Pharmacy', 'Plan', 'Pharmacy Deductible - Individual', 'OON'],
    [2257, 'Pharmacy', 'Plan', 'Pharmacy Deductible - Family', 'IN1'],
    [2258, 'Pharmacy', 'Plan', 'Pharmacy Deductible - Family', 'OON'],
    [2259, 'Pharmacy', 'Plan', 'Pharmacy OOP Maximum - Individual', 'IN1'],
    [2260, 'Pharmacy', 'Plan', 'Pharmacy OOP Maximum - Individual', 'OON'],
    [2261, 'Pharmacy', 'Plan', 'Pharmacy OOP Maximum - Family', 'IN1'],
    [2262, 'Pharmacy', 'Plan', 'Pharmacy OOP Maximum - Family', 'OON'],
    [2263, 'Pharmacy', 'Plan', 'Pharmacy Deductible Accumulates to Pharmacy OOP', 'IN1'],
    [2264, 'Pharmacy', 'Plan', 'Home Delivery Accumulates to Pharmacy OOP', 'IN1'],
    [2907, 'Pharmacy', 'Plan', 'Pharmacy Discount Option', 'IN1'],
    [3215, 'Pharmacy', 'Plan', 'Pharmacy Rebate Option', 'IN1'],
    [3670, 'Pharmacy', 'Plan', 'EnReachRx for Cigna Healthcare', 'INN'],
    [2368, 'Pharmacy', 'Plan', 'Pharmacy Pricing', 'IN1'],
    [2908, 'Pharmacy', 'Plan', 'Combined Med/RX Ded/OOP', 'IN1'],
    [2281, 'Pharmacy', 'Supply Limit', 'Non-Specialty Drugs - Day Supply Limit - Retail', 'IN1'],
    [2282, 'Pharmacy', 'Supply Limit', 'Non-Specialty Drugs - Day Supply Limit - Home Delivery', 'IN1'],
    [2283, 'Pharmacy', 'Supply Limit', 'Specialty Drugs - Day Supply Limit - Retail', 'IN1'],
    [2284, 'Pharmacy', 'Supply Limit', 'Specialty Drugs - Day Supply Limit - Home Delivery', 'IN1'],
    [3386, 'Pharmacy', 'Supply Limit', 'Clinical Day Supply Program', 'INN'],
    [3387, 'Pharmacy', 'Supply Limit', 'Up to 15 Days Supply (Split Fill)', 'INN'],
    [3388, 'Pharmacy', 'Supply Limit', '30-90 Days Supply Maximums', 'INN'],
    [3389, 'Pharmacy', 'Supply Limit', 'Customer Cost Proration', 'INN'],
    [2285, 'Pharmacy', 'Retail Cost Share', 'Retail Cost Share Type', 'IN1'],
    [2286, 'Pharmacy', 'Retail Cost Share', 'Retail Cost Share Type', 'OON'],
    [2287, 'Pharmacy', 'Retail Cost Share', 'Retail Min/Max Option for Coinsurance', 'IN1'],
    [2289, 'Pharmacy', 'Retail Cost Share', 'Oral Specialty Drugs Cost Share', 'IN1'],
    [2872, 'Pharmacy', 'Retail Cost Share', 'Retail Flat Customer Coinsurance', 'IN1'],
    [2290, 'Pharmacy', 'Retail Cost Share', 'Retail Flat Customer Coinsurance', 'OON'],
    [2291, 'Pharmacy', 'Retail Cost Share', 'Retail Generic Copay', 'IN1'],
    [2293, 'Pharmacy', 'Retail Cost Share', 'Retail Generic Customer Coinsurance', 'IN1'],
    [2295, 'Pharmacy', 'Retail Cost Share', 'Retail Generic Minimum Copay', 'IN1'],
    [2297, 'Pharmacy', 'Retail Cost Share', 'Retail Generic Maximum Copay', 'IN1'],
    [2299, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Generic', 'IN1'],
    [3500, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Generic Copay', 'INN'],
    [3501, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Generic Customer Coinsurance', 'INN'],
    [3502, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Generic Minimum Copay', 'INN'],
    [3503, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Generic Maximum Copay', 'INN'],
    [3504, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Pref Generic', 'INN'],
    [3505, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Generic Copay', 'INN'],
    [3506, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Generic Customer Coinsurance', 'INN'],
    [3507, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Generic Minimum Copay', 'INN'],
    [3508, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Generic Maximum Copay', 'INN'],
    [3509, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Non Pref Generic', 'INN'],
    [2300, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Brand Copay', 'IN1'],
    [2302, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Brand Customer Coinsurance', 'IN1'],
    [2304, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Brand Minimum Copay', 'IN1'],
    [2306, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Brand Maximum Copay', 'IN1'],
    [2308, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Pref Brand', 'IN1'],
    [2309, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Brand Copay', 'IN1'],
    [2311, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Brand Customer Coinsurance', 'IN1'],
    [2313, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Brand Minimum Copay', 'IN1'],
    [2315, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Brand Maximum Copay', 'IN1'],
    [2317, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Non Pref Brand', 'IN1'],
    [2318, 'Pharmacy', 'Retail Cost Share', 'Retail Specialty Copay', 'IN1'],
    [2320, 'Pharmacy', 'Retail Cost Share', 'Retail Specialty Customer Coinsurance', 'IN1'],
    [2322, 'Pharmacy', 'Retail Cost Share', 'Retail Specialty Minimum Copay', 'IN1'],
    [2324, 'Pharmacy', 'Retail Cost Share', 'Retail Specialty Maximum Copay', 'IN1'],
    [2326, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Specialty', 'IN1'],
    [3510, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Specialty Copay', 'INN'],
    [3511, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Specialty Customer Coinsurance', 'INN'],
    [3512, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Specialty Minimum Copay', 'INN'],
    [3513, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Specialty Maximum Copay', 'INN'],
    [3514, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Pref Specialty', 'INN'],
    [3515, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Specialty Copay', 'INN'],
    [3516, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Specialty Customer Coinsurance', 'INN'],
    [3517, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Specialty Minimum Copay', 'INN'],
    [3518, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Specialty Maximum Copay', 'INN'],
    [3519, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Non Pref Specialty', 'INN'],
    [2763, 'Pharmacy', 'Retail Cost Share', '90 Day Retail Benefit Cost Share (copay multiplier)', 'IN1'],
    [2764, 'Pharmacy', 'Retail Cost Share', 'Retail Generic Copay (90 Days)', 'IN1'],
    [2765, 'Pharmacy', 'Retail Cost Share', 'Retail Generic Customer Coinsurance (90 Days)', 'IN1'],
    [2766, 'Pharmacy', 'Retail Cost Share', 'Retail Generic Minimum Copay (90 Days)', 'IN1'],
    [2767, 'Pharmacy', 'Retail Cost Share', 'Retail Generic Maximum Copay (90 Days)', 'IN1'],
    [2768, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Generic (90 Days)', 'IN1'],
    [3520, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Generic Copay (90 Days)', 'INN'],
    [3521, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Generic Customer Coinsurance (90 Days)', 'INN'],
    [3522, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Generic Minimum Copay (90 Days)', 'INN'],
    [3523, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Generic Maximum Copay (90 Days)', 'INN'],
    [3524, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Pref Generic (90 Days)', 'INN'],
    [3525, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Generic Copay (90 Days)', 'INN'],
    [3526, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Generic Customer Coinsurance (90 Days)', 'INN'],
    [3527, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Generic Minimum Copay (90 Days)', 'INN'],
    [3528, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Generic Maximum Copay (90 Days)', 'INN'],
    [3529, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Non Pref Generic (90 Days)', 'INN'],
    [2769, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Brand Copay (90 Days)', 'IN1'],
    [2770, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Brand Customer Coinsurance (90 Days)', 'IN1'],
    [2771, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Brand Minimum Copay (90 Days)', 'IN1'],
    [2772, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Brand Maximum Copay (90 Days)', 'IN1'],
    [2773, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Pref Brand (90 Days)', 'IN1'],
    [2774, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Brand Copay (90 Days)', 'IN1'],
    [2775, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Brand Customer Coinsurance (90 Days)', 'IN1'],
    [2776, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Brand Minimum Copay (90 Days)', 'IN1'],
    [2777, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Brand Maximum Copay (90 Days)', 'IN1'],
    [2778, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Non Pref Brand (90 Days)', 'IN1'],
    [2819, 'Pharmacy', 'Retail Cost Share', 'Retail Specialty Copay (90 Days)', 'IN1'],
    [2815, 'Pharmacy', 'Retail Cost Share', 'Retail Specialty Customer Coinsurance (90 Days)', 'IN1'],
    [2816, 'Pharmacy', 'Retail Cost Share', 'Retail Specialty Minimum Copay (90 Days)', 'IN1'],
    [2817, 'Pharmacy', 'Retail Cost Share', 'Retail Specialty Maximum Copay (90 Days)', 'IN1'],
    [2818, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Specialty (90 Days)', 'IN1'],
    [3530, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Specialty Copay (90 Days)', 'INN'],
    [3531, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Specialty Customer Coinsurance (90 Days)', 'INN'],
    [3532, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Specialty Minimum Copay (90 Days)', 'INN'],
    [3533, 'Pharmacy', 'Retail Cost Share', 'Retail Pref Specialty Maximum Copay (90 Days)', 'INN'],
    [3534, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Pref Specialty (90 Days)', 'INN'],
    [3535, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Specialty Copay (90 Days)', 'INN'],
    [3536, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Specialty Customer Coinsurance (90 Days)', 'INN'],
    [3537, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Specialty Minimum Copay (90 Days)', 'INN'],
    [3538, 'Pharmacy', 'Retail Cost Share', 'Retail Non Pref Specialty Maximum Copay (90 Days)', 'INN'],
    [3539, 'Pharmacy', 'Retail Cost Share', 'Deductible Applies to In Network Retail - Non Pref Specialty (90 Days)', 'INN'],
    [2909, 'Pharmacy', 'Retail Cost Share', 'Retail Individual Deductible', 'IN1'],
    [2779, 'Pharmacy', '90 Day Program', '90 Day Program Type', 'IN1'],
    [2780, 'Pharmacy', '90 Day Program', 'Number of 30 Day Fills Allowed', 'IN1'],
    [2327, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Cost Share Type', 'IN1'],
    [2328, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Cost Share Type', 'OON'],
    [2873, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Flat Customer Coinsurance', 'IN1'],
    [2329, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Min/Max Option for Coinsurance', 'IN1'],
    [2781, 'Pharmacy', 'Home Delivery Cost Share', 'Home delivery Benefit Cost Share (copay multiplier)', 'IN1'],
    [2330, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Generic Copay', 'IN1'],
    [2331, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Generic Customer Coinsurance', 'IN1'],
    [2332, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Generic Minimum Copay', 'IN1'],
    [2333, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Generic Maximum Copay', 'IN1'],
    [2334, 'Pharmacy', 'Home Delivery Cost Share', 'Deductible Applies to In Network Home Delivery - Generic', 'IN1'],
    [3540, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Generic Copay', 'INN'],
    [3541, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Generic Customer Coinsurance', 'INN'],
    [3542, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Generic Minimum Copay', 'INN'],
    [3543, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Generic Maximum Copay', 'INN'],
    [3544, 'Pharmacy', 'Home Delivery Cost Share', 'Deductible Applies to In Network Home Delivery - Pref Generic', 'INN'],
    [3545, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Generic Copay', 'INN'],
    [3546, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Generic Customer Coinsurance', 'INN'],
    [3547, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Generic Minimum Copay', 'INN'],
    [3548, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Generic Maximum Copay', 'INN'],
    [3549, 'Pharmacy', 'Home Delivery Cost Share', 'Deductible Applies to In Network Home Delivery - Non Pref Generic', 'INN'],
    [2335, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Brand Copay', 'IN1'],
    [2336, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Brand Customer Coinsurance', 'IN1'],
    [2337, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Brand Minimum Copay', 'IN1'],
    [2338, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Brand Maximum Copay', 'IN1'],
    [2339, 'Pharmacy', 'Home Delivery Cost Share', 'Deductible Applies to In Network Home Delivery - Pref Brand', 'IN1'],
    [2340, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Brand Copay', 'IN1'],
    [2341, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Brand Customer Coinsurance', 'IN1'],
    [2342, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Brand Minimum Copay', 'IN1'],
    [2343, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Brand Maximum Copay', 'IN1'],
    [2344, 'Pharmacy', 'Home Delivery Cost Share', 'Deductible Applies to In Network Home Delivery - Non Pref Brand', 'IN1'],
    [2345, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Specialty Copay', 'IN1'],
    [2346, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Specialty Customer Coinsurance', 'IN1'],
    [2347, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Specialty Minimum Copay', 'IN1'],
    [2348, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Specialty Maximum Copay', 'IN1'],
    [2349, 'Pharmacy', 'Home Delivery Cost Share', 'Deductible Applies to In Network Home Delivery Specialty', 'IN1'],
    [3550, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Specialty Copay', 'INN'],
    [3551, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Specialty Customer Coinsurance', 'INN'],
    [3552, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Specialty Minimum Copay', 'INN'],
    [3553, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Pref Specialty Maximum Copay', 'INN'],
    [3554, 'Pharmacy', 'Home Delivery Cost Share', 'Deductible Applies to In Network Home Delivery - Pref Specialty', 'INN'],
    [3555, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Specialty Copay', 'INN'],
    [3556, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Specialty Customer Coinsurance', 'INN'],
    [3557, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Specialty Minimum Copay', 'INN'],
    [3558, 'Pharmacy', 'Home Delivery Cost Share', 'Home Delivery Non Pref Specialty Maximum Copay', 'INN'],
    [3559, 'Pharmacy', 'Home Delivery Cost Share', 'Deductible Applies to In Network Home Delivery - Non Pref Specialty', 'INN'],
    [3225, 'Pharmacy', 'Home Delivery Programs', 'Out-of-Pocket Adjuster Program', 'IN1'],
    [3270, 'Pharmacy', 'Home Delivery Programs', 'SaveOnSP Programs', 'IN1'],
    [2350, 'Pharmacy', 'Home Delivery Programs', 'Exclusive Specialty Home Delivery Program (Med Access Option)', 'IN1'],
    [2351, 'Pharmacy', 'Home Delivery Programs', 'Number of Exclusive Specialty Retail Fills Allowed', 'IN1'],
    [2352, 'Pharmacy', 'Home Delivery Programs', 'Maintenance Home Delivery Program', 'IN1'],
    [2353, 'Pharmacy', 'Home Delivery Programs', 'Number of Maintenance Retail Fills Allowed', 'IN1'],
    [2354, 'Pharmacy', 'Home Delivery Programs', 'Maintenance Drug List', 'IN1'],
    [2267, 'Pharmacy', 'Reproductive Drug List Options', 'PPACA Contraceptive Devices and Drugs', 'IN1'],
    [2268, 'Pharmacy', 'Reproductive Drug List Options', 'Contraceptive Devices and Drugs Buy-Up', 'IN1'],
    [2269, 'Pharmacy', 'Reproductive Drug List Options', 'Oral Fertility Drugs', 'IN1'],
    [3263, 'Pharmacy', 'Reproductive Drug List Options', 'Fertility - Injectable', 'IN1'],
    [3264, 'Pharmacy', 'Reproductive Drug List Options', 'Fertility - Intra-Vaginal', 'IN1'],
    [2355, 'Pharmacy', 'Preventive Drugs Cost Share Enrichment', 'Preventive Drugs Management', 'IN1'],
    [3265, 'Pharmacy', 'Preventive Drugs Cost Share Enrichment', 'Generics', 'IN1'],
    [3266, 'Pharmacy', 'Preventive Drugs Cost Share Enrichment', 'Generic Customer Cost Share', 'IN1'],
    [3267, 'Pharmacy', 'Preventive Drugs Cost Share Enrichment', 'Brand Drugs', 'IN1'],
    [3268, 'Pharmacy', 'Preventive Drugs Cost Share Enrichment', 'Brand Drugs Customer Cost Share', 'IN1'],
    [3269, 'Pharmacy', 'Preventive Drugs Cost Share Enrichment', 'Applies When Dispensed At', 'IN1'],
    [3649, 'Pharmacy', 'EncircleRx for Cigna Programs', 'EncircleRx for Cigna: Weight Management', 'IN1'],
    [2271, 'Pharmacy', 'Drug List Options', 'PPACA Prenatal Vitamins', 'IN1'],
    [2272, 'Pharmacy', 'Drug List Options', 'Prescription Vitamins Buy-Up', 'IN1'],
    [2273, 'Pharmacy', 'Drug List Options', 'Prescription Weight Loss Drugs', 'IN1'],
    [2274, 'Pharmacy', 'Drug List Options', 'PPACA Smoking Cessation', 'IN1'],
    [2275, 'Pharmacy', 'Drug List Options', 'Smoking Cessation Buy-Up', 'IN1'],
    [2270, 'Pharmacy', 'Drug List Options', 'Lifestyle Drugs', 'IN1'],
    [2276, 'Pharmacy', 'Drug List Options', 'Insulin', 'IN1'],
    [2277, 'Pharmacy', 'Drug List Options', 'Diabetic Supplies', 'IN1'],
    [2278, 'Pharmacy', 'Drug List Options', 'Diabetic Pens & cartridges', 'IN1'],
    [2266, 'Pharmacy', 'Drug List Options', 'Optional Self Injectable (Excludes Infertility)', 'INN'],
    [2761, 'Pharmacy', 'Drug List Options', 'Proton Pump Inhibitors (Ulcer drugs)', 'IN1'],
    [2762, 'Pharmacy', 'Drug List Options', 'Non-Sedating Anti-histamines', 'IN1'],
    [2265, 'Pharmacy', 'Drug List Options', 'Drug Removal Table', 'IN1'],
    [2820, 'Pharmacy', 'Clinical Program', 'Non-SRx Drug Management Program', 'IN1'],
    [2782, 'Pharmacy', 'Clinical Program', 'Specialty Drug Management', 'IN1'],
    [2363, 'Pharmacy', 'Clinical Program', 'Specialty Condition Counseling (previously TheraCare)', 'IN1'],
    [2906, 'Pharmacy', 'Clinical Program', 'Pay & Communicate (Step Therapy)', 'IN1'],
    [2893, 'Pharmacy', 'Clinical Program', 'Grandfathering (Step Therapy)', 'IN1'],
    [2892, 'Pharmacy', 'Clinical Program', 'Grandfathering (Prior Auth - SRx and Non-SRx)', 'IN1'],
    [2364, 'Pharmacy', 'Clinical Program', 'Complex Psych', 'IN1'],
    [2365, 'Pharmacy', 'Clinical Program', 'Narcotic Therapy Management Program', 'IN1'],
    [3232, 'Pharmacy', 'Patient Assurance Program', 'Patient Assurance Program', 'IN1'],
    [3233, 'Pharmacy', 'Patient Assurance Program', 'Cost Share Accumulates To', 'IN1'],
    [3234, 'Pharmacy', 'Patient Assurance Program', 'Pharma Mfg Discount Accumulates To', 'IN1']
]