from config import *

from subprocess import call

DASH_SERVER = raw_input("What's the URL of your dash server ? ")
link_redis = None

print("The name of your dash app is: "+DASH_APP_NAME)

print("Your dash server is: "+DASH_SERVER)

TRACKED_REPO = DASH_SERVER.replace('.', '-')+'-'+DASH_APP_NAME.replace('.', '-')
print("The tracked repo is: "+TRACKED_REPO)

# Change number of workers if needed
while True:
	link_celery = raw_input("Do you need to change the number of workers for your app? (Yes/No): ")
	if link_celery.lower() == "yes":
		workers = raw_input("How many workers does your app need? ")
		print('Running: ssh dokku@'+DASH_SERVER+' ps:scale '+DASH_APP_NAME+' worker='+workers)
		ps_scale_code = call(['ssh', 'dokku@'+DASH_SERVER, 'ps:scale', DASH_APP_NAME, 'worker='+workers])
		if ps_scale_code == 0:
			print(DASH_APP_NAME+' was scaled to '+workers+' workers')
			link_redis = "yes"
			break
		else:
			exit()
	if link_celery.lower() == "no":
		print("Not changing the number of workers...")
		break

# Link to redis if needed
while True:
	if link_redis not in ["yes", "no"]:	
		link_redis = raw_input("Do you need a Redis instance for your app? (Yes/No): ").lower()
	if link_redis == "yes":
		while True:
			existing_redis = raw_input("Do you want to link an existing Redis instance? (Yes/No): ")
			if existing_redis.lower() == "yes":
				redis_service = raw_input("Please type the name of the existing Redis Service you want to link: ")
				break
			if existing_redis.lower() == "no":
				redis_service = raw_input("Please type the name of the new Redis Service you want to link: ")
				print('Running: ssh dokku@'+DASH_SERVER+' redis:create '+redis_service)
				redis_create_code = call(['ssh', 'dokku@'+DASH_SERVER, 'redis:create', redis_service])
				if redis_create_code == 0:
					print('Redis service '+redis_service+' was created')
					break
				else:
					exit()
		print('Running: ssh dokku@'+DASH_SERVER+' redis:link '+redis_service+' '+DASH_APP_NAME)
		redis_link_code = call(['ssh', 'dokku@'+DASH_SERVER, 'redis:link', redis_service, DASH_APP_NAME])
		if redis_link_code in [0, 1]:
			print('Redis service '+redis_service+' was linked to dash app '+DASH_APP_NAME)
			break
		else:
			exit()
	if link_redis == "no":
		print("Not linking Redis...")
		break

# Git remote add tracked-repo
print('Running: git remote add '+TRACKED_REPO+' dokku@'+DASH_SERVER+':'+DASH_APP_NAME)
git_remote_add_code = call(['git', 'remote', 'add', TRACKED_REPO, 'dokku@'+DASH_SERVER+':'+DASH_APP_NAME])
if git_remote_add_code == 0:
	print('New remote tracked repo added, carrying on...')
elif git_remote_add_code == 128:
	print('Remote tracked repo exists already, carrying on using it...')
else:
	exit()

# Git add
while True:
	git_add = raw_input("Do you want to add all your changes to git? (Yes/No): ")
	if git_add.lower() == "yes":
		while True:
			call(['git', 'status'])
			git_status = raw_input("These are the changes that are gonna be added, you wanna continue? (Yes/No): ").lower()
			if git_status == "yes":
				print('Running: git add .')
				git_add_code = call(['git', 'add', '.'])
				if git_add_code == 0:
					print('Changes staged with git')
					break
				else:
					exit()
			if git_status == "no":
				print("Exiting...")
				exit()
		break
	if git_add.lower() == "no":
		print("Exiting...")
		exit()

# Git commit
git_commit_message = raw_input("Enter a message for your commit: ")
print('Running: git commit -m "'+git_commit_message+'"')
git_commit_code = call(['git', 'commit', '-m', '"'+git_commit_message+'"'])
if git_commit_code == 0:
	print('Changes commited with git')
else:
	exit()

# Git push
while True:
	deploy = raw_input("Are you on the branch master? (Yes/No): ").lower()
	if deploy == "yes":
		print('Running: git push '+TRACKED_REPO+' master')
		git_push_code = call(['git', 'push', TRACKED_REPO, 'master'])
		if git_push_code == 0:
			print('Your app was deployed successfully')
			break
		else:
			exit()
	if deploy == "no":
		git_branch = raw_input("Enter the name of your branch: ")
		print('Running: git push '+TRACKED_REPO+' '+git_branch+':master')
		git_push_code = call(['git', 'push', TRACKED_REPO, git_branch+':master'])
		if git_push_code == 0:
			print('Your app was deployed successfully')
			break
		else:
			exit()

print('Done.')