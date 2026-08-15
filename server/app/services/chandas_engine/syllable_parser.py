"""
Custom Devanagari syllable parser — built from scratch.

Implements Unicode-aware syllable segmentation for Sanskrit text.
Handles: independent vowels, consonants + dependent vowel marks (mātrās),
virāma (halant), nukta, anusvāra, visarga, chandrabindu.
Segments conjunct consonants (ligatures) correctly.

Supports Devanagari input directly, or IAST/HK/SLP1 input via the
transliteration module (normalized to Devanagari before parsing).
"""

from dataclasses import dataclass, field


# ===========================================================================
# Unicode Constants — Devanagari Block (U+0900 – U+097F)
# ===========================================================================

# Independent vowels (स्वर)
INDEPENDENT_VOWELS = {
    "\u0905",  # अ (a)
    "\u0906",  # आ (ā)
    "\u0907",  # इ (i)
    "\u0908",  # ई (ī)
    "\u0909",  # उ (u)
    "\u090A",  # ऊ (ū)
    "\u090B",  # ऋ (ṛ)
    "\u0960",  # ॠ (ṝ)
    "\u090C",  # ऌ (ḷ)
    "\u0961",  # ॡ (ḹ)
    "\u090F",  # ए (e)
    "\u0910",  # ऐ (ai)
    "\u0913",  # ओ (o)
    "\u0914",  # औ (au)
}

# Short independent vowels
SHORT_VOWELS = {
    "\u0905",  # अ (a)
    "\u0907",  # इ (i)
    "\u0909",  # उ (u)
    "\u090B",  # ऋ (ṛ)
    "\u090C",  # ऌ (ḷ)
}

# Long independent vowels
LONG_VOWELS = {
    "\u0906",  # आ (ā)
    "\u0908",  # ई (ī)
    "\u090A",  # ऊ (ū)
    "\u0960",  # ॠ (ṝ)
    "\u0961",  # ॡ (ḹ)
    "\u090F",  # ए (e)
    "\u0910",  # ऐ (ai)
    "\u0913",  # ओ (o)
    "\u0914",  # औ (au)
}

# Dependent vowel signs (mātrā marks)
DEPENDENT_VOWEL_SIGNS = {
    "\u093E",  # ा (ā)
    "\u093F",  # ि (i)
    "\u0940",  # ी (ī)
    "\u0941",  # ु (u)
    "\u0942",  # ू (ū)
    "\u0943",  # ृ (ṛ)
    "\u0944",  # ॄ (ṝ)
    "\u0962",  # ॢ (ḷ)
    "\u0963",  # ॣ (ḹ)
    "\u0947",  # े (e)
    "\u0948",  # ै (ai)
    "\u094B",  # ो (o)
    "\u094C",  # ौ (au)
}

# Short dependent vowel signs
SHORT_DEPENDENT_SIGNS = {
    # No sign = inherent 'a' (short)
    "\u093F",  # ि (i)
    "\u0941",  # ु (u)
    "\u0943",  # ृ (ṛ)
    "\u0962",  # ॢ (ḷ)
}

# Long dependent vowel signs
LONG_DEPENDENT_SIGNS = {
    "\u093E",  # ा (ā)
    "\u0940",  # ी (ī)
    "\u0942",  # ू (ū)
    "\u0944",  # ॄ (ṝ)
    "\u0963",  # ॣ (ḹ)
    "\u0947",  # े (e)
    "\u0948",  # ै (ai)
    "\u094B",  # ो (o)
    "\u094C",  # ौ (au)
}

# Consonants (व्यञ्जन) — U+0915 to U+0939
CONSONANTS = set()
for cp in range(0x0915, 0x093A):  # क to ह
    CONSONANTS.add(chr(cp))

# Additional consonants / nukta forms
CONSONANTS.update({
    "\u0958",  # क़
    "\u0959",  # ख़
    "\u095A",  # ग़
    "\u095B",  # ज़
    "\u095C",  # ड़
    "\u095D",  # ढ़
    "\u095E",  # फ़
    "\u095F",  # य़
})

# Halant / Virāma (suppresses inherent 'a')
HALANT = "\u094D"  # ्

# Nukta (modifies consonants for borrowed sounds)
NUKTA = "\u093C"  # ़

# Anusvāra (nasal)
ANUSVARA = "\u0902"  # ं

# Visarga (aspiration)
VISARGA = "\u0903"  # ः

# Chandrabindu (nasalization)
CHANDRABINDU = "\u0901"  # ँ

# Avagraha (elision marker)
AVAGRAHA = "\u093D"  # ऽ

