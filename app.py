import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Legia Warszawa — Ekstraklasa 2025/26",
    page_icon="⚽",
    layout="wide",
)

IMAGES_DIR = Path("images")

st.title("Legia Warszawa — Ekstraklasa 2025/26")
st.divider()

PLOTS = [
    {
        "file": "scatter2.png",
        "title": "Obraz drużyny na tle ligi",
        "text": (
            "Legia wykazała się <b>najmniejszą</b> liczbą straconych goli w sezonie, "
            "jednak dysproporcja względem xGA (oczekiwane gole stracone) nie jest zbyt wielka. "
            "Ofensywnie jednak zaliczyła <b>underperformence</b> (-5xG względem goals). "
            "Porównując do innych drużyn, jest to <b>poziom 5-8</b>: solidna defensywa, "
            "natomiast liczba strzelonych goli."
        ),
    },
    {
        "file": "pie1.png",
        "title": "Dysproporcja goli",
        "text": (
            "Najmniejsza liczba goli straconych w lidze brzmi dobrze, "
            "jednak zdecydowanym <b>problemem</b> jest ilość straconych goli przy stałych fragmentach. "
            "Więcej goli ze <b>stałych fragmentów</b> traciły tylko zespoły, które zajęły <b>ostatnie 5 miejsc</b>, "
            "co pokazuje, jak często Legia traciła koncentracje broniąc się w swoim polu karnym."
        ),
    },
    {
        "file": "radar2.png",
        "title": "Bramkarze",
        "text": (
            "Porównując obu bramkarzy można stwierdzić, że w drugiej połowie sezonu defensywa była "
            "zdecydowanie skuteczna: Hindrich w ~40% meczach (5/13) zachował czyste konto, "
            "<b>2x więcej</b> niż średnia ligowa czy Kacper Tobiasz. Sam bramkarz przyczynił się do tego: "
            "75% obron to <b>najlepsze 13%</b> bramkarzy ligi. Tobiasz w tym sezonie negatywnie wyróżnił się "
            "w statystyce % obron (5pkt % poniżej średniej). Dodatkowo na jeden mecz miał średnio "
            "<b>1.3 sytuacji</b> sam na sam (Sweeper actions), co pokazuje, jak dziurawa była obrona Legii na jesień."
        ),
    },
    {
        "file": "bar1.png",
        "title": "Bramkarze - gole zapobiegane",
        "text": (
            "Pierwszą połowę sezonu bronił Kacper Tobiasz. Nie był to dla udany okres dla bramki Legii, "
            "do tego ujemny wynik goli zapobieganych to pogarsza. W drugiej połowie nastąpiła zmiana, "
            "w miejsce Tobiasza wskoczył Hindrich. Defensywa Legii wtedy się znacznie poprawiła, "
            "bo dochodziło do mniejszej ilości strzałów, co w połączeniu z <b>+3 goli zapobieganych</b> "
            "dało tak małą ilość goli straconych na tle ligi. Podsumowując: Hindrich zaliczył "
            "overperformence, Tobiasz underperformence."
        ),
    },
    {
        "file": "bar3.png",
        "title": "Dyscyplina w obronie",
        "text": (
            "Zawodnikami, którzy zdecydowanie prowokowali <b>najwięcej</b> fauli, nie wywalczając zbyt wiele, "
            "byli Augustyniak (-22), Szymański (-22) i Kapuadi (-35). Z drugiej strony bardzo dużo "
            "wywalczyli dla drużyny Elitim (+12), Bichakhchyan (+9) czy Vinagre (+14). Porównując do "
            "średniej ligowej, Legia wywalcza <b>zdecydowanie mniej fauli</b> niż reszta zespołów "
            "(dysproporcja wynosi aż +3.4)."
        ),
    },
    {
        "file": "bar4.png",
        "title": "Kary indywidualne, sprokurowane karne",
        "text": (
            "Nie ma tutaj zbyt wielu zaskoczeń jeśli chodzi o żółte kartki. "
            "Zawodnicy o profilu Augustyniaka i D. Szymańskiego mają często <b>za zadanie</b> przerwanie "
            "np. kontry rywala, nawet jeśli grozi to kartką. W aspekcie dyscypliny słabo wypada K. "
            "Piątkowski: może dostał tylko 3 żółte kartki, co jak na stopera to niewiele, jednak "
            "dostał 1 czerwoną i sprokurował jednego karnego. Była to <b>jedyna</b> czerwona kartka Legii; "
            "razem z Górnikiem Zabrze są w tym aspekcie <b>najefektywniejsi</b>."
        ),
    },
    {
        "file": "bar5.png",
        "title": "Odbiory",
        "text": (
            "K. Piątkowski i B. Kapustka znajdują się w <b>czołówce</b> ligi pod względem odbiorów (tackles). "
            "Pozytywnie wygląda to również w przypadku pozostałych \"6\". Z ofensywnych zawodników "
            "wyróżnia się Krasniqi. Jeśli chodzi o przechwycone piłki (np. wbiegnięcie przed rywala "
            "w momencie podania) czołowi zawodnicy defensywni wyglądają <b>zdecydowanie lepiej</b> niż średnia "
            "ligowa, co potwierdza m.in. ilość straconych bramek z gry (tylko 18)."
        ),
    },
    {
        "file": "scatter3.png",
        "title": "Pojedynki Główkowe",
        "text": (
            "W wygranych pojedynkach główkowych należy pochwalić Legię. Średnia klubowa jest o <b>lepsza</b> "
            "i minimalnie skuteczniejsza niż średnia ligowa. <b>Zdecydowanie na plus</b> wyróżniają się "
            "zawodnicy defensywni + M. Rajović, którzy przy sporej ilości sytuacji w powietrzu są w stanie "
            "zachować dużą skuteczność. Słabi w powietrzu są pomocnicy tacy jak Bichakhchyan czy "
            "K. Urbański, którzy są bardziej zawodnikami technicznymi niż fizycznymi."
        ),
    },
    {
        "file": "bar2.png",
        "title": "Odbiory w 3 tercji",
        "text": (
            "Najbardziej aktywnymi piłkarzami w odbiorach w 3 tercji byli Kapustka, Krasniqi "
            "i M. Rajović. Średnia klubowa była niestety <b>niższa o ~15%</b> od ligowej, co pokazuje, "
            "że pressing Legii w 3 tercji nie okazywał się zbytnio skuteczny na tle ligi."
        ),
    },
    {
        "file": "treemap2.png",
        "title": "Kreowanie szans",
        "text": (
            "Najwięcej szans stworzył Jurgen Elitim, pomocny był też Bartek Kapusta. "
            "Jednak bardzo dużym kreatorem szans byli wahadłowi: Wszołek + Vinagre + Kun + Reca "
            "stworzyli łącznie 13 tzw. \"<b>Big chances</b>\" (bardzo dogodne sytuacje), co stanowi <b>34% całości</b>. "
            "Za największe rozczarowanie można uznać chyba V. Bichakhchana, który pomimo wielu "
            "stworzonych szans nie stworzył ani jednej big chances. Podobnie sytuacja wygląda "
            "z Kacprem Chodyną; Od zawodników ofensywnych w środku pola oczekuje się <b>lepszego</b> "
            "kreowania gry."
        ),
    },
    {
        "file": "bar6.png",
        "title": "Długie piłki",
        "text": (
            "Pod względem długich podań (>30m) J. Elitim ma zdecydowanie <b>największą skuteczność</b> "
            "przy dużej ilości takich podań. Kapuadi, Szymański mają co prawda skuteczność na poziomie "
            "średniej ligowej, ale za to nadrabiają ilością. Słabo wygląda to w przypadku <b>Piątkowskiego</b>: "
            "skuteczność na poziomie 33.5% to <b>najgorsze</b> 13% ligi. Drużyna jako całość nie ma złej "
            "skuteczności, ale ~15% mniejsza ilość długich podań nie pomaga w kreowaniu dogodnych sytuacji."
        ),
    },
    {
        "file": "scatter4.png",
        "title": "Skuteczność dryblingu",
        "text": (
            "W przypadku dryblingów, bardzo dobrze wygląda <b>Krasniqi</b>, miał on bardzo wysoką skuteczność "
            "dryblingów, co przy tak wielu dryblingach daje duży wkład dla drużyny (przełożyło się to "
            "potem na stworzenie 3 \"big chances\"). Bardzo słabo wygląda ilość dryblingów <b>Kacpra "
            "Urbańskiego</b>. Zanotowanie tylko 12 udanych dryblingów w całym sezonie to wynik <b>rozczarowujący</b> "
            "jak na tak utalentowanego technicznie zawodnika."
        ),
    },
    {
        "file": "treemap1.png",
        "title": "Atak",
        "text": (
            "W przypadku udziału przy golach najbardziej trzeba wyróżnić <b>Rafała Adamskiego</b>, "
            "który tylko w 13 meczach zanotował 4G + 2A. Z zawodników nie będących snajperami, "
            "dobrze wygląda J. Elitim. Na minus <b>zdecydowanie</b> M. Rajovic, którego pomimo największej "
            "ilości bramek jest uważany za najgorszego ofensywnego zawodnika ze względu na skuteczność "
            "(o tym poniżej)."
        ),
    },
    {
        "file": "dumbbell1.png",
        "title": "Gole a xG",
        "text": (
            "Zdecydowanie największy problem to M. Rajovic - przy <b>xG = 12,3</b> strzelił tylko 6 goli "
            "- <b>różnica -6,3</b>: to ogromna <b>anomalia</b>, rzadko obserwuje się takie wartości na zawodowym "
            "poziomie. Do tego dochodzą Bichakhchyan (-1,9) i Kapustka (-1,2), więc niewykorzystywanie "
            "klarownych okazji to ogólny problem drużyny (średnia klubowa -0,3xG). Na plus wybija się "
            "Colak (+1,3), Nsame (+1,2) oraz Adamski (+0,7) - nie mieli zbyt dużego problemu "
            "z wykańczaniem kluczowych akcji, jednak przy tak małej ilości szans taki overperformence "
            "<b>nie robi</b> zbyt dużej różnicy w ofensywie."
        ),
    },
    {
        "file": "scatter1.png",
        "title": "Skuteczność w strzałach celnych",
        "text": (
            "W przypadku strzałów celnych <b>jedynym</b> graczem, który się wyróżnia jest R. Adamski. "
            "Pozostali gracze albo mają wysoką skuteczność przy małej ilości strzałów, albo małą "
            "skuteczność przy dużej ilości. Znowu trzeba zwrócić uwagę na <b>nieskuteczność</b> Rajovicia, "
            "który pomimo oddania aż 30 strzałów celnych (xGOT = 9.2) strzelił <b>tylko</b> 6 goli "
            "(w tym 1 z karnego)."
        ),
    },
]

