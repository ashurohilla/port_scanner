import socket
import threading
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from .serializers import PortScannerSerializer

class PortScannerViewSet(ViewSet):
    @staticmethod
    def scan_port(target_address, port, open_ports):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_address, port))
            if result == 0:
                open_ports.append(port)
        except socket.error:
            pass
        finally:
            sock.close()

    @action(detail=False, methods=['get', 'post'])
    def scan_ports(self, request):
        if request.method == 'GET':
            target_address = request.query_params.get('address')
        elif request.method == 'POST':
            serializer = PortScannerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            target_address = serializer.validated_data['address']
        else:
            return Response({'error': 'Method not allowed'}, status=405)

        open_ports = []

        try:
            if target_address:
                threads = []
                for port in range(1, 9000):  # Scan ports 1 to 1024 concurrently
                    thread = threading.Thread(target=self.scan_port, args=(target_address, port, open_ports))
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

                return Response({'target_address': target_address, 'open_ports': open_ports})
        except socket.error as e:
            return Response({'error': f"Error: {e}"}, status=500)

        return Response({'error': 'Please provide a valid address'}, status=400)
