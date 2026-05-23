import socket
import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.models.portAnalyser.portScanner import PortScanner

class TestPortScanner(unittest.TestCase):

    def setUp(self):
        """Set up a target and range for scanner testing."""
        self.target = "127.0.0.1"
        self.port_range = (20, 25)  # 6 ports: 20, 21, 22, 23, 24, 25

    def test_fill_port_queue(self):
        """Verify the queue correctly populates with the specified range."""
        scanner = PortScanner(self.target, self.port_range)
        self.assertEqual(scanner.port_queue.qsize(), 6)

        ports = []
        while not scanner.port_queue.empty():
            ports.append(scanner.port_queue.get())
        self.assertEqual(ports, [20, 21, 22, 23, 24, 25])

    @patch("socket.socket")
    def test_port_scan_open(self, mock_socket_cls):
        """Verify port_scan returns True when connection succeeds."""
        mock_socket_instance = MagicMock()
        mock_socket_cls.return_value = mock_socket_instance

        scanner = PortScanner(self.target, self.port_range)

        result = scanner.port_scan(80)

        self.assertTrue(result)
        mock_socket_instance.connect.assert_called_once_with((self.target, 80))
        mock_socket_instance.close.assert_called_once()

    @patch("socket.socket")
    def test_port_scan_closed(self, mock_socket_cls):
        """Verify port_scan returns False when connection fails."""
        mock_socket_instance = MagicMock()
        mock_socket_instance.connect.side_effect = socket.error("Connection refused")
        mock_socket_cls.return_value = mock_socket_instance

        scanner = PortScanner(self.target, self.port_range)

        result = scanner.port_scan(80)

        self.assertFalse(result)

    @patch.object(PortScanner, "port_scan")
    def test_get_open_ports(self, mock_port_scan):
        """Test threading logic collects discovered open ports accurately."""
        def side_effect(port):
            return port in [22, 25]
        mock_port_scan.side_effect = side_effect

        scanner = PortScanner(self.target, self.port_range)

        open_ports = scanner.get_open_ports()

        self.assertEqual(set(open_ports), {22, 25})

if __name__ == "__main__":
    unittest.main()