SUMMARY_TEXT = (
    "<p>Patrząc na całokształt drużyny, widać dużą dysproporcję między statystykami defensywnymi "
    "a ofensywnymi. W obronie Legia była solidną drużyną: najmniejsza liczba goli straconych "
    "(choć przy podobnym xGA), niektórzy zawodnicy byli w topce pod względem odbiorów, obrońcy "
    "w pojedynkach główkowych wykazywali się dużą skutecznością.</p>"
    "<p>Jednak w przypadku ofensywy widać 2 duże problemy:</p>"
    "<ol>"
    "<li><b>Brak kreatorów</b> - wielu zawodników z środka pola nie wykazywało się kreatywnością "
    "w stwarzaniu okazji. Szczególnie w tym aspekcie rozczarował Kacper Urbański. Te braki trochę "
    "nadrabiali wahadłowi, jednak nadal drużyna tworzyła mało sytuacji.</li>"
    "<li><b>Nieskuteczność w wykańczaniach akcji</b> - tutaj największym problemem była nieskuteczność "
    "Rajovica, co w połączeniu z małą ilością stworzonych sytuacji, przełożyło się na tak ogromny "
    "underperformance w xG (6 mniej goli niż xG).</li>"
    "</ol>"
    "<p>Gdyby podzielić statystyki na okres przed przyjściem i okres po przyjściu M. Papszuna okazałoby "
    "się, że Legia jest jednym z czołowych zespołów w lidze. Jednak sezon trwa od lipca do maja, "
    "więc trzeba uwzględnić też te gorsze mecze.</p>"
)

