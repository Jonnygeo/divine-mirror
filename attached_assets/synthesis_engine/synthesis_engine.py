# Main synthesis engine
def synthesize_meaning(citations, tone="neutral"):
    """
    Input: list of dicts with {verse, tradition, text}
    Output: synthesized spiritual interpretation
    """
    interpretations = []
    for c in citations:
        interpretations.append(f"From {c['tradition']} ({c['verse']}): {c['text']}")
    base_synthesis = "The common thread is: Divinity is found within. Not in buildings, but in being."
    return "\n".join(interpretations) + "\n\n" + base_synthesis
