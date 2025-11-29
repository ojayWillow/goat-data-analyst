from backend.domain_detection.patterns import DomainPatterns

ecom = DomainPatterns.get_all_patterns()["e-commerce"]
print("Total keywords:", len(ecom.keywords))
for kw in sorted(ecom.keywords):
    print(kw)
