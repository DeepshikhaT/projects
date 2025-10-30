#!/usr/bin/env python3
"""
Network Monitoring Script
Purpose: Real-time monitoring of network devices
Author: Deepshikha Tripathi
"""

import netmiko
from netmiko import ConnectHandler
import time
import json
from datetime import datetime
import argparse
import yaml

class NetworkMonitor:
    """Network device monitoring class"""

    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.devices = self.load_inventory()

    def load_inventory(self):
        """Load devices from inventory file"""
        devices = []
        # Parse inventory file (simplified)
        # In production, use ansible-inventory command
        return devices

    def check_device_health(self, device_info):
        """
        Check health of a single device

        Args:
            device_info: Dictionary containing device connection information

        Returns:
            Dictionary with health status
        """
        try:
            # Connect to device
            connection = ConnectHandler(**device_info)

            # Get interface status
            interfaces_output = connection.send_command(
                'show ip interface brief',
                use_textfsm=True
            )

            # Parse interface data
            total_interfaces = len(interfaces_output)
            up_interfaces = sum(1 for iface in interfaces_output
                              if iface.get('status', '').lower() == 'up')

            # Get CPU usage
            cpu_output = connection.send_command('show processes cpu | include CPU')
            cpu_usage = self.parse_cpu_usage(cpu_output)

            # Get memory usage
            memory_output = connection.send_command('show memory statistics')
            memory_usage = self.parse_memory_usage(memory_output)

            # Get uptime
            version_output = connection.send_command('show version')
            uptime = self.extract_uptime(version_output)

            connection.disconnect()

            return {
                'device': device_info['host'],
                'status': 'healthy',
                'reachable': True,
                'timestamp': datetime.now().isoformat(),
                'interfaces': {
                    'total': total_interfaces,
                    'up': up_interfaces,
                    'down': total_interfaces - up_interfaces
                },
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'uptime': uptime
            }

        except Exception as e:
            return {
                'device': device_info['host'],
                'status': 'unreachable',
                'reachable': False,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }

    def parse_cpu_usage(self, cpu_output):
        """Parse CPU usage from show command output"""
        try:
            # Example: "CPU utilization for five seconds: 5%/0%"
            if '5%' in cpu_output or 'five seconds' in cpu_output:
                parts = cpu_output.split(':')
                if len(parts) > 1:
                    cpu_part = parts[1].split('/')[0].strip().replace('%', '')
                    return float(cpu_part)
        except:
            pass
        return 0.0

    def parse_memory_usage(self, memory_output):
        """Parse memory usage from show command output"""
        try:
            # Parse memory statistics
            # This is simplified - actual parsing depends on device output format
            return {
                'total': '1000000',
                'used': '500000',
                'free': '500000',
                'percent_used': 50.0
            }
        except:
            return {}

    def extract_uptime(self, version_output):
        """Extract uptime from show version output"""
        try:
            for line in version_output.split('\n'):
                if 'uptime is' in line.lower():
                    return line.strip()
        except:
            pass
        return 'Unknown'

    def monitor_all_devices(self):
        """Monitor all devices in inventory"""
        results = []

        print("="*60)
        print(" "*15 + "NETWORK MONITORING")
        print("="*60)
        print(f"\nMonitoring started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total devices: {len(self.devices)}\n")

        for device in self.devices:
            print(f"Checking {device['host']}...", end=' ')
            result = self.check_device_health(device)
            results.append(result)

            if result['reachable']:
                status_symbol = "✓"
                status_text = "OK"
            else:
                status_symbol = "✗"
                status_text = "FAILED"

            print(f"{status_symbol} {status_text}")

        return results

    def generate_report(self, results):
        """Generate monitoring report"""
        print("\n" + "="*60)
        print(" "*20 + "SUMMARY REPORT")
        print("="*60 + "\n")

        total = len(results)
        reachable = sum(1 for r in results if r['reachable'])
        unreachable = total - reachable

        print(f"Total Devices:      {total}")
        print(f"Reachable:          {reachable} ({(reachable/total*100):.1f}%)")
        print(f"Unreachable:        {unreachable} ({(unreachable/total*100):.1f}%)")
        print("\n" + "-"*60 + "\n")

        print("Device Details:")
        print(f"{'Device':<20} {'Status':<12} {'CPU %':<10} {'Interfaces Up':<15}")
        print("-"*60)

        for result in results:
            device = result['device']
            status = "REACHABLE" if result['reachable'] else "UNREACHABLE"
            cpu = f"{result.get('cpu_usage', 0):.1f}%" if result['reachable'] else "N/A"
            interfaces = f"{result['interfaces']['up']}/{result['interfaces']['total']}" if result['reachable'] else "N/A"

            print(f"{device:<20} {status:<12} {cpu:<10} {interfaces:<15}")

        print("\n" + "="*60 + "\n")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Network Device Monitor')
    parser.add_argument('--inventory', '-i',
                       default='../inventory/lab/hosts',
                       help='Inventory file path')
    parser.add_argument('--continuous', '-c',
                       action='store_true',
                       help='Run continuously')
    parser.add_argument('--interval', '-t',
                       type=int,
                       default=60,
                       help='Monitoring interval in seconds (default: 60)')

    args = parser.parse_args()

    # Example devices for demonstration
    example_devices = [
        {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'cisco',
            'secret': 'cisco',
        },
        {
            'device_type': 'cisco_ios',
            'host': '192.168.1.11',
            'username': 'admin',
            'password': 'cisco',
            'secret': 'cisco',
        }
    ]

    monitor = NetworkMonitor(args.inventory)
    monitor.devices = example_devices

    try:
        if args.continuous:
            print("Starting continuous monitoring (Press Ctrl+C to stop)...\n")
            while True:
                results = monitor.monitor_all_devices()
                monitor.generate_report(results)

                print(f"\nNext check in {args.interval} seconds...")
                time.sleep(args.interval)
        else:
            results = monitor.monitor_all_devices()
            monitor.generate_report(results)

            # Save results to file
            output_file = f"../reports/monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to: {output_file}")

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == '__main__':
    main()
