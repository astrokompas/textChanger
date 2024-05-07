import re
import requests
from docx import Document
import difflib

def summary(city, lang='pl'):
    base_url = "https://{lang}.wikipedia.org/w/api.php".format(lang=lang)
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        'redirects': 1,
        'titles': city
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    page = next(iter(data['query']['pages'].values()), {})
    return page.get('extract', 'No summary available.')

def find_best_match_and_replace(original_text, original_description, new_description):
    s = difflib.SequenceMatcher(None, original_text, original_description)
    best_ratio = 0.5
    best_match = None

    for block in s.get_matching_blocks():
        if block.size == 0:
            continue
        match_ratio = s.ratio()
        if match_ratio > best_ratio:
            best_ratio = match_ratio
            best_match = block

    if best_match:
        start, end = best_match.a, best_match.a + best_match.size
        if end - start > 100:
            return original_text[:start] + new_description + original_text[end:]
    return original_text


def replace(original_text, original_city, new_city, original_inflections, new_inflections):
    original_city_desc = summary(original_city)
    new_city_desc = summary(new_city)
    
    updated_text = original_text
    for old_inflection, new_inflection in zip(original_inflections, new_inflections):
        pattern = r'\b' + re.escape(old_inflection) + r'\b'
        updated_text = re.sub(pattern, new_inflection, updated_text, flags=re.IGNORECASE)

    updated_text = find_best_match_and_replace(updated_text, original_city_desc, new_city_desc)

    return updated_text

def save_text_to_word(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def generate_and_save_documents(original_text, city_pairs):
    for original_city, new_city, original_inflections, new_inflections in city_pairs:
        updated_text = replace(original_text, original_city, new_city, original_inflections, new_inflections)
        filename = f'relocation_{new_city}.docx'
        save_text_to_word(updated_text, filename)
        print(f"Saved document for {new_city} as {filename}")

city_pairs = [
    ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi", "Łódzki"]),
    ("Kraków", "Warszawa", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Warszawa", "Warszawie", "w Warszawie", "Warszawski"]),
    ("Kraków", "Wrocław", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Wrocław", "Wrocławiu", "w Wrocławiu", "Wrocławski"]),
    ("Kraków", "Poznań", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Poznań", "Poznaniu", "w Poznaniu", "Poznański"]),
    ("Kraków", "Gdańsk", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Gdańska", "Gdańsku", "w Gdańsku", "Gdański"]),
    ("Kraków", "Szczecin", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Szczecin", "Szczecinie", "w Szczecinie", "Szczeciński"]),
    ("Kraków", "Bydgoszcz", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Bydgoszcz", "Bydgoszczy", "w Bydgoszczy", "Bydgoski"]),
    ("Kraków", "Lublin", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Lublin", "Lublinie", "w Lublinie", "Lubelski"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
    # ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi"]),
]


original_text = """"""


generate_and_save_documents(original_text, city_pairs)