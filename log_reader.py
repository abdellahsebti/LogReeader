import os
import re
import subprocess
import platform
import json
from datetime import datetime

class LogReader:
    def __init__(self):
        self.system = platform.system()
        print(f"🔍 Detected OS: {self.system}")
    
    def read_logs(self, max_logs=100):
        """Read logs based on operating system"""
        if self.system == "Windows":
            return self.read_windows_logs(max_logs)
        elif self.system == "Linux":
            return self.read_linux_logs(max_logs)
        else:
            print(f"⚠️  Unsupported OS: {self.system}")
            return self.get_sample_logs()
    
    def read_windows_logs(self, max_logs=100):
        """Read Windows Event Logs - Multiple methods for reliability"""
        
        # METHOD 1: Try Security Events (Logon events)
        print("📁 Attempting to read Windows Security logs...")
        logs = self._read_security_events(max_logs)
        
        if logs and len(logs) > 0:
            print(f"✅ Successfully loaded {len(logs)} Security events")
            return logs
        
        # METHOD 2: Try System Events (more accessible)
        print("📁 Security logs inaccessible, trying System logs...")
        logs = self._read_system_events(max_logs)
        
        if logs and len(logs) > 0:
            print(f"✅ Successfully loaded {len(logs)} System events")
            return logs
        
        # METHOD 3: Fallback to sample data
        print("⚠️  Could not access Windows Event Logs. Using sample data.")
        print("💡 Tip: Run PowerShell as Administrator to enable log access")
        return self.get_sample_logs()
    
    def _read_security_events(self, max_logs=100):
        """Read Security Event Log (Logon events)"""
        try:
            # PowerShell command - more compatible format
            ps_command = '''
            $events = Get-WinEvent -FilterHashtable @{LogName='Security';Id=4624,4625,4672} -MaxEvents $MAX | 
            ForEach-Object {
                [PSCustomObject]@{
                    TimeCreated = $_.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss')
                    Id = $_.Id
                    Message = $_.Message -replace "`r`n", " "
                }
            }
            $events | ConvertTo-Json -Compress -Depth 3
            '''.replace('$MAX', str(max_logs))
            
            result = subprocess.run(
                ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0 and result.stdout.strip():
                events = json.loads(result.stdout)
                return self._parse_windows_events(events, 'Security')
        
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parse error: {e}")
        except subprocess.TimeoutExpired:
            print("⚠️  PowerShell command timed out")
        except Exception as e:
            print(f"⚠️  Security log error: {e}")
        
        return []
    
    def _read_system_events(self, max_logs=100):
        """Read System Event Log (more accessible)"""
        try:
            ps_command = '''
            $events = Get-WinEvent -FilterHashtable @{LogName='System';Level=1,2,3} -MaxEvents $MAX | 
            ForEach-Object {
                [PSCustomObject]@{
                    TimeCreated = $_.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss')
                    Id = $_.Id
                    Message = $_.Message -replace "`r`n", " "
                    Source = $_.Source
                }
            }
            $events | ConvertTo-Json -Compress -Depth 3
            '''.replace('$MAX', str(max_logs))
            
            result = subprocess.run(
                ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0 and result.stdout.strip():
                events = json.loads(result.stdout)
                return self._parse_windows_events(events, 'System')
        
        except Exception as e:
            print(f"⚠️  System log error: {e}")
        
        return []
    
    def _parse_windows_events(self, events, log_type):
        """Parse Windows event data into standardized format"""
        logs = []
        
        if isinstance(events, dict):
            events = [events]
        
        for event in events:
            try:
                event_id = event.get('Id', 0)
                time_created = event.get('TimeCreated', 'Unknown')
                message = event.get('Message', '')[:200]  # Truncate long messages
                source = event.get('Source', log_type)
                
                # Determine if suspicious based on event ID
                suspicion = 0
                if event_id in [4625, 4771, 4776]:  # Failed logon events
                    suspicion = 1
                elif event_id in [1102, 1100]:  # Log cleared events
                    suspicion = 1
                
                logs.append({
                    'timestamp': time_created,
                    'hostname': os.environ.get('COMPUTERNAME', 'unknown'),
                    'service': f'{log_type}(ID:{event_id})',
                    'message': message,
                    'source': 'windows',
                    'event_id': event_id
                })
            except Exception as e:
                print(f"⚠️  Error parsing event: {e}")
                continue
        
        return logs
    
    def read_linux_logs(self, max_logs=100):
        """Read Linux authentication logs"""
        log_paths = ['/var/log/auth.log', '/var/log/secure', '/var/log/syslog']
        
        for log_path in log_paths:
            if os.path.exists(log_path):
                try:
                    logs = []
                    pattern = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+):\s+(.*)'
                    
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            match = re.match(pattern, line)
                            if match:
                                logs.append({
                                    'timestamp': match.group(1),
                                    'hostname': match.group(2),
                                    'service': match.group(3),
                                    'message': match.group(4),
                                    'source': 'linux'
                                })
                    
                    return logs[-max_logs:]
                except Exception as e:
                    print(f"⚠️  Error reading {log_path}: {e}")
        
        return self.get_sample_logs()
    
    def get_sample_logs(self):
        """Sample logs for testing"""
        return [
            {'timestamp': '2024-01-15 10:23:45', 'hostname': 'DESKTOP-PC', 'service': 'Security(ID:4624)', 
             'message': 'An account was successfully logged in. Account Name: admin', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:24:12', 'hostname': 'DESKTOP-PC', 'service': 'Security(ID:4624)', 
             'message': 'An account was successfully logged in. Account Name: user1', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:25:33', 'hostname': 'DESKTOP-PC', 'service': 'Security(ID:4625)', 
             'message': 'An account failed to log on. Account Name: administrator', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:26:01', 'hostname': 'DESKTOP-PC', 'service': 'Security(ID:4625)', 
             'message': 'An account failed to log on. Account Name: root', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:26:15', 'hostname': 'DESKTOP-PC', 'service': 'Security(ID:4625)', 
             'message': 'An account failed to log on. Account Name: admin', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:27:00', 'hostname': 'DESKTOP-PC', 'service': 'Security(ID:4624)', 
             'message': 'An account was successfully logged in. Account Name: admin', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:28:30', 'hostname': 'DESKTOP-PC', 'service': 'System(ID:7036)', 
             'message': 'The Windows Update service entered the running state', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:30:00', 'hostname': 'DESKTOP-PC', 'service': 'Security(ID:4776)', 
             'message': 'The domain controller attempted to validate credentials', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:31:00', 'hostname': 'DESKTOP-PC', 'service': 'System(ID:6005)', 
             'message': 'The Event log service was started', 'source': 'sample'},
            {'timestamp': '2024-01-15 10:32:00', 'hostname': 'DESKTOP-PC', 'service': 'System(ID:6006)', 
             'message': 'The Event log service was stopped', 'source': 'sample'},
        ]