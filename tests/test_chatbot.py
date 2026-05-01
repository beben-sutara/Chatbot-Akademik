import json
import pytest
import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from chatbot import ChatbotAkademik


@pytest.fixture(scope="module")
def bot():
    return ChatbotAkademik()


# ---------------------------------------------------------------------------
# Intent detection tests
# ---------------------------------------------------------------------------

class TestIntentDetection:
    def test_salam_halo(self, bot):
        assert bot.predict_intent("halo") == "salam"

    def test_salam_selamat_pagi(self, bot):
        assert bot.predict_intent("selamat pagi") == "salam"

    def test_perpisahan(self, bot):
        assert bot.predict_intent("sampai jumpa") == "perpisahan"

    def test_terima_kasih(self, bot):
        assert bot.predict_intent("terima kasih") == "terima_kasih"

    def test_pendaftaran(self, bot):
        assert bot.predict_intent("cara mendaftar mahasiswa baru") == "pendaftaran_mahasiswa_baru"

    def test_biaya_kuliah(self, bot):
        assert bot.predict_intent("berapa biaya kuliah") == "biaya_kuliah"

    def test_beasiswa(self, bot):
        assert bot.predict_intent("informasi beasiswa") == "beasiswa"

    def test_jadwal_kuliah(self, bot):
        assert bot.predict_intent("jadwal kuliah semester ini") == "jadwal_kuliah"

    def test_krs(self, bot):
        assert bot.predict_intent("cara isi krs online") == "krs"

    def test_nilai(self, bot):
        assert bot.predict_intent("lihat nilai ipk") == "nilai_ipk"

    def test_wisuda(self, bot):
        assert bot.predict_intent("syarat wisuda") == "wisuda"

    def test_skripsi(self, bot):
        assert bot.predict_intent("prosedur skripsi") == "skripsi_ta"

    def test_perpustakaan(self, bot):
        assert bot.predict_intent("pinjam buku perpustakaan") == "perpustakaan"

    def test_kalender_akademik(self, bot):
        assert bot.predict_intent("kalender akademik semester") == "kalender_akademik"

    def test_kontak(self, bot):
        assert bot.predict_intent("nomor telepon kampus") == "kontak"

    def test_program_studi(self, bot):
        assert bot.predict_intent("daftar program studi") == "program_studi"

    def test_pkl_magang(self, bot):
        assert bot.predict_intent("syarat pkl magang") == "pkl_magang"

    def test_organisasi(self, bot):
        assert bot.predict_intent("daftar ukm organisasi") == "organisasi_mahasiswa"

    def test_cuti(self, bot):
        assert bot.predict_intent("prosedur cuti kuliah") == "cuti_akademik"

    def test_transfer(self, bot):
        assert bot.predict_intent("pindah kuliah") == "transfer_mahasiswa"

    def test_bantuan(self, bot):
        assert bot.predict_intent("bantuan") == "bantuan_umum"

    def test_unknown_returns_fallback(self, bot):
        assert bot.predict_intent("xyzqwertyuiop") == "tidak_dipahami"

    def test_empty_input_returns_fallback(self, bot):
        assert bot.predict_intent("") == "tidak_dipahami"


# ---------------------------------------------------------------------------
# Response tests
# ---------------------------------------------------------------------------

class TestResponses:
    def test_response_is_string(self, bot):
        response = bot.get_response("halo")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_response_not_empty_for_known_intent(self, bot):
        for phrase in ["beasiswa", "jadwal kuliah", "wisuda", "krs", "kontak"]:
            resp = bot.get_response(phrase)
            assert resp, f"Respons kosong untuk input: '{phrase}'"

    def test_fallback_response_for_gibberish(self, bot):
        resp = bot.get_response("asdfghjklzxcvbnm")
        assert isinstance(resp, str)
        assert len(resp) > 0

    def test_whitespace_input_fallback(self, bot):
        resp = bot.get_response("   ")
        assert isinstance(resp, str)

    def test_beasiswa_response_contains_kip(self, bot):
        resp = bot.get_response("beasiswa")
        assert "KIP" in resp or "beasiswa" in resp.lower()

    def test_kontak_response_contains_email_or_phone(self, bot):
        resp = bot.get_response("kontak kampus")
        assert "@" in resp or "021" in resp or "0812" in resp


# ---------------------------------------------------------------------------
# Normalization tests
# ---------------------------------------------------------------------------

class TestNormalization:
    def test_normalize_lowercase(self, bot):
        assert bot._normalize("HALO") == "halo"

    def test_normalize_strips_punctuation(self, bot):
        assert bot._normalize("halo!") == "halo"

    def test_normalize_collapses_spaces(self, bot):
        assert bot._normalize("  jadwal   kuliah  ") == "jadwal kuliah"

    def test_normalize_mixed(self, bot):
        assert bot._normalize("Apa Jadwal Kuliah?") == "apa jadwal kuliah"


# ---------------------------------------------------------------------------
# Intents data integrity tests
# ---------------------------------------------------------------------------

class TestIntentsData:
    def test_intents_file_loads(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "data", "intents.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert "intents" in data
        assert len(data["intents"]) > 0

    def test_each_intent_has_tag_and_responses(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "data", "intents.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for intent in data["intents"]:
            assert "tag" in intent, f"Intent tanpa 'tag': {intent}"
            assert "responses" in intent, f"Intent '{intent['tag']}' tanpa 'responses'"
            assert len(intent["responses"]) > 0, f"Intent '{intent['tag']}' memiliki responses kosong"
