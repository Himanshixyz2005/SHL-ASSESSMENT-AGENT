import re


def normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def compare_assessments(query, catalog):
    """
    Compare two SHL assessments mentioned in the user's query.
    """

    normalized_query = normalize(query)

    matched = []

    for item in catalog:

        name = item.get("name", "")

        normalized_name = normalize(name)

        # Exact normalized match
        if normalized_name in normalized_query:
            matched.append(item)
            continue

        # Partial token matching
        tokens = name.lower().replace("(", " ").replace(")", " ").split()

        if any(token in query.lower() for token in tokens if len(token) > 2):
            matched.append(item)

    # Remove duplicates
    unique = []

    seen = set()

    for item in matched:

        if item["name"] not in seen:

            unique.append(item)

            seen.add(item["name"])

    if len(unique) < 2:
        return None

    first = unique[0]
    second = unique[1]

    reply = f"""
Comparison between **{first['name']}** and **{second['name']}**

| Feature | {first['name']} | {second['name']} |
|---------|-----------------|------------------|
| Duration | {first.get('duration', 'N/A')} | {second.get('duration', 'N/A')} |
| Remote | {first.get('remote', 'N/A')} | {second.get('remote', 'N/A')} |
| Adaptive | {first.get('adaptive', 'N/A')} | {second.get('adaptive', 'N/A')} |

### {first['name']}
{first.get('description', 'N/A')}

### {second['name']}
{second.get('description', 'N/A')}
"""

    return {
        "reply": reply.strip(),
        "recommendations": [],
        "end_of_conversation": True
    }