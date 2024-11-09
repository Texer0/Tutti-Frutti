import subprocess
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
# subprocess.run(['start', 'cmd', '/K', 'python', os.path.join(script_directory, current_file)], shell=True)

subprocess.run(['start', 'cmd','/K', 'python', f'{script_directory}\Servidor.py'], shell=True)
subprocess.run(['start', 'cmd','/K', 'python', f'{script_directory}\Cliente.py'], shell=True)