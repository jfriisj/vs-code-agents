import os
import hashlib
import sys
import unittest
from memory_utils import WFNodeManager

class TestMemoryUtilsSecurity(unittest.TestCase):
    def setUp(self):
        self.test_output_root = "test-agent-output"
        self.test_workflows_dir = os.path.join(self.test_output_root, "workflows")
        os.makedirs(self.test_workflows_dir, exist_ok=True)
        self.manager = WFNodeManager(workflows_dir=self.test_workflows_dir, output_root=self.test_output_root)

    def tearDown(self):
        import shutil
        if os.path.exists(self.test_output_root):
            shutil.rmtree(self.test_output_root)

    def test_path_traversal_prevention(self):
        # Malicious slug attempting to escape workflows_dir
        malicious_slug = "../../../etc/passwd"
        node_id = "WF-TEST-TRAVERSAL"
        # We expect basename to clean this to 'passwd'
        filepath = self.manager.create_node(node_id, malicious_slug, "Test", "[[WF-PARENT]]", "123", "[[WF-H]]")
        
        # Verify it stays inside the test workflows dir
        # Use abspath for robust comparison
        self.assertTrue(os.path.abspath(filepath).startswith(os.path.abspath(self.test_workflows_dir)))
        self.assertIn("passwd.md", filepath)
        self.assertNotIn("etc", filepath)

    def test_integrity_verification(self):
        # Create a dummy artifact
        artifact_path = os.path.join(self.test_output_root, "dummy_artifact.md")
        artifact_content = "Canonical Content"
        with open(artifact_path, "w") as f:
            f.write(artifact_content)
        
        # Calculate expected hash
        expected_hash = hashlib.sha256(artifact_content.encode()).hexdigest()
        
        # Create node with linked artifact (using a method we'll implement)
        node_id = "WF-TEST-INTEGRITY"
        slug = "test-integrity"
        # We'll update create_node to take artifact_path or add update_hash
        filepath = self.manager.create_node(node_id, slug, "Test", "[[WF-P]]", "123", "[[WF-H]]", artifact_path=artifact_path)
        
        # Verify hash is in frontmatter
        with open(filepath, "r") as f:
            content = f.read()
            self.assertIn(f"artifact_hash: {expected_hash}", content)
        
        # Verify successful check
        self.assertTrue(self.manager.verify_integrity(node_id, slug, artifact_path))
        
        # Tamper with artifact
        with open(artifact_path, "a") as f:
            f.write("\nTampered!")
            
        # Verify failed check
        self.assertFalse(self.manager.verify_integrity(node_id, slug, artifact_path))

if __name__ == "__main__":
    unittest.main()
