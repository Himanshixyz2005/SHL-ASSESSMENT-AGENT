import json
import re

STOPWORDS = {
    "i", "me", "my", "we", "our",
    "need", "want", "looking",
    "for", "the", "a", "an",
    "to", "of", "with", "show",
    "actually", "please", "only",
    "can", "you", "is", "are",
    "some", "assessment", "assessments",
    "test", "tests"
}

# Query normalization
SYNONYMS = {
    "developer": ["developer", "programmer", "software"],
    "java": ["java", "spring", "jdk"],
    "python": ["python", "django", "flask"],
    "technical": ["technical", "coding", "programming", "knowledge"],
    "personality": ["personality", "behavioral", "behavioural", "opq"],
    "cognitive": ["cognitive", "ability", "reasoning", "aptitude"],
    "graduate": ["graduate", "entry", "junior"],
    "mid": ["mid", "mid-level", "professional"],
    "senior": ["senior", "lead", "manager"]
}
TECH_BOOST = {
    "java": ["java"],
    "python": ["python"],
    "sql": ["sql", "database"],
    "linux": ["linux", "unix"],
    "c++": ["c++"],
    "c#": ["c#"],
    ".net": [".net", "asp.net"],
    "javascript": ["javascript", "node", "react"],
}

def load_catalog(file_path="data/catalog.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_query(query):
    query = query.lower()
    query = re.sub(r"[^a-z0-9\s-]", " ", query)

    words = []

    for word in query.split():
        if word not in STOPWORDS:
            words.append(word)

    expanded = []

    for word in words:
        expanded.append(word)

        for key, values in SYNONYMS.items():
            if word in values:
                expanded.extend(values)

    return list(set(expanded))


def search_tests(query, catalog, top_n=5):

    query_words = clean_query(query)

    query_lower = query.lower()

    wants_remote = "remote" in query_lower

    wants_adaptive = "adaptive" in query_lower

    results = []

    for item in catalog:

        score = 0

        name = item.get("name", "").lower()
        description = item.get("description", "").lower()
        keys = " ".join(item.get("keys", [])).lower()
        levels = " ".join(item.get("job_levels", [])).lower()

        searchable = f"{name} {description} {keys} {levels}"

                # ----------------------------------
        # Strong boost for exact technology
        # ----------------------------------
        for tech, aliases in TECH_BOOST.items():

            if tech in query_lower:

                if any(alias in name for alias in aliases):
                    score += 40

                elif any(alias in description for alias in aliases):
                    score += 20

        # -----------------------------
        # Weighted keyword scoring
        # -----------------------------
        for word in query_words:

    # Exact name match
          if word == name:
           score += 20

    # Word appears in assessment name
          elif word in name:
           score += 12

    # Job level
          elif word in levels:
            score += 8

    # Assessment category
          elif word in keys:
            score += 6

    # Description
          elif word in description:
            score += 4
        # Mid-professional preference
        if "mid" in query_lower and "mid-professional" in levels:
            score += 10

        # Entry-level preference
        if "entry" in query_lower and "entry-level" in levels:
            score += 10
        # -----------------------------
        # Remote preference
        # -----------------------------
        if wants_remote:

            if item.get("remote", "").lower() == "yes":
                score += 8
            else:
                continue

        # -----------------------------
        # Adaptive preference
        # -----------------------------
        if wants_adaptive:

            if item.get("adaptive", "").lower() == "yes":
                score += 5

        # -----------------------------
        # Exact phrase bonus
        # -----------------------------
        if query_lower in searchable:
            score += 15

        # -----------------------------
        # Keep only relevant
        # -----------------------------
        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)

    recommendations = []

    for score, item in results[:top_n]:

        recommendations.append(item)

    return recommendations