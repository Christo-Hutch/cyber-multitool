import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.models.portAnalyser.bannerGrabber import BannerGrabber

class TestBannerGrabber(unittest.TestCase):

    MOCK_JSON_DATA = """{
        "21": {"payload": "USER anonymous\\\\r\\\\n"},
        "default": {"payload": "\\\\r\\\\n\\\\r\\\\n"}
    }"""

    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
    def test_get_probe_dict(self, mock_file):
        """Verify initialization reads and parses the JSON config file."""
        grabber = BannerGrabber("127.0.0.1")
        
        self.assertIn("21", grabber.probe_dict)
        self.assertEqual(grabber.probe_dict["21"]["payload"], "USER anonymous\r\n")
        mock_file.assert_called_once_with("src/config/port_probes.json", "r")

    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
    def test_get_probe_conversion(self, mock_file):
        """Test payload retrieval and backslash escaping conversions."""
        grabber = BannerGrabber("127.0.0.1")

        probe_21 = grabber.get_probe(21)
        self.assertEqual(probe_21, b"USER anonymous\r\n")

        probe_default = grabber.get_probe(80)
        self.assertEqual(probe_default, b"\r\n\r\n")

    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
    @patch("socket.create_connection")
    def test_banner_grabber_success(self, mock_create_connection, mock_file):
        """Verify banner_grabber sends payload and returns bytes on success."""
        mock_sock = MagicMock()
        mock_sock.recv.return_value = b"220 FTP Server Ready"
        mock_create_connection.return_value.__enter__.return_value = mock_sock

        grabber = BannerGrabber("127.0.0.1")

        response = grabber.banner_grabber(21)

        self.assertEqual(response, b"220 FTP Server Ready")
        mock_sock.sendall.assert_called_once_with(b"USER anonymous\r\n")

    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
    @patch("socket.create_connection")
    def test_banner_grabber_empty_response(self, mock_create_connection, mock_file):
        """Verify handling of an empty byte response."""
        mock_sock = MagicMock()
        mock_sock.recv.return_value = b""
        mock_create_connection.return_value.__enter__.return_value = mock_sock

        grabber = BannerGrabber("127.0.0.1")
        response = grabber.banner_grabber(21)

        self.assertEqual(response, "[EMPTY RESPONSE]")

    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_JSON_DATA)
    @patch("socket.create_connection")
    def test_banner_grabber_timeout(self, mock_create_connection, mock_file):
        """Verify TimeoutError returns None safely."""
        mock_create_connection.return_value.__enter__.side_effect = TimeoutError()

        grabber = BannerGrabber("127.0.0.1")
        response = grabber.banner_grabber(80)

        self.assertIsNone(response)

if __name__ == "__main__":
    unittest.main()