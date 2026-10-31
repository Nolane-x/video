import unittest

from validate_hyperframes_report import validate_report


def clean_report():
    return {
        "ok": True,
        "strict": True,
        "snapshots": {"enabled": True},
        "lint": {"ok": True, "errorCount": 0, "warningCount": 0, "findings": []},
        "runtime": {"ok": True, "errorCount": 0, "warningCount": 0, "findings": []},
        "layout": {"ok": True, "errorCount": 0, "warningCount": 0, "findings": []},
        "motion": {"ok": True, "errorCount": 0, "warningCount": 0, "enabled": True, "samples": 8, "findings": []},
        "contrast": {"ok": True, "errorCount": 0, "warningCount": 0, "enabled": True, "findings": []},
        "craft": {"ok": True, "errorCount": 0, "warningCount": 0, "findings": []},
    }


class HyperFramesReportTests(unittest.TestCase):
    def test_clean_strict_report_passes(self):
        self.assertEqual(validate_report(clean_report()), [])

    def test_report_with_contrast_error_fails(self):
        report = clean_report()
        report["contrast"]["ok"] = False
        report["contrast"]["errorCount"] = 1
        report["contrast"]["findings"] = [{"severity": "error", "code": "contrast_aa_failure"}]
        self.assertTrue(any("contrast" in item for item in validate_report(report)))

    def test_report_with_craft_warning_fails(self):
        report = clean_report()
        report["craft"]["warningCount"] = 1
        report["craft"]["findings"] = [{"severity": "warning", "code": "line_unread"}]
        self.assertTrue(any("warningCount=1" in item for item in validate_report(report)))

    def test_report_without_motion_sidecar_fails(self):
        report = clean_report()
        report["motion"]["enabled"] = False
        report["motion"]["samples"] = 0
        self.assertTrue(any("motion" in item for item in validate_report(report)))

    def test_non_strict_report_fails(self):
        report = clean_report()
        report["strict"] = False
        self.assertTrue(any("strict mode" in item for item in validate_report(report)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