# Pāda / verse separators
DANDA = "\u0964"  # ।
DOUBLE_DANDA = "\u0965"  # ॥

# All Devanagari characters
ALL_DEVANAGARI = (
    INDEPENDENT_VOWELS | CONSONANTS | DEPENDENT_VOWEL_SIGNS |
    {HALANT, NUKTA, ANUSVARA, VISARGA, CHANDRABINDU, AVAGRAHA, DANDA, DOUBLE_DANDA}
)


# ===========================================================================
# Data Classes
# ===========================================================================

@dataclass
class Syllable:
    """Represents a single Sanskrit syllable (akṣara).

    Attributes:
        text: The raw Devanagari text of this syllable.
        vowel: The vowel nucleus (independent vowel or consonant's vowel).
        is_long_vowel: Whether the vowel is long (dīrgha).
        has_anusvara: Whether the syllable ends with anusvāra.
        has_visarga: Whether the syllable ends with visarga.
        has_chandrabindu: Whether the syllable has chandrabindu.
        consonant_cluster_follows: Whether a consonant cluster follows this syllable.
        is_pada_final: Whether this is the last syllable in a pāda.
        position: Index position in the pāda (0-based).
    """
    text: str = ""
    vowel: str = ""
    is_long_vowel: bool = False
    has_anusvara: bool = False
    has_visarga: bool = False
    has_chandrabindu: bool = False
    consonant_cluster_follows: bool = False
    is_pada_final: bool = False
    position: int = 0


@dataclass
class ParseResult:
    """Result of parsing a complete verse.

    Attributes:
        original_text: The original input text.
        script: Detected or specified script.
        devanagari_text: Text normalized to Devanagari.
        padas: List of pāda strings.
        syllables_by_pada: List of syllable lists, one per pāda.
        total_syllables: Total number of syllables across all pādas.
    """
    original_text: str = ""
    script: str = "devanagari"
    devanagari_text: str = ""
    padas: list = field(default_factory=list)
    syllables_by_pada: list = field(default_factory=list)
    total_syllables: int = 0


# ===========================================================================
# Syllable Parser
# ===========================================================================

