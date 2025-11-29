\# Performance Testing Report

\*\*Date:\*\* 2025-11-29  

\*\*Dataset:\*\* customer\_spending\_1M\_2018\_2025.csv



\## Results



| Metric | Value | Target | Status |

|--------|-------|--------|--------|

| Rows | 1,000,000 | 500K-1M | ✅ |

| Processing Time | 14.39s | <60s | ✅ |

| Memory | Normal | No leaks | ✅ |

| Report Generated | Yes | Yes | ✅ |

| AI Insights Quality | Good | High | ✅ |



\## Breakdown

\- Load: 1.33s

\- Profile: 5.34s

\- Domain: 0.00s

\- Analytics: 4.19s

\- AI Insights: 3.54s (7 insights)



\## Issues Found



\### Critical: Domain confidence too low (16%)

\- Dataset: Pure customer data

\- Expected: 50%+

\- Actual: 16%

\- Impact: Misclassification risk

\- Action: Investigate domain pattern weights



\## AI Insights Quality

✅ Specific and actionable

✅ References actual data (mean age 46.65, avg spend $1416)

✅ Business-relevant recommendations



