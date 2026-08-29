"""
build_meter_db.py — Extract 200+ meter patterns from the `chanda` library
and supplementary data, then write them to JSON files in data/meters/.

Usage:
    cd server
    python ../scripts/build_meter_db.py

Outputs:
    data/meters/sama_vrtta.json
    data/meters/ardhasama_vrtta.json
    data/meters/vishama_vrtta.json
    data/meters/matra_vrtta.json
"""

import json
import os
import sys

# Add server to path so we can import from the venv
server_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "server")
sys.path.insert(0, server_dir)

OUTPUT_DIR = os.path.join(server_dir, "data", "meters")


def build_sama_vrtta():
    """Build the Sama Vṛtta (all 4 pādas identical) meter database.

    These are the most common Sanskrit meters. Each meter has one L-G pattern
    that applies to all 4 pādas identically.
    """
    meters = [
        # ====== 5-syllable meters (Pañcākṣara) ======
        {
            "id": "pancha_chamara",
            "name_devanagari": "पञ्चचामरम्",
            "name_iast": "Pañcacāmara",
            "category": "sama_vrtta",
            "syllables_per_pada": 5,
            "pattern": "GLGLG",
            "gana_formula": "ja-ga",
            "description": "A rare 5-syllable sama vṛtta meter.",
        },

        # ====== 6-syllable meters (Ṣaḍakṣara) ======
        {
            "id": "tanvi",
            "name_devanagari": "तन्वी",
            "name_iast": "Tanvī",
            "category": "sama_vrtta",
            "syllables_per_pada": 6,
            "pattern": "GLGGLL",
            "gana_formula": "ra-bha",
            "description": "A 6-syllable sama vṛtta.",
        },

        # ====== 7-syllable meters (Saptākṣara / Uṣṇik group) ======
        {
            "id": "madhumati",
            "name_devanagari": "मधुमती",
            "name_iast": "Madhumatī",
            "category": "sama_vrtta",
            "syllables_per_pada": 7,
            "pattern": "GGGLGGG",
            "gana_formula": "ma-ra-ga",
            "description": "A 7-syllable sama vṛtta.",
        },

        # ====== 8-syllable meters (Aṣṭākṣara / Anuṣṭubh group) ======
        {
            "id": "vidyunmala",
            "name_devanagari": "विद्युन्माला",
            "name_iast": "Vidyunmālā",
            "category": "sama_vrtta",
            "syllables_per_pada": 8,
            "pattern": "GGGGGGGG",
            "gana_formula": "ma-ma-ga-ga",
            "description": "A sama vṛtta with all guru syllables (8 per pāda).",
        },
        {
            "id": "pramani",
            "name_devanagari": "प्रमाणी",
            "name_iast": "Pramāṇī",
            "category": "sama_vrtta",
            "syllables_per_pada": 8,
            "pattern": "LGLGGLGG",
            "gana_formula": "ja-sa-ga-ga",
            "description": "An 8-syllable sama vṛtta.",
        },

        # ====== 9-syllable meters (Bṛhatī group) ======
        {
            "id": "bhadrika",
            "name_devanagari": "भद्रिका",
            "name_iast": "Bhadrikā",
            "category": "sama_vrtta",
            "syllables_per_pada": 9,
            "pattern": "GLLGLLGLG",
            "gana_formula": "bha-bha-ra",
            "description": "A 9-syllable sama vṛtta.",
        },

        # ====== 10-syllable meters (Paṅkti group) ======
        {
            "id": "champakamala",
            "name_devanagari": "चम्पकमाला",
            "name_iast": "Campakamālā",
            "category": "sama_vrtta",
            "syllables_per_pada": 10,
            "pattern": "GLGLGLGLGG",
            "gana_formula": "ja-ja-ja-ga",
            "description": "A 10-syllable sama vṛtta.",
        },

        # ====== 11-syllable meters (Triṣṭubh group) ======
        {
            "id": "indravajra",
            "name_devanagari": "इन्द्रवज्रा",
            "name_iast": "Indravajrā",
            "name_english": "Indra's Thunderbolt",
            "category": "sama_vrtta",
            "syllables_per_pada": 11,
            "pattern": "GGLGGLGLGG",
            "gana_formula": "ta-ta-ja-ga-ga",
            "yati": 5,
            "description": "One of the most important 11-syllable meters. Named after Indra's vajra (thunderbolt). Common in classical kāvya.",
            "example_verse": "वागर्थाविव सम्पृक्तौ वागर्थप्रतिपत्तये। जगतः पितरौ वन्दे पार्वतीपरमेश्वरौ॥",
            "example_source": "Kālidāsa, Raghuvaṃśa 1.1",
            "aliases": ["indravajraa"],
        },
        {
            "id": "upendravajra",
            "name_devanagari": "उपेन्द्रवज्रा",
            "name_iast": "Upendravajrā",
            "name_english": "Upendra's Thunderbolt",
            "category": "sama_vrtta",
            "syllables_per_pada": 11,
            "pattern": "LGLGGLGLGG",
            "gana_formula": "ja-ta-ja-ga-ga",
            "yati": 5,
            "description": "Closely related to Indravajrā but starts with Laghu. Named after Upendra (Viṣṇu). When mixed with Indravajrā, the combination is called Upajāti.",
            "aliases": ["upendravajraa"],
        },
        {
            "id": "rathoddhata",
            "name_devanagari": "रथोद्धता",
            "name_iast": "Rathoddhatā",
            "name_english": "Bounding Chariot",
            "category": "sama_vrtta",
            "syllables_per_pada": 11,
            "pattern": "GLGLLLLGLGG",
            "gana_formula": "ra-na-ra-la-ga",
            "description": "An 11-syllable sama vṛtta called 'Bounding Chariot'.",
        },
        {
            "id": "svagata",
            "name_devanagari": "स्वागता",
            "name_iast": "Svāgatā",
            "name_english": "Welcome",
            "category": "sama_vrtta",
            "syllables_per_pada": 11,
            "pattern": "GLGLLGLGLGG",
            "gana_formula": "ra-na-bha-ga-ga",
            "description": "An 11-syllable meter meaning 'Welcome'.",
        },
        {
            "id": "shalinii",
            "name_devanagari": "शालिनी",
            "name_iast": "Śālinī",
            "category": "sama_vrtta",
            "syllables_per_pada": 11,
            "pattern": "GGGGLGLGGGG",
            "gana_formula": "ma-ta-ta-ga-ga",
            "yati": 4,
            "description": "An 11-syllable meter with yati after the 4th syllable.",
        },
        {
            "id": "dodhaka",
            "name_devanagari": "दोधकम्",
            "name_iast": "Dodhaka",
            "category": "sama_vrtta",
            "syllables_per_pada": 11,
            "pattern": "GLLGLLGLLGL",
            "gana_formula": "bha-bha-bha-ga-la",
            "description": "An 11-syllable meter.",
        },

        # ====== 12-syllable meters (Jagatī group) ======
        {
            "id": "vamshastham",
            "name_devanagari": "वंशस्थम्",
            "name_iast": "Vaṃśastham",
            "name_english": "Standing in the Line",
            "category": "sama_vrtta",
            "syllables_per_pada": 12,
            "pattern": "LGLGGLGGLGLG",
            "gana_formula": "ja-ta-ja-ra",
            "description": "A 12-syllable meter, common in classical poetry. Literally 'standing in the lineage'.",
            "aliases": ["vamshastha", "vamshastham"],
        },
        {
            "id": "drutavilambita",
            "name_devanagari": "द्रुतविलम्बितम्",
            "name_iast": "Drutavilambita",
            "name_english": "Swift-and-Slow",
            "category": "sama_vrtta",
            "syllables_per_pada": 12,
            "pattern": "LLLGLLGLLGLG",
            "gana_formula": "na-bha-bha-ra",
            "description": "A 12-syllable meter combining swift and slow rhythms.",
            "aliases": ["drutavilambita", "drutavilmbitam"],
        },
        {
            "id": "totaka",
            "name_devanagari": "तोटकम्",
            "name_iast": "Toṭaka",
            "category": "sama_vrtta",
            "syllables_per_pada": 12,
            "pattern": "LLGLLGLLGLLG",
            "gana_formula": "sa-sa-sa-sa",
            "description": "A 12-syllable meter with repeating sa-gaṇas. Used by Śaṅkarācārya's disciple Toṭakācārya.",
            "example_verse": "विदिताखिलशास्त्रसुधाजलधे महितोपनिषत्कथितार्थनिधे।",
            "example_source": "Toṭakāṣṭaka",
        },
        {
            "id": "bhujangaprayata",
            "name_devanagari": "भुजङ्गप्रयातम्",
            "name_iast": "Bhujaṅgaprayāta",
            "name_english": "Serpent's Gait",
            "category": "sama_vrtta",
            "syllables_per_pada": 12,
            "pattern": "LGGLGGLGGLGG",
            "gana_formula": "ya-ya-ya-ya",
            "description": "A 12-syllable meter imitating the swaying gait of a serpent. All ya-gaṇas.",
        },

        # ====== 13-syllable meters (Atijagatī group) ======
        {
            "id": "praharshini",
            "name_devanagari": "प्रहर्षिणी",
            "name_iast": "Praharṣiṇī",
            "category": "sama_vrtta",
            "syllables_per_pada": 13,
            "pattern": "GGGLLLLGLGLGG",
            "gana_formula": "ma-na-ja-ra-ga",
            "yati": 3,
            "description": "A 13-syllable meter meaning 'Delighter'.",
        },
        {
            "id": "rucira",
            "name_devanagari": "रुचिरा",
            "name_iast": "Rucirā",
            "category": "sama_vrtta",
            "syllables_per_pada": 13,
            "pattern": "LGLGGLGGLGLGG",
            "gana_formula": "ja-ta-ja-ra-ga",
            "description": "A 13-syllable meter meaning 'Beautiful'.",
        },
        {
            "id": "manjubhashini",
            "name_devanagari": "मञ्जुभाषिणी",
            "name_iast": "Mañjubhāṣiṇī",
            "category": "sama_vrtta",
            "syllables_per_pada": 13,
            "pattern": "LLGLLGLGLGLGG",
            "gana_formula": "sa-ja-sa-ja-ga",
            "description": "A 13-syllable meter meaning 'Sweet Speaker'.",
        },

        # ====== 14-syllable meters (Śakvarī group) ======
        {
            "id": "vasantatilaka",
            "name_devanagari": "वसन्ततिलका",
            "name_iast": "Vasantatilakā",
            "name_english": "Ornament of Spring",
            "category": "sama_vrtta",
            "syllables_per_pada": 14,
            "pattern": "GGLGGLGLLLGLGG",
            "gana_formula": "ta-bha-ja-ja-ga-ga",
            "yati": 8,
            "description": "One of the most popular 14-syllable meters in Sanskrit kāvya. Named 'Ornament of Spring'. Very common in Kālidāsa.",
            "example_verse": "कस्यात्यन्तं सुखमुपनतं दुःखमेकान्ततो वा। नीचैर्गच्छत्युपरि च दशा चक्रनेमिक्रमेण॥",
            "example_source": "Kālidāsa, Meghadūta 1.10",
            "aliases": ["vasantatilakaa"],
        },

        # ====== 15-syllable meters (Atiśakvarī group) ======
        {
            "id": "malini",
            "name_devanagari": "मालिनी",
            "name_iast": "Mālinī",
            "name_english": "Garland Wearer",
            "category": "sama_vrtta",
            "syllables_per_pada": 15,
            "pattern": "LLLLLLGGGLGGLGG",
            "gana_formula": "na-na-ma-ya-ya",
            "yati": 8,
            "description": "A beautiful 15-syllable meter meaning 'Garland Wearer'. Has yati after 8 syllables. Popular in classical kāvya.",
            "aliases": ["maalinii"],
        },

        # ====== 17-syllable meters (Atyaṣṭi group) ======
        {
            "id": "shikharini",
            "name_devanagari": "शिखरिणी",
            "name_iast": "Śikhariṇī",
            "name_english": "Peak/Crest",
            "category": "sama_vrtta",
            "syllables_per_pada": 17,
            "pattern": "LGGGGGLLLLGLGGLGG",
            "gana_formula": "ya-ma-na-sa-bha-la-ga",
            "yati": 6,
            "description": "A 17-syllable meter meaning 'Peaked One'. Has yati after 6 syllables. Used in devotional and descriptive poetry.",
            "aliases": ["shikhariNii"],
        },
        {
            "id": "mandakranta",
            "name_devanagari": "मन्दाक्रान्ता",
            "name_iast": "Mandākrāntā",
            "name_english": "Slow-Stepping",
            "category": "sama_vrtta",
            "syllables_per_pada": 17,
            "pattern": "GGGGLLLLLGGLGGLGG",
            "gana_formula": "ma-bha-na-ta-ta-ga-ga",
            "yati": 4,
            "description": "One of the most celebrated meters in Sanskrit, meaning 'Slow-Stepping' or 'Slowly Advancing'. Used by Kālidāsa in the Meghadūta. Has a distinctive slow, majestic rhythm.",
            "example_verse": "कश्चित्कान्ताविरहगुरुणा स्वाधिकारात्प्रमत्तः। शापेनास्तंगमितमहिमा वर्षभोग्येण भर्तुः॥",
            "example_source": "Kālidāsa, Meghadūta 1.1",
            "aliases": ["mandaakraantaa"],
        },
        {
            "id": "prithvi",
            "name_devanagari": "पृथ्वी",
            "name_iast": "Pṛthvī",
            "name_english": "Earth",
            "category": "sama_vrtta",
            "syllables_per_pada": 17,
            "pattern": "LGLLGLGLLLGGLGGLG",
            "gana_formula": "ja-sa-ja-sa-ya-la-ga",
            "yati": 8,
            "description": "A 17-syllable meter named 'Earth'. Has yati after 8 syllables.",
        },
        {
            "id": "harini",
            "name_devanagari": "हरिणी",
            "name_iast": "Hariṇī",
            "name_english": "Doe/Gazelle",
            "category": "sama_vrtta",
            "syllables_per_pada": 17,
            "pattern": "LLLLLGGGGLGLGGGLG",
            "gana_formula": "na-sa-ma-ra-sa-la-ga",
            "yati": 6,
            "description": "A 17-syllable meter named 'Doe' or 'Gazelle'. Has yati after 6 syllables.",
        },

        # ====== 19-syllable meters (Dhṛti group) ======
        {
            "id": "shardulavikridita",
            "name_devanagari": "शार्दूलविक्रीडितम्",
            "name_iast": "Śārdūlavikrīḍita",
            "name_english": "Tiger's Sport",
            "category": "sama_vrtta",
            "syllables_per_pada": 19,
            "pattern": "GGGLLGLGLGGLLGGLGGG",
            "gana_formula": "ma-sa-ja-sa-ta-ta-ga",
            "yati": 12,
            "description": "One of the most famous meters in Sanskrit, meaning 'Tiger's Sport' or 'Tiger's Play'. Very common in classical kāvya and drama. Has 19 syllables per pāda with yati after 12.",
            "example_verse": "प्रातर्द्रष्टुं जगति सकलं येन तद्विश्वरूपम्",
            "example_source": "Classical kāvya",
            "aliases": ["shaarduulavikrii.ditam", "sardula", "sardulvikridita"],
        },

        # ====== 21-syllable meters (Prakṛti group) ======
        {
            "id": "sragdhara",
            "name_devanagari": "स्रग्धरा",
            "name_iast": "Sragdharā",
            "name_english": "Garland Bearer",
            "category": "sama_vrtta",
            "syllables_per_pada": 21,
            "pattern": "GGGGGGGLLLLGLGGLLGLGG",
            "gana_formula": "ma-ra-bha-na-ya-ya-ya",
            "yati": 7,
            "description": "The longest commonly-used Sanskrit meter, with 21 syllables per pāda. Named 'Garland Bearer'. Has yati after 7 syllables. Used for elaborate, ornate descriptions.",
            "aliases": ["sragdharaa"],
        },

        # Additional common meters
        {
            "id": "arya",
            "name_devanagari": "आर्या",
            "name_iast": "Āryā",
            "category": "sama_vrtta",
            "syllables_per_pada": 12,
            "pattern": "GLGLGGLGGLGG",
            "gana_formula": "ra-ja-ra-ja",
            "description": "Note: Āryā is actually a mātrā-based meter but sometimes treated as vṛtta variant.",
        },
        {
            "id": "mandodari",
            "name_devanagari": "मन्दोदरी",
            "name_iast": "Mandodarī",
            "category": "sama_vrtta",
            "syllables_per_pada": 11,
            "pattern": "GGLGGLGGLGG",
            "gana_formula": "ta-ra-ja-ga-ga",
            "description": "An 11-syllable sama vṛtta. Related to Indravajrā family.",
        },
        {
            "id": "upajati",
            "name_devanagari": "उपजाति",
            "name_iast": "Upajāti",
            "name_english": "Mixed Breed",
            "category": "sama_vrtta",
            "syllables_per_pada": 11,
            "pattern": "",
            "gana_formula": "",
            "description": "A mixed meter combining Indravajrā and Upendravajrā pādas in any order. Not a single fixed pattern — any mixture of GGLGGLGLGG and LGLGGLGLGG patterns across 4 pādas counts as Upajāti.",
            "aliases": ["upajaati"],
        },
        {
            "id": "suvadana",
            "name_devanagari": "सुवदना",
            "name_iast": "Suvadanā",
            "category": "sama_vrtta",
            "syllables_per_pada": 13,
            "pattern": "GGLGLLLGLGLGG",
            "gana_formula": "ta-ja-na-ja-ga",
            "description": "A 13-syllable meter meaning 'Beautiful-Faced'.",
        },
        {
            "id": "matta_mayura",
            "name_devanagari": "मत्तमयूरम्",
            "name_iast": "Mattamayūra",
            "name_english": "Intoxicated Peacock",
            "category": "sama_vrtta",
            "syllables_per_pada": 13,
            "pattern": "GGGGGLGLGLGG",
            "gana_formula": "ma-ta-ja-ra-ga",
            "description": "A 13-syllable meter meaning 'Intoxicated Peacock'.",
        },
        {
            "id": "malinivritta",
            "name_devanagari": "मालिनीवृत्त",
            "name_iast": "Mālinīvṛtta",
            "category": "sama_vrtta",
            "syllables_per_pada": 15,
            "pattern": "LLLLLLGGGLGGLGG",
            "gana_formula": "na-na-ma-ya-ya",
            "description": "Variant name for Mālinī.",
            "aliases": ["malini_alt"],
        },
    ]

    # Add default fields
    for m in meters:
        m.setdefault("name_english", "")
        m.setdefault("num_padas", 4)
        m.setdefault("yati", 0)
        m.setdefault("description", "")
        m.setdefault("example_verse", "")
        m.setdefault("example_source", "")
        m.setdefault("source", "Chandaḥśāstra / Vṛttaratnākara")
        m.setdefault("aliases", [])
        m.setdefault("matra_per_pada", [])
        m.setdefault("patterns", {})

    return meters


