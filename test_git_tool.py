import unittest
from unittest.mock import patch


class TestMaybeOpenPR(unittest.TestCase):
    @patch("git_tool.webbrowser.open")
    def test_maybe_open_pr_url_construction(self, mock_web_open):
        from git_tool import maybe_open_pr

        branch_name = "test-branch"
        push_branch = True
        expected_url = f"https://github.com/rineheaj/Basketball-Predictions/pull/new/{branch_name}".lower()

        maybe_open_pr(branch_name, push_branch)

        mock_web_open.assert_called_once_with(expected_url)

if __name__ == "__main__":
    unittest.main()
