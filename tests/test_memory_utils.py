import pytest
import os
import yaml
from scripts.memory_utils import WFNodeManager

@pytest.fixture
def manager(tmp_path):
    workflows_dir = tmp_path / "workflows"
    workflows_dir.mkdir()
    
    agent_output_dir = tmp_path / "agent-output"
    agent_output_dir.mkdir()
    
    return WFNodeManager(workflows_dir=str(workflows_dir), output_root=str(agent_output_dir))

def test_wf_node_manager_create_node(manager):
    node_id = "WF-P002"
    slug = "obsidian-memory"
    node_type = "Planning"
    parent = "[[WF-E1.2]]"
    planka_card = "1729878166190688097"
    handoff_id = "[[WF-2]]"
    
    result_path = manager.create_node(
        node_id=node_id,
        slug=slug,
        node_type=node_type,
        parent=parent,
        planka_card=planka_card,
        handoff_id=handoff_id,
        summary_lines=["Test direct link to artifacts."]
    )
    
    # Assertions
    assert os.path.exists(result_path)
    assert result_path.endswith(f"{node_id}-{slug}.md")
    
    with open(result_path, "r") as f:
        content = f.read()
        assert "type: Planning" in content
        assert "parent: '[[WF-E1.2]]'" in content
        assert "Planka-Card: '1729878166190688097'" in content
        assert "handoff_id: '[[WF-2]]'" in content
        assert "Test direct link to artifacts." in content

def test_wf_node_manager_get_next_id(manager, tmp_path):
    next_id_file = tmp_path / "agent-output" / ".next-id"
    next_id_file.write_text("2")
    
    next_id = manager.get_next_id()
    assert next_id == 2
    
    # Test increments
    next_id = manager.get_next_id(increment=True)
    assert next_id == 2
    assert next_id_file.read_text() == "3"

def test_wf_node_manager_validate_links(manager, tmp_path):
    actual_file = tmp_path / "agent-output" / "doc.md"
    actual_file.write_text("content")
    
    # Create node with 1 valid and 1 broken link
    node_filepath = manager.create_node(
        node_id="WF-P002",
        slug="test",
        node_type="Testing",
        parent="None",
        planka_card="0",
        handoff_id="none",
        summary_lines=[
            "[[agent-output/doc.md]]",
            "[[broken/link.md]]"
        ]
    )
    
    broken = manager.validate_links("WF-P002", "test")
    assert "broken/link.md" in broken
    assert "agent-output/doc.md" not in broken

def test_wf_node_manager_update_status(manager):
    node_id = "WF-S001"
    slug = "status-test"
    handoff_id = "SECRET-KEY"
    
    manager.create_node(
        node_id=node_id,
        slug=slug,
        node_type="StatusTest",
        parent="None",
        planka_card="0",
        handoff_id=handoff_id
    )
    
    # Successful update
    assert manager.update_node_status(node_id, slug, "Closed", handoff_id) is True
    
    # Verify change
    node_path = os.path.join(manager.workflows_dir, f"{node_id}-{slug}.md")
    with open(node_path, "r") as f:
        content = f.read()
        assert "status: Closed" in content
        
    # Mismatched handoff_id (should fail)
    assert manager.update_node_status(node_id, slug, "Active", "WRONG-KEY") is False
    with open(node_path, "r") as f:
        content = f.read()
        assert "status: Closed" in content # Still closed