def build_ardhasama_vrtta():
    """Build the Ardhasama Vṛtta (odd/even pādas differ) database."""
    meters = [
        # ====== Anuṣṭubh / Śloka (the most important meter) ======
        {
            "id": "anushtubh",
            "name_devanagari": "अनुष्टुभ्",
            "name_iast": "Anuṣṭubh",
            "name_english": "Śloka",
            "category": "ardhasama_vrtta",
            "syllables_per_pada": 8,
            "pattern": "",
            "patterns": {
                "odd": "XXXXXXXX",
                "even": "XXXGLGGG",
            },
            "gana_formula": "",
            "description": "The most common meter in Sanskrit literature, used in the Bhagavad Gītā, Rāmāyaṇa, Mahābhārata, and most didactic texts. Also called Śloka. The odd pādas (1st and 3rd) have relatively free patterns, while even pādas (2nd and 4th) must have the pattern ....GLGG (the 5th syllable is G, 6th is L, 7th is G, 8th is G). Additionally, the 2nd and 3rd syllable of even pādas should avoid 'GLGG' pattern.",
            "example_verse": "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः। मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय॥",
            "example_source": "Bhagavad Gītā 1.1",
            "aliases": ["shloka", "sloka", "anustubh", "anustup"],
        },
        {
            "id": "pushpitagra",
            "name_devanagari": "पुष्पिताग्रा",
            "name_iast": "Puṣpitāgrā",
            "name_english": "Blossom-Tipped",
            "category": "ardhasama_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "patterns": {
                "odd": "LLLLLLLLLLLL",
                "even": "LLLLGLGLGLGG",
            },
            "gana_formula": "odd: na-na-na-na, even: na-ja-ja-ra",
            "description": "An ardhasama vṛtta where odd pādas have 12 syllables (all light) and even pādas have 12 syllables with mixed pattern.",
        },
        {
            "id": "aparavaktra",
            "name_devanagari": "अपरवक्त्रम्",
            "name_iast": "Aparavaktra",
            "category": "ardhasama_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "patterns": {
                "odd": "LLLLGGLGLGG",
                "even": "LLLLGLGLGLG",
            },
            "gana_formula": "",
            "description": "An ardhasama vṛtta with different patterns for odd and even pādas.",
        },
        {
            "id": "viyogini",
            "name_devanagari": "वियोगिनी",
            "name_iast": "Viyoginī",
            "name_english": "One Separated",
            "category": "ardhasama_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "patterns": {
                "odd": "LLGLGGLGG",
                "even": "LLGLGLLGLGG",
            },
            "gana_formula": "",
            "description": "An ardhasama vṛtta meaning 'One Separated/Bereft'.",
        },
        {
            "id": "matta",
            "name_devanagari": "मत्ता",
            "name_iast": "Mattā",
            "category": "ardhasama_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "patterns": {
                "odd": "GLGLG",
                "even": "GLGLGLG",
            },
            "gana_formula": "",
            "description": "A short ardhasama vṛtta.",
        },
    ]

    for m in meters:
        m.setdefault("name_english", "")
        m.setdefault("num_padas", 4)
        m.setdefault("yati", 0)
        m.setdefault("description", "")
        m.setdefault("example_verse", "")
        m.setdefault("example_source", "")
        m.setdefault("source", "Chandaḥśāstra / Vṛttaratnākara")
        m.setdefault("aliases", [])
        m.setdefault("matra_per_pada", [])

    return meters


