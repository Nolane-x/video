import unittest

from crew_mesh_policy import is_unwanted_crew_mesh


class CrewMeshPolicyTests(unittest.TestCase):
    def test_rejects_icosphere_leftover_seen_in_pbr_smoke(self):
        self.assertTrue(is_unwanted_crew_mesh(
            "Icosphere", "Icosphere", (), (1.902, 2.0, 2.0)
        ))

    def test_rejects_unmaterialed_oversized_helper_even_if_renamed(self):
        self.assertTrue(is_unwanted_crew_mesh(
            "Imported helper 07", "Mesh.007", (), (1.9, 2.0, 2.0)
        ))

    def test_keeps_valid_skinned_body_with_skin_material(self):
        self.assertFalse(is_unwanted_crew_mesh(
            "Body", "base", ("Skin",), (0.981, 0.697, 1.681)
        ))

    def test_keeps_small_material_free_detail(self):
        self.assertFalse(is_unwanted_crew_mesh(
            "Small helper", "Mesh.001", (), (0.1, 0.08, 0.05)
        ))


if __name__ == "__main__":
    unittest.main()
