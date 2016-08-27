import sys, re, os, subprocess #,signal

def startargs ():
	RE = ['Robot1', 'Robot2', 'firefox', 'iexplore'] #chrome, javaws
	argv = sys.argv
	del argv[0]
	if len(argv) >= 1:
		opts = {'-c':'chrome', '-j':'javaws', '-w':'winvnc'}
		if len(argv[0]) == 2 and argv[0] in opts.keys():
			argv += [ opts[argv[0]] ]
			del argv[0]
		elif argv[0].lower() == '-re':
			return argv[1]
	RE += argv
	argv = '^('+ '|'.join(RE) +')\..+$'
	return argv

def help ():
	if len(sys.argv) > 1 and sys.argv[1].lower() == 'help':
		print '\t[ -c ; -j ; -w ; abc xyz tgb ; -re ExpReg ]'
		exit(0)

def tasklist (pname):
	task_list = []
	tmp = os.popen('tasklist').readlines()
	for line in tmp[3:]:
		name = line[:25]
		pid  = extract_pid( line[26:34] )
		mem = int( extract_pid( line[64:70] +line[71:-3] ) )
		#apid = extract_pid( line[64:70] +line[71:-3] )
		if is_pname(pname, name):
			task_list += [(name, pid, mem)]
	return task_list

def extract (patern, data):
	r = re.compile(patern, re.IGNORECASE )
	res = list( r.finditer(data) )
	if len(res):
		return res[0].group()
	return None

def is_pname (patern, data):
	# patern = '%s' %(pname)
	if extract(patern, data) != None:
		return True
	return False

def extract_pid (data):
	patern = '(\d+)'
	return extract(patern, data)

def kill_list (task_list):
	global pname, smemo
	if len(task_list):
		for name, pid, mem in task_list:
			smemo += mem
			print '\n%s pid: %s use %s Kb' %(name, pid, mem/1000)
			print os.popen( 'Taskkill /PID %s /F' %(pid) ).read()
	else:
		print 'NOT FOUND PROCESS WITH REXP: %s' %pname

def QueryUser (pname):
	args = [r'C:\Windows\System32\query.exe', 'user'] #C:\Windows\Sysnative\query.exe
	process = subprocess.Popen(args, stdout=subprocess.PIPE)
	output, err = process.communicate()
	userlist = []
	for line in output.strip().split('\n')[1:]:
		usr = line[:23]
		pid = extract_pid(line[43:46])
		if not is_pname(pname, usr):
			userlist += [(usr, pid)]
	return userlist

def Logoff (userlist):
	for usr, pid in userlist:
		if not is_pname(pname, usr):
			args = [r'C:\Windows\System32\logoff.exe', str(pid)] #C:\Windows\Sysnative\logoff.exe
			process = subprocess.Popen(args, stdout=subprocess.PIPE)
			output, err = process.communicate()
			print output, err

help()
print '\n\n##########################\n#   Start Blade Runner   #\n##########################\n'
pname = startargs() #'(Robo2|TesteServico|firefox|iexplore|javaws)' #chrome|javaws
uname = '(userName)'
smemo = 0

print 'Get & Filter TaskList ::\n'
task_list = tasklist(pname)
print 'Kill TaskList ::\n'
kill_list(task_list)
print 'Get & Filter UserList ::\n'
userlist = QueryUser(uname)
print 'Kill UserList ::\n'
Logoff(userlist)
print '##########################\n# Total %s\t\t #\n# Use %s Kb\t\t #\n##########################\n' % (str(len(task_list)), smemo/1000)