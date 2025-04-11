import json

# Load the JSON data (list of dicts)
with open("funds_data.json", "r") as f:
    data = json.load(f)

# Build reference index
security_index = []

for fund in data:
    entry = {
        "schemeName": fund.get("schemeName"),
        "shortName": fund.get("name"),
        "isin": fund.get("isin"),
        "internalSecurityId": fund.get("internalSecurityId"),
        "schemeCode": fund.get("schemeCode"),
        "amcName": fund.get("amcName"),
        "securityType": fund.get("securityType"),
        "category": fund.get("category"),
        "subCategory": fund.get("subCategory"),
        "aum": fund.get("aum"),
        "riskOMeter": fund.get("riskOMeter"),
        "returns": {
            "1D": fund.get("1DReturns"),
            "1M": fund.get("1MReturns"),
            "1Y": fund.get("1YReturns"),
            "3Y": fund.get("3YReturns"),
            "5Y": fund.get("5YReturns")
        },
        "nav": fund.get("nav"),
        "navDate": fund.get("navDate"),
        "benchmark": fund.get("benchmarkIndex"),
        "fundManagers": [fm["name"] for fm in fund.get("fundManagersInfo", [])],
        "assetAllocation": fund.get("assetAllocation", {})
    }
    security_index.append(entry)

# Save index (optional)
with open("security_reference_index.json", "w") as f:
    json.dump(security_index, f, indent=4)

print(f"✅ Indexed {len(security_index)} mutual funds.")
