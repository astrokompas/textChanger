import re
import requests
from docx import Document
import spacy

def fetch_wikipedia_summary(city, lang='pl'):
    """Fetch the first few sentences from Wikipedia for a given city in a specified language."""
    base_url = "https://pl.wikipedia.org/w/api.php"
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
    page = next(iter(data['query']['pages'].values()))
    return page.get('extract', 'No summary available.')

def replace_city_and_description_polish(original_text, original_city, new_city, original_inflections, new_inflections):
    """Replace the original city and its Wikipedia description with a new city and its Wikipedia description, using manual inflections."""
    # Fetch the Wikipedia descriptions for both cities
    original_city_desc = fetch_wikipedia_summary(original_city, lang='pl')
    new_city_desc = fetch_wikipedia_summary(new_city, lang='pl')
    
    print(f"Original City Description for {original_city}: {original_city_desc[:150]}...")  # Debugging line to check description
    print(f"New City Description for {new_city}: {new_city_desc[:150]}...")  # Debugging line to check description

    # Replace all specified inflections of the original city's name with the corresponding new city's name inflections
    updated_text = original_text
    for old_inflection, new_inflection in zip(original_inflections, new_inflections):
        updated_text = re.sub(r'\b' + re.escape(old_inflection) + r'\b', new_inflection, updated_text, flags=re.IGNORECASE)
    
    # Ensure the original description is replaced with the new city's description
    updated_text = updated_text.replace(original_city_desc, new_city_desc)
    
    return updated_text

def save_text_to_word(text, filename):
    """Save the given text to a Word document."""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def generate_and_save_documents(original_text, city_pairs):
    """Generate documents for different city replacements and save each to a Word file."""
    for original_city, new_city, original_inflections, new_inflections in city_pairs:
        # Replace city and its description
        updated_text = replace_city_and_description_polish(original_text, original_city, new_city, original_inflections, new_inflections)
        
        # Generate a filename
        filename = f'relocation_{new_city}.docx'
        
        # Save to a Word document
        save_text_to_word(updated_text, filename)
        print(f"Saved document for {new_city} as {filename}")

# Example city pairs and inflections
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




