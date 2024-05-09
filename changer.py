import re
import requests
from docx import Document

def summary(city, lang='pl'):
    base_url = f"https://{lang}.wikipedia.org/w/api.php"
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

def titleEndpoint(original_text, title, new_description, endpoint_title): #max_chars
    start_index = original_text.find(title)
    if start_index == -1:
        return original_text

    #new_description = new_description[:max_chars]

    end_index = original_text.find(endpoint_title, start_index)
    if end_index == -1:
        end_index = len(original_text)

    start_of_section = start_index + len(title)
    section_to_replace = original_text[start_of_section:end_index].strip()

    return original_text[:start_of_section] + '\n\n' + new_description + '\n\n' + original_text[end_index:]

def replaceInflections(original_text, old_inflections, new_inflections):
    for old, new in zip(old_inflections, new_inflections):
        pattern = r'\b' + re.escape(old) + r'\b'
        original_text = re.sub(pattern, new, original_text, flags=re.IGNORECASE)
    return original_text

def saveToWord(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def pairs(original_text, city_pairs):
    for old_city, new_city, old_inflections, new_inflections, title, endpoint_title in city_pairs:
        new_city_desc = summary(new_city)
        updated_text = titleEndpoint(original_text, title, new_city_desc, endpoint_title) #char limit
        updated_text = replaceInflections(updated_text, old_inflections, new_inflections)
        filename = f"Updated_Description_{new_city}.docx"
        saveToWord(updated_text, filename)
        print(f"Document saved for {new_city} as {filename}")


city_pairs = [
    ("Kraków", "Łódź", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Łódź", "Łodzi", "w Łodźi", "Łódzki"], "O Krakowie", "Nasze Usługi w Krakowie"),
    ("Kraków", "Warszawa", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Warszawa", "Warszawie", "w Warszawie", "Warszawski"], "O Krakowie", "Nasze Usługi w Krakowie"),
    ("Kraków", "Wrocław", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Wrocław", "Wrocławiu", "w Wrocławiu", "Wrocławski"], "O Krakowie", "Nasze Usługi w Krakowie"),
    ("Kraków", "Poznań", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Poznań", "Poznaniu", "w Poznaniu", "Poznański"], "O Krakowie", "Nasze Usługi w Krakowie"),
    ("Kraków", "Gdańsk", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Gdańska", "Gdańsku", "w Gdańsku", "Gdański"], "O Krakowie", "Nasze Usługi w Krakowie"),
    ("Kraków", "Szczecin", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Szczecin", "Szczecinie", "w Szczecinie", "Szczeciński"], "O Krakowie", "Nasze Usługi w Krakowie"),
    ("Kraków", "Bydgoszcz", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Bydgoszcz", "Bydgoszczy", "w Bydgoszczy", "Bydgoski"], "O Krakowie", "Nasze Usługi w Krakowie"),
    ("Kraków", "Lublin", ["Kraków", "Krakowie", "w Krakowie", "Krakowski"], ["Lublin", "Lublinie", "w Lublinie", "Lubelski"], "O Krakowie", "Nasze Usługi w Krakowie"),
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


pairs(original_text, city_pairs)