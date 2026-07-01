import json

def load_catalog(file_path="data/catalog.json"): # Path fix kar diya
    with open(file_path, "r", encoding="utf-8") as f: # encoding added
        return json.load(f)

def search_tests(query, catalog, top_n=5):
    query_lower = query.lower()
    query_words = query_lower.split()
    results = []
    
    # Check if user is asking for remote tests
    is_remote_requested = "remote" in query_lower

    for item in catalog:
        # 1. Base Score (Keyword Matching)
        score = 0
        text_to_search = (item['name'] + " " + item['description'] + " " + " ".join(item['keys'])).lower()
        
        for word in query_words:
            if word in text_to_search:
                score += 1
        
        # 2. Remote filter logic (Agar user ne 'remote' manga hai)
        if is_remote_requested and item.get('remote') != 'yes':
            continue # Skip non-remote if user specifically wants remote

        if score > 0:
            results.append((item, score))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results[:top_n]]