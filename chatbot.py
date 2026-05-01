import json
import random
import re
import os
from typing import Optional


class ChatbotAkademik:
    """
    Chatbot berbasis intent untuk layanan akademik kampus.
    Menggunakan pencocokan kata kunci untuk menentukan respons yang sesuai.
    """

    def __init__(self, intents_path: Optional[str] = None):
        if intents_path is None:
            intents_path = os.path.join(
                os.path.dirname(__file__), "data", "intents.json"
            )
        self.intents = self._load_intents(intents_path)
        self._build_pattern_index()

    def _load_intents(self, path: str) -> list:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("intents", [])

    def _normalize(self, text: str) -> str:
        """Normalisasi teks: lowercase dan hapus tanda baca."""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _build_pattern_index(self):
        """Bangun indeks pola dari semua intent untuk pencocokan cepat."""
        self._pattern_index = []
        for intent in self.intents:
            if intent.get("tag") == "tidak_dipahami":
                continue
            normalized_patterns = [
                self._normalize(p) for p in intent.get("patterns", [])
            ]
            self._pattern_index.append(
                {
                    "tag": intent["tag"],
                    "patterns": normalized_patterns,
                    "responses": intent.get("responses", []),
                }
            )
        # Simpan fallback intent
        self._fallback_responses = []
        for intent in self.intents:
            if intent.get("tag") == "tidak_dipahami":
                self._fallback_responses = intent.get("responses", [])
                break

    def _phrase_match(self, pattern_words: list, input_words: list) -> bool:
        """Cek apakah pattern_words muncul sebagai urutan kata berturut-turut dalam input_words."""
        k = len(pattern_words)
        n = len(input_words)
        for i in range(n - k + 1):
            if input_words[i : i + k] == pattern_words:
                return True
        return False

    def _score_intent(self, normalized_input: str, patterns: list) -> float:
        """
        Hitung skor kecocokan antara input dan daftar pola.
        Menggunakan pencocokan kata (bukan substring) untuk mencegah false-positive.
        Mengembalikan nilai antara 0.0 dan 1.0.
        """
        input_words_list = normalized_input.split()
        input_words_set = set(input_words_list)
        best_score = 0.0

        for pattern in patterns:
            pattern_words = pattern.split()
            if not pattern_words:
                continue

            # Cek pencocokan frasa tepat (berurutan, per-kata)
            if self._phrase_match(pattern_words, input_words_list):
                score = 1.0
            else:
                # Hitung overlap kata (tidak harus berurutan)
                overlap = input_words_set & set(pattern_words)
                score = len(overlap) / len(pattern_words)

            if score > best_score:
                best_score = score

        return best_score

    def predict_intent(self, user_input: str) -> str:
        """Prediksi tag intent dari input pengguna."""
        normalized = self._normalize(user_input)
        if not normalized:
            return "tidak_dipahami"

        best_tag = "tidak_dipahami"
        best_score = 0.0
        threshold = 0.3  # Ambang batas minimum skor

        for entry in self._pattern_index:
            score = self._score_intent(normalized, entry["patterns"])
            if score > best_score:
                best_score = score
                best_tag = entry["tag"]

        if best_score < threshold:
            return "tidak_dipahami"

        return best_tag

    def get_response(self, user_input: str) -> str:
        """
        Proses input pengguna dan kembalikan respons chatbot.
        """
        tag = self.predict_intent(user_input)

        if tag == "tidak_dipahami":
            if self._fallback_responses:
                return random.choice(self._fallback_responses)
            return "Maaf, saya belum memahami pertanyaan Anda."

        for entry in self._pattern_index:
            if entry["tag"] == tag:
                return random.choice(entry["responses"])

        return "Maaf, terjadi kesalahan. Silakan coba lagi."
