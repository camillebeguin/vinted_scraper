def clean_text_scraped_dict(t):
    t = " ".join(t.split()).replace(" Suivre", "")
    return t