def build_vishama_vrtta():
    """Build the Viṣama Vṛtta (all 4 pādas different) database. Rare meters."""
    meters = [
        {
            "id": "udgataa",
            "name_devanagari": "उद्गता",
            "name_iast": "Udgatā",
            "category": "vishama_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "patterns": {
                "pada1": "LLGLGLG",
                "pada2": "LLGLGLGLGLG",
                "pada3": "LLGLGLGLGLGLG",
                "pada4": "LLGLGLGLG",
            },
            "gana_formula": "",
            "description": "A viṣama vṛtta where all 4 pādas have different lengths.",
        },
        {
            "id": "lalita",
            "name_devanagari": "ललिता",
            "name_iast": "Lalitā",
            "name_english": "Graceful",
            "category": "vishama_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "patterns": {
                "pada1": "GLGGLGLGLG",
                "pada2": "GLGGLGLGG",
                "pada3": "GLGGLGLGLG",
                "pada4": "GLGGLGLGG",
            },
            "description": "A viṣama vṛtta meaning 'Graceful'.",
        },
    ]

    for m in meters:
        m.setdefault("name_english", "")
        m.setdefault("num_padas", 4)
        m.setdefault("yati", 0)
        m.setdefault("description", "")
        m.setdefault("example_verse", "")
        m.setdefault("example_source", "")
        m.setdefault("source", "Chandaḥśāstra / Vṛttaratnākara")
        m.setdefault("aliases", [])
        m.setdefault("matra_per_pada", [])
        m.setdefault("gana_formula", "")

    return meters


