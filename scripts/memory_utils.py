import os
import yaml
import re
import hashlib

class WFNodeManager:
    def __init__(self, workflows_dir=None, output_root=None):
        self.workflows_dir = workflows_dir or "agent-output/workflows"
        self.output_root = output_root or "agent-output"
        self.next_id_path = os.path.join(self.output_root, ".next-id")

    def create_node(self, node_id, slug, node_type, parent, planka_card, handoff_id, summary_lines=None, artifact_path=None):
        # SECURITY (INJ-001): Path sanitisation using os.path.basename
        clean_node_id = os.path.basename(str(node_id))
        clean_slug = os.path.basename(str(slug))
        full_id = f"WF-{clean_node_id}" if not clean_node_id.startswith("WF-") else clean_node_id
        
        filename = f"{full_id}-{clean_slug}.md"
        filepath = os.path.abspath(os.path.join(self.workflows_dir, filename))
        
        # Verify it stays inside workflows_dir
        if not filepath.startswith(os.path.abspath(self.workflows_dir)):
            raise ValueError(f"Security Violation: Path traversal detected for {filepath}")

        # Enforce 10-Line Rule for summary
        if summary_lines and len(summary_lines) > 3:
            summary_lines = summary_lines[:3]
        
        frontmatter = {
            "type": node_type,
            "parent": parent,
            "Planka-Card": str(planka_card),
            "handoff_id": handoff_id
        }

        # SECURITY (INTEGRITY-001): Hash linked artifact
        if artifact_path:
            frontmatter["artifact_hash"] = self._calculate_hash(artifact_path)
            frontmatter["artifact_path"] = artifact_path
        
        content = "---\n"
        content += yaml.dump(frontmatter, sort_keys=False)
        content += "---\n\n"
        content += "## Summary\n"
        if summary_lines:
            for line in summary_lines:
                content += f"- {line}\n"
        
        with open(filepath, "w") as f:
            f.write(content)
            
        return filepath

    def _calculate_hash(self, filepath):
        if not os.path.exists(filepath):
            return None
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256.update(byte_block)
        return sha256.hexdigest()

    def verify_integrity(self, node_id, slug, artifact_path=None):
        clean_node_id = os.path.basename(str(node_id))
        clean_slug = os.path.basename(str(slug))
        full_id = f"WF-{clean_node_id}" if not clean_node_id.startswith("WF-") else clean_node_id
        filename = f"{full_id}-{clean_slug}.md"
        filepath = os.path.join(self.workflows_dir, filename)
        
        if not os.path.exists(filepath):
            return False
            
        with open(filepath, "r") as f:
            content = f.read()
            
        # Parse frontmatter
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            return False
            
        try:
            frontmatter = yaml.safe_load(fm_match.group(1))
        except yaml.YAMLError:
            return False

        stored_hash = frontmatter.get("artifact_hash")
        artifact_to_check = artifact_path or frontmatter.get("artifact_path")
        
        if not stored_hash or not artifact_to_check:
            return False
            
        current_hash = self._calculate_hash(artifact_to_check)
        return stored_hash == current_hash

    def update_hash(self, node_id, slug, artifact_path=None):
        clean_node_id = os.path.basename(str(node_id))
        clean_slug = os.path.basename(str(slug))
        full_id = f"WF-{clean_node_id}" if not clean_node_id.startswith("WF-") else clean_node_id
        filename = f"{full_id}-{clean_slug}.md"
        filepath = os.path.join(self.workflows_dir, filename)
        
        if not os.path.exists(filepath):
            return False
            
        with open(filepath, "r") as f:
            content = f.read()
            
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            return False
            
        frontmatter = yaml.safe_load(fm_match.group(1))
        artifact_to_hash = artifact_path or frontmatter.get("artifact_path")
        
        if not artifact_to_hash:
            return False
            
        new_hash = self._calculate_hash(artifact_to_hash)
        frontmatter["artifact_hash"] = new_hash
        if artifact_path:
            frontmatter["artifact_path"] = artifact_path
            
        new_fm = yaml.dump(frontmatter, sort_keys=False)
        new_content = f"---\n{new_fm}---\n" + content[fm_match.end():].lstrip()
        
        with open(filepath, "w") as f:
            f.write(new_content)
        return True

    def get_next_id(self, increment=False):
        if not os.path.exists(self.next_id_path):
            with open(self.next_id_path, "w") as f:
                f.write("1")
            return 1
            
        with open(self.next_id_path, "r") as f:
            current_id = int(f.read().strip())
            
        if increment:
            with open(self.next_id_path, "w") as f:
                f.write(str(current_id + 1))
                
        return current_id

    def validate_links(self, node_id, slug):
        filename = f"{node_id}-{slug}.md"
        filepath = os.path.join(self.workflows_dir, filename)
        if not os.path.exists(filepath):
            return []
            
        with open(filepath, "r") as f:
            content = f.read()
            
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        broken = []
        for link in links:
            # Check if link points to another WF node or an agent-output artifact
            # For simplicity, if it starts with 'agent-output/' or 'workflows/'
            # actually obsidian wikilinks are often just filenames.
            # But the contract said 'Direct wikilinks to agent-output/ artifacts'.
            # [[agent-output/architecture/003-obsidian-memory-architecture-findings.md]]
            
            clean_link = link.split("|")[0]
            # Resolve relative to workspace root
            # The workspace root is the base for git relative paths in the repo
            full_path = os.path.join(self.output_root, "..", clean_link)
            if not os.path.exists(full_path):
                # Also check relative to workflows_dir if it's node-to-node
                node_link_path = os.path.join(self.workflows_dir, clean_link + ".md")
                if not os.path.exists(node_link_path):
                     broken.append(link)
        return broken

    def update_node_status(self, node_id, slug, new_status, handoff_id_key):
        full_id = f"WF-{node_id}" if not str(node_id).startswith("WF-") else node_id
        filename = f"{full_id}-{slug}.md"
        filepath = os.path.join(self.workflows_dir, filename)
        if not os.path.exists(filepath):
            return False
            
        with open(filepath, "r") as f:
            lines = f.readlines()
            
        # Check handoff_id match for security/locking
        # Support both single and double quotes since yaml.dump might vary
        found_handoff = False
        status_line_idx = -1
        
        # Regex to find handoff_id regardless of quotes
        # Matches: handoff_id: value OR handoff_id: 'value' OR handoff_id: "value"
        # Handles potential whitespace
        handoff_pattern = re.compile(rf'^\s*handoff_id:\s*[\'"]?{re.escape(handoff_id_key)}[\'"]?\s*$', re.IGNORECASE)
        
        for i, line in enumerate(lines):
            if handoff_pattern.match(line.strip()):
                found_handoff = True
            if line.startswith("status:"):
                status_line_idx = i
                
        if not found_handoff:
            return False # Security: handoff_id mismatch
            
        if status_line_idx != -1:
            lines[status_line_idx] = f"status: {new_status}\n"
        else:
            # Insert before the last --- of the frontmatter
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    lines.insert(i, f"status: {new_status}\n")
                    break
                    
        with open(filepath, "w") as f:
            f.writelines(lines)
            
        return True

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="WF Node Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Create node
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--id", required=True)
    create_parser.add_argument("--slug", required=True)
    create_parser.add_argument("--type", required=True)
    create_parser.add_argument("--parent", required=True)
    create_parser.add_argument("--card", required=True)
    create_parser.add_argument("--handoff", required=True)
    create_parser.add_argument("--summary", action="append")
    create_parser.add_argument("--artifact", help="Path to linked artifact for hashing")

    # Get next ID
    id_parser = subparsers.add_parser("next-id")
    id_parser.add_argument("--increment", action="store_true")

    # Validate links
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--id", required=True)
    validate_parser.add_argument("--slug", required=True)

    # Update status
    status_parser = subparsers.add_parser("update-status")
    status_parser.add_argument("--id", required=True)
    status_parser.add_argument("--slug", required=True)
    status_parser.add_argument("--status", required=True)
    status_parser.add_argument("--handoff", required=True)

    # Update hash
    update_hash_parser = subparsers.add_parser("update-hash")
    update_hash_parser.add_argument("--id", required=True)
    update_hash_parser.add_argument("--slug", required=True)
    update_hash_parser.add_argument("--artifact", help="Path to linked artifact")

    # Verify integrity
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--id", required=True)
    verify_parser.add_argument("--slug", required=True)
    verify_parser.add_argument("--artifact", help="Path to linked artifact")

    args = parser.parse_args()
    manager = WFNodeManager()

    if args.command == "create":
        path = manager.create_node(args.id, args.slug, args.type, args.parent, args.card, args.handoff, args.summary, artifact_path=args.artifact)
        print(f"Created node at {path}")
    elif args.command == "next-id":
        print(manager.get_next_id(increment=args.increment))
    elif args.command == "validate":
        broken = manager.validate_links(args.id, args.slug)
        if broken:
            print(f"Broken links found: {', '.join(broken)}")
            sys.exit(1)
        else:
            print("All links valid.")
    elif args.command == "update-status":
        success = manager.update_node_status(args.id, args.slug, args.status, args.handoff)
        if success:
            print("Status updated successfully.")
        else:
            print("Failed to update status (id mismatch or file not found).")
            sys.exit(1)
    elif args.command == "update-hash":
        success = manager.update_hash(args.id, args.slug, artifact_path=args.artifact)
        if success:
            print("Hash updated successfully.")
        else:
            print("Failed to update hash.")
            sys.exit(1)
    elif args.command == "verify":
        valid = manager.verify_integrity(args.id, args.slug, artifact_path=args.artifact)
        if valid:
            print("Integrity verified.")
        else:
            print("Integrity check FAILED.")
            sys.exit(1)
