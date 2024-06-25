#!/usr/bin/env python3

#!/usr/bin/env python3

#!/usr/bin/env python3

from applescript import tell

cmd = '''	
	tell application "Terminal"
		open
		do script "cd ./Desktop/project
		python3 Server.py"
		exit()
	end tell
	'''
tell.app("Terminal", cmd)