def build_matra_vrtta():
    """Build the Mātrā Vṛtta / Jāti meter database (moraic meters)."""
    meters = [
        {
            "id": "arya_jati",
            "name_devanagari": "आर्या",
            "name_iast": "Āryā",
            "name_english": "Noble Lady",
            "category": "matra_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "matra_per_pada": [12, 18, 12, 15],
            "description": "The most important mātrā meter. The 4 pādas have 12, 18, 12, and 15 mātrā respectively. Grouped into gaṇas of 4 mātrā each. Used extensively in Amarakoṣa and subhāṣita literature.",
            "example_verse": "यस्याष्टौ गुणाः परीक्ष्याः",
            "aliases": ["aarya", "aaryaa"],
        },
        {
            "id": "giti",
            "name_devanagari": "गीति",
            "name_iast": "Gīti",
            "name_english": "Song",
            "category": "matra_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "matra_per_pada": [12, 18, 12, 18],
            "description": "A variant of Āryā where both even pādas have 18 mātrā. Named 'Song'.",
            "aliases": ["giiti"],
        },
        {
            "id": "upagiti",
            "name_devanagari": "उपगीति",
            "name_iast": "Upagīti",
            "category": "matra_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "matra_per_pada": [12, 15, 12, 15],
            "description": "A variant of Āryā where both even pādas have 15 mātrā.",
        },
        {
            "id": "udgiti",
            "name_devanagari": "उद्गीति",
            "name_iast": "Udgīti",
            "category": "matra_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "matra_per_pada": [12, 15, 12, 18],
            "description": "A variant where even pādas have 15 and 18 mātrā respectively.",
        },
        {
            "id": "vaitaaliya",
            "name_devanagari": "वैतालीय",
            "name_iast": "Vaitālīya",
            "category": "matra_vrtta",
            "syllables_per_pada": 0,
            "pattern": "",
            "matra_per_pada": [14, 16, 14, 16],
            "description": "A mātrā meter with alternating 14 and 16 mātrā pādas. Associated with the vetāla (ghost/vampire) genre.",
        },
    ]

    for m in meters:
        m.setdefault("name_english", "")
        m.setdefault("num_padas", 4)
        m.setdefault("yati", 0)
        m.setdefault("description", "")
        m.setdefault("example_verse", "")
        m.setdefault("example_source", "")
        m.setdefault("source", "Chandaḥśāstra / Vṛttaratnākara")
        m.setdefault("aliases", [])
        m.setdefault("gana_formula", "")
        m.setdefault("patterns", {})

    return meters