st.sidebar.markdown("## Spis treści")
for i, plot in enumerate(PLOTS):
    st.sidebar.markdown(f"[{plot['title']}](#{i})")
st.sidebar.markdown("[Podsumowanie](#podsumowanie)")

st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
section[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
    background-color: #ffffff !important;
    border-right: 2px solid #e0e0e0 !important;
}

.stApp, .stApp * {
    color: #1a1a1a !important;
}

.plot-description {
    font-size: 1.6rem;
    line-height: 1.8;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.plot-description p,
.plot-description li,
.plot-description ol {
    font-size: 1.6rem !important;
    line-height: 1.8 !important;
}
.plot-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

RADAR_FILES = {"radar1.png", "radar2.png"}

for i, plot in enumerate(PLOTS):
    st.markdown(f'<div id="{i}"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="plot-title">{plot["title"]}</div>', unsafe_allow_html=True)
    img_path = IMAGES_DIR / plot["file"]
    if img_path.exists():
        if plot["file"] in RADAR_FILES:
            col1, col2, col3 = st.columns([1, 3, 1])
        else:
            col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            st.image(str(img_path), use_column_width=True)
    else:
        st.warning(f"Brak pliku: {img_path}")
    st.markdown(f'<div class="plot-description">{plot["text"]}</div>', unsafe_allow_html=True)
    st.divider()

st.markdown('<div id="podsumowanie"></div>', unsafe_allow_html=True)
st.markdown('<div class="plot-title">Podsumowanie</div>', unsafe_allow_html=True)
st.markdown(f'<div class="plot-description">{SUMMARY_TEXT}</div>', unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("## Odnośniki")
st.sidebar.caption('Dane: <a href="https://www.fotmob.com/en-GB" target="_blank">FotMob</a> | Sezon 2025/26', unsafe_allow_html=True)
st.sidebar.caption('<a href="https://github.com/AdamStajer07/ekstraklasa_fotmob" target="_blank">Kod źródłowy na GitHub</a>', unsafe_allow_html=True)
