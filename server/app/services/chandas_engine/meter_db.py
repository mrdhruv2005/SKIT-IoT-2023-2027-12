"""
Meter database loader — loads and indexes the meter JSON database.

Loads the 4 JSON files from data/meters/:
    - sama_vrtta.json     (Sama vṛtta: all 4 pādas identical)
    - ardhasama_vrtta.json (Ardhasama vṛtta: odd/even pādas differ)
    - vishama_vrtta.json   (Viṣama vṛtta: all 4 pādas different)
    - matra_vrtta.json     (Mātrā vṛtta / Jāti: moraic meters)

Provides fast O(1) pattern lookup and search functionality.
"""

import json
import os
from dataclasses import dataclass, field


@dataclass
class Meter:
    """Represents a single Sanskrit meter.

    Attributes:
        id: Unique identifier (e.g., 'anushtubh').
        name_devanagari: Name in Devanagari (e.g., 'अनुष्टुभ्').
        name_iast: Name in IAST (e.g., 'Anuṣṭubh').
        name_english: English name if applicable.
        category: Category (sama_vrtta, ardhasama_vrtta, vishama_vrtta, matra_vrtta).
        syllables_per_pada: Number of syllables per pāda.
        num_padas: Number of pādas (usually 4).
        pattern: L-G pattern for sama vṛtta (single pāda pattern).
        patterns: Per-pāda patterns for ardhasama/viṣama vṛtta.
        gana_formula: Gaṇa notation (e.g., 'ta-ta-ja-ga-ga').
        yati: Yati (caesura) position, if applicable.
        matra_per_pada: Mātrā count per pāda (for jāti meters).
        description: Description of the meter.
        example_verse: Example verse in Devanagari.
        example_source: Source of the example verse.
        source: Source of the meter definition.
        aliases: Alternative names.
    """
    id: str = ""
    name_devanagari: str = ""
    name_iast: str = ""
    name_english: str = ""
    category: str = ""
    syllables_per_pada: int = 0
    num_padas: int = 4
    pattern: str = ""
    patterns: dict = field(default_factory=dict)
    gana_formula: str = ""
    yati: int = 0
    matra_per_pada: list = field(default_factory=list)
    description: str = ""
    example_verse: str = ""
    example_source: str = ""
    source: str = ""
    aliases: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data):
        """Create a Meter from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name_devanagari=data.get("name_devanagari", ""),
            name_iast=data.get("name_iast", ""),
            name_english=data.get("name_english", ""),
            category=data.get("category", ""),
            syllables_per_pada=data.get("syllables_per_pada", 0),
            num_padas=data.get("num_padas", 4),
            pattern=data.get("pattern", ""),
            patterns=data.get("patterns", {}),
            gana_formula=data.get("gana_formula", ""),
            yati=data.get("yati", 0),
            matra_per_pada=data.get("matra_per_pada", []),
            description=data.get("description", ""),
            example_verse=data.get("example_verse", ""),
            example_source=data.get("example_source", ""),
            source=data.get("source", ""),
            aliases=data.get("aliases", []),
        )

    def to_dict(self):
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "name_devanagari": self.name_devanagari,
            "name_iast": self.name_iast,
            "name_english": self.name_english,
            "category": self.category,
            "syllables_per_pada": self.syllables_per_pada,
            "num_padas": self.num_padas,
            "pattern": self.pattern,
            "patterns": self.patterns,
            "gana_formula": self.gana_formula,
            "yati": self.yati,
            "matra_per_pada": self.matra_per_pada,
            "description": self.description,
            "example_verse": self.example_verse,
            "example_source": self.example_source,
            "source": self.source,
            "aliases": self.aliases,
        }


class MeterDatabase:
    """Loads and indexes the meter database for fast lookup.

    Provides:
    - O(1) exact pattern lookup
    - Name-based search (substring)
    - Category filtering
    - ID-based retrieval
    """

    def __init__(self, data_dir=None):
        """Initialize the meter database.

        Args:
            data_dir: Path to the directory containing meter JSON files.
                      If None, uses the default data/meters/ path.
        """
        if data_dir is None:
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                "data", "meters"
            )
        self.data_dir = data_dir
        self._meters = []           # All meters
        self._by_id = {}            # id → Meter
        self._by_pattern = {}       # pattern → [Meter, ...]
        self._by_category = {}      # category → [Meter, ...]
        self._by_syllable_count = {} # syllable_count → [Meter, ...]
        self._loaded = False

    def load(self):
        """Load all meter JSON files and build indexes."""
        if self._loaded:
            return

        json_files = [
            "sama_vrtta.json",
            "ardhasama_vrtta.json",
            "vishama_vrtta.json",
            "matra_vrtta.json",
        ]

        for filename in json_files:
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    meters_data = data.get("meters", [])
                    for m_data in meters_data:
                        meter = Meter.from_dict(m_data)
                        self._meters.append(meter)

        # Build indexes
        for meter in self._meters:
            # By ID
            self._by_id[meter.id] = meter

            # By pattern (sama vṛtta)
            if meter.pattern:
                pattern_key = meter.pattern.upper().replace(" ", "")
                if pattern_key not in self._by_pattern:
                    self._by_pattern[pattern_key] = []
                self._by_pattern[pattern_key].append(meter)

            # By ardhasama/viṣama patterns
            if meter.patterns:
                for pada_key, pada_pattern in meter.patterns.items():
                    if pada_pattern:
                        pk = pada_pattern.upper().replace(" ", "")
                        if pk not in self._by_pattern:
                            self._by_pattern[pk] = []
                        # Avoid duplicates
                        if meter not in self._by_pattern[pk]:
                            self._by_pattern[pk].append(meter)

            # By category
            cat = meter.category
            if cat not in self._by_category:
                self._by_category[cat] = []
            self._by_category[cat].append(meter)

            # By syllable count
            sc = meter.syllables_per_pada
            if sc > 0:
                if sc not in self._by_syllable_count:
                    self._by_syllable_count[sc] = []
                self._by_syllable_count[sc].append(meter)

            # Also index aliases
            for alias in meter.aliases:
                alias_key = alias.lower().replace(" ", "_")
                if alias_key not in self._by_id:
                    self._by_id[alias_key] = meter

        self._loaded = True

    def ensure_loaded(self):
        """Ensure the database is loaded."""
        if not self._loaded:
            self.load()

    def get_all_meters(self):
        """Get all meters in the database.

        Returns:
            List of Meter objects.
        """
        self.ensure_loaded()
        return list(self._meters)

    def get_by_id(self, meter_id):
        """Get a meter by its ID.

        Args:
            meter_id: Meter identifier string.

        Returns:
            Meter object, or None if not found.
        """
        self.ensure_loaded()
        return self._by_id.get(meter_id)

    def get_by_pattern(self, pattern):
        """Get meters matching an exact L-G pattern.

        Args:
            pattern: L-G pattern string (e.g., 'GGLGGLGLGG').

        Returns:
            List of matching Meter objects.
        """
        self.ensure_loaded()
        pattern_key = pattern.upper().replace(" ", "")
        return self._by_pattern.get(pattern_key, [])

    def get_by_category(self, category):
        """Get all meters in a category.

        Args:
            category: Category name (e.g., 'sama_vrtta').

        Returns:
            List of Meter objects in the category.
        """
        self.ensure_loaded()
        return self._by_category.get(category, [])

    def get_by_syllable_count(self, count):
        """Get all meters with a specific syllable count per pāda.

        Args:
            count: Number of syllables per pāda.

        Returns:
            List of Meter objects.
        """
        self.ensure_loaded()
        return self._by_syllable_count.get(count, [])

    def search(self, query):
        """Search meters by name (substring, case-insensitive).

        Searches across: name_iast, name_devanagari, name_english, id, aliases.

        Args:
            query: Search query string.

        Returns:
            List of matching Meter objects.
        """
        self.ensure_loaded()
        if not query:
            return list(self._meters)

        query_lower = query.lower().strip()
        results = []

        for meter in self._meters:
            searchable = [
                meter.id.lower(),
                meter.name_iast.lower(),
                meter.name_devanagari,
                meter.name_english.lower(),
            ] + [a.lower() for a in meter.aliases]

            if any(query_lower in s for s in searchable):
                results.append(meter)

        return results

    def get_meter_count(self):
        """Get total number of meters in the database."""
        self.ensure_loaded()
        return len(self._meters)

    def get_all_patterns(self):
        """Get all unique patterns in the database.

        Returns:
            Dict of pattern → list of meter IDs.
        """
        self.ensure_loaded()
        return {
            pattern: [m.id for m in meters]
            for pattern, meters in self._by_pattern.items()
        }