original_text = """Relokacje Maszyn Kraków

Relokacje Maszyn w Krakowie

W historycznym mieście Kraków, relokacja ciężkich maszyn stanowi kluczową usługę, niezbędną dla firm przeprowadzających modernizacje, relokacje lub restrukturyzacje. Wybór profesjonalnego zespołu do przenoszenia maszyn zapewnia nie tylko bezpieczeństwo i integralność kosztownego sprzętu, ale także zgodność z rygorystycznymi przepisami branżowymi. Nasza wiedza specjalistyczna w zakresie relokacji maszyn w Krakowie gwarantuje płynne przejście, minimalizując czas przestoju i maksymalizując efektywność operacyjną.

Czym Jest Relokacja Maszyn?

Relokacja maszyn obejmuje strategiczny demontaż, transport i montaż przemysłowych maszyn. Usługa ta jest kluczowa dla sektorów takich jak produkcja, wytwarzanie i budownictwo, gdzie duże i złożone maszyny wymagają przemieszczenia, zarówno w obrębie tego samego obiektu, do nowej lokalizacji w Krakowie, jak i nawet za granicę. Nasze podejście zapewnia, że każda maszyna jest obsługiwana z najwyższą starannością i precyzją, dostosowaną do specyficznych wymagań każdego urządzenia. Współczesnym biznesem rządzi pieniądz i polityka. Zakłady przemysłowe otwierane są w miejscach, gdzie produkcja będzie opłacalna, a lokalne warunki polityczne będą sprzyjały jej rozwojowi. W przypadku zmian jednego z tych elementów często dochodzi do przeniesienia produkcji w inne miejsce. Innym czynnikiem, determinującym przenosiny, jest brak odpowiedniego areału, umożliwiającego rozbudowę zakładu. Procesy gospodarcze wymuszają niejako konieczność rozwoju, dlatego też jest to tak ważny element w funkcjonowaniu każdego przedsiębiorstwa.

O Krakowie

Kraków, dawna stolica Polski, jest drugim co do wielkości i jednym z najstarszych miast w kraju. Położony nad rzeką Wisłą, Kraków jest ważnym ośrodkiem kulturalnym, edukacyjnym i gospodarczym. Miasto jest znane z zachowania swojego bogatego dziedzictwa kulturowego, które obejmuje wiele zabytków architektury od średniowiecza po nowoczesność. Kraków jest również znaczącym centrum gospodarczym, w którym rozwinął się przemysł technologiczny, farmaceutyczny oraz usługowy. Uniwersytet Jagielloński, założony w 1364 roku, jest jednym z najstarszych na świecie i stanowi główny ośrodek naukowy w Polsce. Miasto słynie również z licznych muzeów i teatrów, przyciągając turystów z całego świata.


Dlaczego Warto Wybrać Profesjonalne Usługi Relokacyjne?

Przemieszczanie maszyn w Krakowie jest pełne złożoności i ryzyka. Profesjonalne usługi relokacyjne minimalizują te ryzyka, zapewniając, że wszystkie aspekty przeprowadzki są zarządzane przez doświadczonych profesjonalistów. Proces ten wymaga precyzyjnego planowania, od oceny wagi i wrażliwości sprzętu po określenie najbezpieczniejszej trasy i metody transportu. Bez profesjonalnej obsługi firmy narażają się na uszkodzenia, które mogą prowadzić do znaczących strat finansowych i czasu przestoju operacyjnego. Nasza firma zapewnia kompleksowe zarządzanie projektem relokacji od początku do końca, włączając w to uzgodnienia z lokalnymi władzami oraz dostosowanie do specyficznych regulacji i wymogów technicznych. Efektywnie, bezpiecznie i bez zbędnego ryzyka - tak wyglądają relokacje maszyn z firmą OKSEL. Bez względu na to, czy jest to przenoszenie pojedynczych maszyn, czy przeniesienie całej produkcji, rozumiemy Twoje potrzeby i przemyślenia dotyczące relokacji maszyn. Relokacje przemysłowe, przemieszczanie maszyn to skomplikowane procesy, które zawierają wiele szczegółów. Potrzebujesz profesjonalnego partnera, który wie, jak poprowadzić to od A do Z. My to wiemy, my to rozumiemy, dlatego jesteśmy "specjalistami relokacji maszyn". Firma OKSEL realizuje przeprowadzki maszyn nie tylko w Polsce, ale na całym świecie.

Nasze Usługi w Krakowie

Pomagamy w relokacji zarówno poszczególnych maszyn, jak i całych linii produkcyjnych. Wykonujemy kompleksowe działania w tym zakresie, począwszy od działań planistycznych, przez demontaż maszyn lub też linii produkcyjnych. Na swoje barki bierzemy również transport jak i montaż urządzeń lub też linii produkcyjnych w miejscach docelowych. Każda wykonywana przez nas relokacja maszyn jest efektywna - optymalizujemy wszelkie środki i siły tak, by nasza oferta była konkurencyjna, przy równoczesnym zachowaniu wysokiego poziomu bezpieczeństwa.

Nasze kompleksowe usługi relokacji maszyn w Krakowie obejmują:

- Demontaż: Wykwalifikowani technicy starannie demontują maszyny, klasyfikując i bezpiecznie pakując każdy komponent.
- Transport: Wykorzystujemy flotę specjalistycznych pojazdów transportowych zaprojektowanych do bezpiecznego przewożenia ciężkich ładunków przez różnorodne tereny. Niezależnie od tego, czy relokacja odbywa się w Krakowie, czy do innego regionu, nasze doświadczenie logistyczne zapewnia terminową i bezpieczną dostawę.
- Montaż: Po przybyciu do nowej lokalizacji nasz zespół starannie montuje maszyny, zapewniając ich właściwe ustawienie i kalibrację zgodnie z specyfikacjami producenta. Pomagamy również przy uruchomieniu maszyn i linii produkcyjnych. Każda wykonywana przez nas relokacja maszyn jest efektywna - optymalizujemy wszelkie środki i siły tak, by nasza oferta była konkurencyjna, przy równoczesnym zachowaniu wysokiego poziomu bezpieczeństwa.

Jako profesjonaliści zdajemy sobie sprawę, iż tak skomplikowany proces, jakim jest przeniesienie maszyn, wymaga dokładności i precyzji. Przy każdej relokacji linii produkcyjnych lub maszyn wykorzystujemy swoje bogate doświadczenie, dzięki czemu uzyskujemy wysoką skuteczność i zadowolenie każdego klienta.

Korzyści z Wyboru Naszego Zespołu w Krakowie

Nasza firma zajmuje się relokacjami maszyn przemysłowych od wielu lat. Jako specjaliści w tym zakresie posiadamy wieloletnie doświadczenie, które owocuje powodzeniem każdej przeprowadzki maszyn przemysłowych. Nasz zespół specjalistów posiada odpowiednie kwalifikacje do przemieszczania nawet najbardziej skomplikowanych maszyn i relokacji linii produkcyjnych.

Wybór naszego zespołu w Krakowie do potrzeb relokacji maszyn przynosi liczne korzyści:

- Wiedza specjalistyczna: Nasz zespół składa się z weteranów branży z wieloletnim doświadczeniem w obsłudze złożonych relokacji maszyn.
- Sprawdzone doświadczenie: Pomyślnie przeprowadziliśmy relokację maszyn dla wielu znanych firm w Krakowie i poza nimi, posiadamy studia przypadków i referencje klientów potwierdzające nasze możliwości.
- Rozwiązania na miarę: Każda relokacja jest unikalna, a nasze usługi są dostosowywane do konkretnych potrzeb i ograniczeń Twojej operacji. Pomagamy w relokacji zarówno poszczególnych maszyn, jak i całych linii produkcyjnych.

Współpracujemy z najlepszymi robotykami, automatykami, gazownikami jak i elektrykami oraz hydraulikami w Polsce. Są to osoby z odpowiednimi uprawnieniami z zakresu swojej działalności. Gwarantujemy Państwu satysfakcję i pełne bezpieczeństwo podczas i po wykonaniu prac relokacyjnych.

Bezpieczeństwo i Zgodność

Bezpieczeństwo jest naszym najwyższym priorytetem. Przestrzegamy wszystkich lokalnych i międzynarodowych norm bezpieczeństwa, zapewniając, że każda faza procesu relokacji jest zgodna z przepisami branżowymi. Nasza polisa na 2 miliony euro zapewnia spokój ducha, chroniąc Twoje aktywa przed nieprzewidzianymi incydentami.

Kontakt i Konsultacje

Aby uzyskać więcej informacji lub umówić się na konsultację, zapraszamy do kontaktu. Nasz zespół jest gotowy, aby zapewnić Ci spersonalizowany plan usług, który spełni Twoje konkretne wymagania, pomagając osiągnąć płynną i efektywną relokację maszyn.

Posiadamy bogate doświadczenie w relokacji maszyn przemysłowych, o czym świadczą nasze referencje. 

Zapraszamy również do zapoznania się z tym, jakie realizacje udało nam się skutecznie wykonać.

Jeśli interesują Cię tematy związane z branżą relokacji maszyn, zerknij na naszego bloga."""


generate_and_save_documents(original_text, city_pairs)