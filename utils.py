def is_non_academic(affiliation: str) -> bool:
    academic_keywords = [
        "university", "institute", "college", "school", "department",
        "faculty", "academy", "hospital", "center", "centre", "lab"
    ]
    return not any(word.lower() in affiliation.lower() for word in academic_keywords)