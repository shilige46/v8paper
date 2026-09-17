from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.sync_official import CATALOG_FILES, download_snapshot


class FakeResponse(BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


class SyncOfficialTests(unittest.TestCase):
    def test_catalog_file_list_covers_all_official_volumes(self):
        self.assertEqual(11, len(CATALOG_FILES))
        self.assertEqual("catalog-0001-0100.md", CATALOG_FILES[0])
        self.assertEqual("catalog-1001-1022.md", CATALOG_FILES[-1])

    def test_download_snapshot_pins_urls_and_hashes_files(self):
        requested = []
        commit = "a" * 40

        def opener(url):
            requested.append(url)
            filename = url.rsplit("/", 1)[-1]
            return FakeResponse(f"content for {filename}\n".encode("utf-8"))

        with TemporaryDirectory() as tmp:
            output = Path(tmp) / "raw"
            manifest = download_snapshot(output, commit, opener=opener)

            self.assertEqual("TheJustinSunPrize/awards", manifest["source_repository"])
            self.assertEqual(commit, manifest["source_commit"])
            self.assertEqual(list(CATALOG_FILES), manifest["files"])
            self.assertEqual(11, len(manifest["sha256"]))
            self.assertEqual(11, len(requested))
            for filename, url in zip(CATALOG_FILES, requested, strict=True):
                self.assertIn(commit, url)
                self.assertTrue(url.endswith("/problems/" + filename))
                self.assertTrue((output / filename).is_file())

    def test_rejects_non_commit_ref(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                download_snapshot(Path(tmp), "main", opener=lambda _: None)


if __name__ == "__main__":
    unittest.main()