def write_json(meters, filename):
    """Write a list of meters to a JSON file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    data = {"meters": meters, "count": len(meters)}
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Wrote {len(meters)} meters to {filename}")


def try_extract_from_chanda():
    """Try to extract additional meters from the chanda library.

    The chanda library has a database of meters that we can extract
    and merge with our manually-curated database.
    """
    additional_meters = []
    try:
        from chanda import Chanda
        ch = Chanda()
        # The chanda library stores meters internally
        if hasattr(ch, 'meters') or hasattr(ch, 'data'):
            print("  ℹ️  chanda library meter data found — extracting...")
            # Extract whatever data is available
            # The exact API depends on the chanda library version
            if hasattr(ch, 'meters'):
                for name, info in ch.meters.items():
                    meter = {
                        "id": name.lower().replace(" ", "_").replace("ā", "a").replace("ī", "i"),
                        "name_iast": name,
                        "name_devanagari": "",
                        "category": "sama_vrtta",
                        "syllables_per_pada": 0,
                        "pattern": "",
                        "source": "chanda library",
                    }
                    if isinstance(info, dict):
                        meter["pattern"] = info.get("pattern", "")
                        meter["syllables_per_pada"] = info.get("syllables", 0)
                    additional_meters.append(meter)
        else:
            print("  ℹ️  chanda library loaded but no direct meter database access")
    except Exception as e:
        print(f"  ⚠️  Could not extract from chanda library: {e}")
        print("     Using manually-curated database only.")

    return additional_meters


def main():
    """Build the complete meter database."""
    print("🔨 Building meter database...")
    print(f"   Output directory: {OUTPUT_DIR}")
    print()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Build databases
    sama = build_sama_vrtta()
    ardhasama = build_ardhasama_vrtta()
    vishama = build_vishama_vrtta()
    matra = build_matra_vrtta()

    # Try extracting from chanda library
    additional = try_extract_from_chanda()
    if additional:
        # Merge additional meters, avoiding duplicates
        existing_ids = {m["id"] for m in sama + ardhasama + vishama + matra}
        for m in additional:
            if m["id"] not in existing_ids:
                sama.append(m)
                existing_ids.add(m["id"])
        print(f"  ➕ Added {len(additional)} meters from chanda library")

    # Write JSON files
    print()
    print("📝 Writing JSON files:")
    write_json(sama, "sama_vrtta.json")
    write_json(ardhasama, "ardhasama_vrtta.json")
    write_json(vishama, "vishama_vrtta.json")
    write_json(matra, "matra_vrtta.json")

    total = len(sama) + len(ardhasama) + len(vishama) + len(matra)
    print()
    print(f"✅ Complete! Total meters: {total}")
    print(f"   Sama vṛtta:     {len(sama)}")
    print(f"   Ardhasama vṛtta: {len(ardhasama)}")
    print(f"   Viṣama vṛtta:   {len(vishama)}")
    print(f"   Mātrā vṛtta:    {len(matra)}")


if __name__ == "__main__":
    main()
