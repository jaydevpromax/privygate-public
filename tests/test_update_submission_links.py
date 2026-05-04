from __future__ import annotations

import unittest

from scripts.update_submission_links import (
    LinkSet,
    markdown_link,
    update_hackquest_fields,
    update_readme,
    update_x_post,
    validate_links,
)


GOOD_LINKS = LinkSet(
    github_url="https://github.com/example/privygate",
    demo_video_url="https://video.example/privygate",
    x_post_url="https://x.com/example/status/1",
    contract_address="0x1234567890abcdef1234567890abcdef12345678",
    explorer_url="https://explorer.0g.ai/address/0x1234567890abcdef1234567890abcdef12345678",
    deploy_tx_url="https://explorer.0g.ai/tx/0xdeploy",
    authority_tx_url="https://explorer.0g.ai/tx/0xauthority",
    policy_tx_url="https://explorer.0g.ai/tx/0xpolicy",
    verify_success_tx_url="https://explorer.0g.ai/tx/0xsuccess",
    revocation_tx_url="https://explorer.0g.ai/tx/0xrevocation",
    verify_failure_tx_url="https://explorer.0g.ai/tx/0xfailure",
)


class SubmissionLinkUpdateTest(unittest.TestCase):
    def test_validate_links_accepts_complete_link_set(self) -> None:
        self.assertEqual(validate_links(GOOD_LINKS), [])

    def test_validate_links_rejects_bad_url_and_contract_address(self) -> None:
        links = LinkSet(
            github_url="github.com/example/privygate",
            contract_address="0x1234",
            explorer_url="https://explorer.0g.ai/bad path",
        )

        errors = validate_links(links)

        self.assertIn("github_url must start with http:// or https://", errors)
        self.assertIn("explorer_url must not contain whitespace", errors)
        self.assertIn("contract_address must be an EVM-style address like 0x followed by 40 hex characters", errors)

    def test_markdown_link_handles_urls_addresses_and_missing_values(self) -> None:
        self.assertEqual(markdown_link("repo", "https://github.com/example/privygate"), "[repo](https://github.com/example/privygate)")
        self.assertEqual(markdown_link("contract", GOOD_LINKS.contract_address), f"`{GOOD_LINKS.contract_address}`")
        self.assertEqual(markdown_link("empty", ""), "TBD")

    def test_update_readme_fills_evidence_table_and_status(self) -> None:
        text = "\n".join(
            [
                "Current status: deployment pending.",
                "| Evidence | Value |",
                "|---|---|",
                "| 0G contract address | TBD |",
                "| Explorer link | TBD |",
                "| Authority registration tx | TBD |",
                "| Policy registration tx | TBD |",
                "| Verification success tx | TBD |",
                "| Revocation tx | TBD |",
                "| Verification failure tx | TBD |",
            ]
        )

        updated = update_readme(text, GOOD_LINKS)

        self.assertIn("Current status: deployed evidence recorded.", updated)
        self.assertIn(f"| 0G contract address | `{GOOD_LINKS.contract_address}` |", updated)
        self.assertIn(f"| Explorer link | [explorer]({GOOD_LINKS.explorer_url}) |", updated)
        self.assertNotIn("| Explorer link | TBD |", updated)

    def test_update_hackquest_fields_replaces_placeholders_and_marks_ready(self) -> None:
        text = "\n".join(
            [
                "| Field | Value |",
                "|---|---|",
                "| Repository | TODO: GitHub repository URL |",
                "| Demo video | TODO: demo video URL, under 3 minutes |",
                "| 0G contract address | TODO: deployed address |",
                "| 0G explorer link | TODO: explorer URL |",
                "| X public post | TODO: X post URL |",
                "TODO_GITHUB_REPO_URL",
                "TODO_0G_CONTRACT_ADDRESS",
                "| TODO | GitHub repository is public and contains the latest commit. |",
            ]
        )

        updated = update_hackquest_fields(text, GOOD_LINKS)

        self.assertIn(f"| Repository | [Repository]({GOOD_LINKS.github_url}) |", updated)
        self.assertIn(GOOD_LINKS.contract_address, updated)
        self.assertNotIn("TODO_GITHUB_REPO_URL", updated)
        self.assertNotIn("TODO_0G_CONTRACT_ADDRESS", updated)
        self.assertIn("| READY | GitHub repository is public and contains the latest commit. |", updated)

    def test_update_x_post_replaces_public_placeholders(self) -> None:
        text = "GitHub: <GITHUB_REPO_URL>\nDemo: <DEMO_VIDEO_URL>\n0G: <0G_EXPLORER_ACTIVITY_LINK>"

        updated = update_x_post(text, GOOD_LINKS)

        self.assertIn(GOOD_LINKS.github_url, updated)
        self.assertIn(GOOD_LINKS.demo_video_url, updated)
        self.assertIn(GOOD_LINKS.explorer_url, updated)
        self.assertNotIn("<GITHUB_REPO_URL>", updated)


if __name__ == "__main__":
    unittest.main()