class SyllableParser:
    """Custom Devanagari syllable parser.

    Splits Sanskrit text (in Devanagari) into syllables (akṣara) following
    standard Sanskrit phonological rules for syllable boundaries.

    Rules:
    1. A syllable consists of an optional onset (consonants) + a vowel nucleus
       + optional coda (anusvāra, visarga, chandrabindu).
    2. Consonants followed by halant form conjuncts that belong to the NEXT syllable.
    3. A standalone independent vowel starts a new syllable.
    4. If a consonant has no halant and no explicit mātrā, it carries the
       inherent vowel 'a' (short).
    """

    def parse(self, text, script="devanagari"):
        """Parse a complete verse into syllables.

        Args:
            text: Sanskrit verse text.
            script: Input script ('devanagari', 'iast', 'hk', 'slp1', 'itrans').

        Returns:
            ParseResult with pādas and syllables.
        """
        if not text or not text.strip():
            return ParseResult(original_text=text or "", script=script)

        # Normalize and transliterate to Devanagari if needed
        from app.services.transliteration import normalize, to_devanagari, detect_script

        if script == "auto":
            script = detect_script(text)

        normalized = normalize(text, script)

        if script != "devanagari":
            devanagari_text = to_devanagari(normalized, script)
        else:
            devanagari_text = normalized

        # Split into pādas
        padas = self.split_padas(devanagari_text)

        # First pass: syllabify each pāda as-is
        raw_syllables = []
        for pada in padas:
            syllables = self.syllabify(pada)
            raw_syllables.append((pada, syllables))

        # Second pass: auto-split long pādas into sub-pādas
        # In Sanskrit verse, a daṇḍa (।) separates half-verses (2 pādas),
        # and a double daṇḍa (॥) separates full verses. So each "half"
        # may actually contain 2 pādas that need splitting.
        final_padas = []
        syllables_by_pada = []
        total = 0

        for pada_text, syllables in raw_syllables:
            syl_count = len(syllables)

            # Common split points: if syllable count is divisible by common
            # per-pada counts (8, 11, 12, 14, etc.) and the total suggests
            # it's a multi-pada half, split it.
            split = False
            for per_pada in [8, 11, 12, 14, 15, 17, 19, 21]:
                if syl_count == 2 * per_pada:
                    # This half contains exactly 2 pādas
                    mid = per_pada
                    pada1_syls = syllables[:mid]
                    pada2_syls = syllables[mid:]

                    # Reconstruct pāda text from syllables
                    pada1_text = "".join(s.text for s in pada1_syls)
                    pada2_text = "".join(s.text for s in pada2_syls)

                    # Reset positions and pada-final markers
                    for idx, s in enumerate(pada1_syls):
                        s.position = idx
                        s.is_pada_final = (idx == len(pada1_syls) - 1)
                    for idx, s in enumerate(pada2_syls):
                        s.position = idx
                        s.is_pada_final = (idx == len(pada2_syls) - 1)

                    final_padas.append(pada1_text)
                    final_padas.append(pada2_text)
                    syllables_by_pada.append(pada1_syls)
                    syllables_by_pada.append(pada2_syls)
                    total += syl_count
                    split = True
                    break

            if not split:
                # Keep as single pāda
                if syllables:
                    syllables[-1].is_pada_final = True
                final_padas.append(pada_text)
                syllables_by_pada.append(syllables)
                total += syl_count

        return ParseResult(
            original_text=text,
            script=script,
            devanagari_text=devanagari_text,
            padas=final_padas,
            syllables_by_pada=syllables_by_pada,
            total_syllables=total,
        )

    def split_padas(self, text):
        """Split a verse into pādas (quarter-verses).

        Splits on:
        - Double daṇḍa (॥) — full verse separator
        - Single daṇḍa (।) — half-verse separator
        - Pipe character (|) — common in digital texts
        - Newlines

        Args:
            text: Devanagari verse text.

        Returns:
            List of pāda strings (stripped, non-empty).
        """
        if not text:
            return []

        import re

        # Replace verse separators with a uniform delimiter
        # Order matters: check double daṇḍa before single
        normalized = text.replace("॥", "|").replace("।", "|")

        # Also split on newlines
        normalized = normalized.replace("\n", "|")

        # Split and filter empty parts
        parts = [p.strip() for p in normalized.split("|")]
        padas = [p for p in parts if p and self._has_devanagari(p)]

        return padas

    def syllabify(self, pada_text):
        """Split a single pāda into syllables.

        This is the core algorithm. It processes the Devanagari text
        character by character, building syllables according to
        Sanskrit phonological rules.

        Args:
            pada_text: A single pāda in Devanagari.

        Returns:
            List of Syllable objects.
        """
        if not pada_text:
            return []

        # Clean: remove spaces and non-Devanagari characters (keep avagraha)
        chars = []
        for ch in pada_text:
            if (ch in ALL_DEVANAGARI or ch == AVAGRAHA or
                    ch in INDEPENDENT_VOWELS or ch in CONSONANTS or
                    ch in DEPENDENT_VOWEL_SIGNS or
                    ch in {HALANT, NUKTA, ANUSVARA, VISARGA, CHANDRABINDU}):
                chars.append(ch)

        if not chars:
            return []

        # Build "units" — groups of characters that form logical units
        # Each unit is either:
        # - An independent vowel (possibly with anusvāra/visarga)
        # - A consonant cluster + vowel (explicit mātrā or inherent 'a')
        #   + optional anusvāra/visarga
        syllables = []
        i = 0
        n = len(chars)

        while i < n:
            syl_chars = []
            vowel_char = ""
            is_long = False
            has_anu = False
            has_vis = False
            has_chand = False

            # Case 1: Independent vowel starts a syllable
            if chars[i] in INDEPENDENT_VOWELS:
                syl_chars.append(chars[i])
                vowel_char = chars[i]
                is_long = chars[i] in LONG_VOWELS
                i += 1

                # Check for trailing anusvāra, visarga, chandrabindu
                while i < n and chars[i] in {ANUSVARA, VISARGA, CHANDRABINDU}:
                    syl_chars.append(chars[i])
                    if chars[i] == ANUSVARA:
                        has_anu = True
                    elif chars[i] == VISARGA:
                        has_vis = True
                    elif chars[i] == CHANDRABINDU:
                        has_chand = True
                    i += 1

            # Case 2: Consonant (possibly with conjuncts) + vowel
            elif chars[i] in CONSONANTS:
                # Consume consonant cluster: C + halant + C + halant + ... + C
                while i < n and chars[i] in CONSONANTS:
                    syl_chars.append(chars[i])
                    i += 1

                    # Check for nukta
                    if i < n and chars[i] == NUKTA:
                        syl_chars.append(chars[i])
                        i += 1

                    # Check for halant — if present, next consonant joins the cluster
                    if i < n and chars[i] == HALANT:
                        # Look ahead: if another consonant follows, it's a conjunct
                        if i + 1 < n and chars[i + 1] in CONSONANTS:
                            syl_chars.append(chars[i])  # Include halant
                            i += 1  # Move past halant, loop will get next consonant
                        else:
                            # Halant at end — consonant with no vowel (rare in verse)
                            syl_chars.append(chars[i])
                            i += 1
                            # This consonant has halant at end; treat as having no vowel
                            vowel_char = ""
                            is_long = False
                            break
                    else:
                        break

                # Now check for dependent vowel sign (mātrā)
                if i < n and chars[i] in DEPENDENT_VOWEL_SIGNS:
                    syl_chars.append(chars[i])
                    vowel_char = chars[i]
                    is_long = chars[i] in LONG_DEPENDENT_SIGNS
                    i += 1
                else:
                    # No explicit mātrā — inherent short 'a'
                    # (unless we already set vowel_char="" from halant-final above)
                    if vowel_char != "" or not syl_chars or syl_chars[-1] != HALANT:
                        vowel_char = "\u0905"  # inherent 'a'
                        is_long = False

                # Check for trailing anusvāra, visarga, chandrabindu
                while i < n and chars[i] in {ANUSVARA, VISARGA, CHANDRABINDU}:
                    syl_chars.append(chars[i])
                    if chars[i] == ANUSVARA:
                        has_anu = True
                    elif chars[i] == VISARGA:
                        has_vis = True
                    elif chars[i] == CHANDRABINDU:
                        has_chand = True
                    i += 1

            # Case 3: Avagraha (ऽ) — represents elided 'a', treated as short vowel syllable
            elif chars[i] == AVAGRAHA:
                syl_chars.append(chars[i])
                vowel_char = "\u0905"  # Treated as short 'a'
                is_long = False
                i += 1

            # Case 4: Standalone anusvāra/visarga/chandrabindu (shouldn't happen normally)
            elif chars[i] in {ANUSVARA, VISARGA, CHANDRABINDU}:
                # Attach to previous syllable if possible
                if syllables:
                    prev = syllables[-1]
                    prev.text += chars[i]
                    if chars[i] == ANUSVARA:
                        prev.has_anusvara = True
                    elif chars[i] == VISARGA:
                        prev.has_visarga = True
                    elif chars[i] == CHANDRABINDU:
                        prev.has_chandrabindu = True
                i += 1
                continue

            # Case 5: Halant without preceding consonant (shouldn't happen)
            elif chars[i] == HALANT:
                i += 1
                continue

            # Case 6: Any other character — skip
            else:
                i += 1
                continue

            # Build syllable object or merge with previous if halant-final
            if syl_chars:
                if vowel_char == "" and syllables:
                    # Halant at the end of a word — merge into previous syllable
                    prev = syllables[-1]
                    prev.text += "".join(syl_chars)
                    # A trailing halant makes the previous syllable heavy (Guru) by saṃyoga rule
                    # But we'll handle this in the Laghu-Guru classifier, because the classifier
                    # checks for trailing halant. Actually, let's mark consonant_cluster_follows
                    # to True for the previous syllable if it's merged!
                    prev.consonant_cluster_follows = True
                else:
                    syl = Syllable(
                        text="".join(syl_chars),
                        vowel=vowel_char,
                        is_long_vowel=is_long,
                        has_anusvara=has_anu,
                        has_visarga=has_vis,
                        has_chandrabindu=has_chand,
                        position=len(syllables),
                    )
                    syllables.append(syl)

        # Second pass: determine consonant_cluster_follows for each syllable
        self._mark_consonant_clusters(syllables, chars)

        return syllables

    def _mark_consonant_clusters(self, syllables, chars):
        """Mark syllables where a consonant cluster follows.

        A syllable has consonant_cluster_follows=True if the next syllable
        begins with a conjunct consonant (2+ consonants joined by halant).
        This is needed for the saṃyoga rule in L-G classification.

        This is determined by checking if the text of the next syllable
        contains a halant (indicating a conjunct onset).
        """
        for i in range(len(syllables) - 1):
            next_syl = syllables[i + 1]
            # Count consonants at the start of the next syllable
            consonant_count = 0
            for ch in next_syl.text:
                if ch in CONSONANTS:
                    consonant_count += 1
                elif ch == HALANT or ch == NUKTA:
                    continue  # Part of conjunct, keep counting
                else:
                    break  # Hit a vowel/mātrā, stop

            if consonant_count >= 2:
                syllables[i].consonant_cluster_follows = True

    def _has_devanagari(self, text):
        """Check if text contains any Devanagari characters."""
        return any("\u0900" <= ch <= "\u097F" for ch in text)


# Module-level convenience instance
parser = SyllableParser()
