import unicodedata
import unittest

from ideaengine.text import slugify


class SlugifyTest(unittest.TestCase):
    def test_slugify_serbian(self):
        self.assertEqual(
            slugify("Računovođe ručno prepisuju fakture"), "racunovodje-rucno-prepisuju-fakture"
        )

    def test_slugify_nfd_equals_nfc(self):
        s = "Čačak, Ćuprija, Šabac, Žabalj, Đakovica"
        self.assertEqual(slugify(unicodedata.normalize("NFD", s)), slugify(s))

    def test_slugify_casefold_specials(self):
        self.assertEqual(slugify("Straße ſtore"), "strasse-store")

    def test_slugify_latin_letters_without_decomposition(self):
        # NFKD leaves these whole, so without a map they would vanish from the slug.
        self.assertEqual(slugify("Ærø æble øl"), "aero-aeble-ol")
        self.assertEqual(slugify("Łódź łąka"), "lodz-laka")
        self.assertEqual(slugify("Œuvre þing ðað"), "oeuvre-thing-dad")
        self.assertEqual(slugify("Đorđe"), "djordje")

    def test_slugify_truncates_on_word_boundary(self):
        s = slugify("word " * 30)
        self.assertLessEqual(len(s), 60)
        self.assertFalse(s.endswith("-"))

    def test_slugify_empty(self):
        self.assertEqual([slugify("   "), slugify("!!!")], ["untitled", "untitled"])


if __name__ == "__main__":
    unittest.main()
