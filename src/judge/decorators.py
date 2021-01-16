from django.conf import settings
import logging
import os


def limit_permisions(func):
    '''
    decorator for limitting access to directories
    '''

    def wrapper(*args, **kwargs):
        # Check if docker secrets are used and if so make them readable to only
        # root user.

        if(os.path.exists("/run/secrets")): 
            os.system("chmod -R 500 /run/secrets")

        # Limiting max process that can be spawned by a user to 100 to protect against 
        # fork bombs. Also, switching the user to 'judge' to run the submitted program.
        # After the allocated time limit, all process spawned by 'judge' user is killed.

        os.system('ulimit -u 100; su judge -c "')


        # Change permission to allow only root user to be
        # able to execute commands in the directory.
        os.system("chmod 100 .")

        # enable media root with execution files
        os.system('chmod 777 ' + settings.MEDIA_ROOT)

        func(*args, **kwargs)

        # kill all process spawned by user 'judge'
        os.system("pkill -u judge")

        # Make directly readable / executable again.
        os.system(f"chmod 777 {settings.BASE_DIR}")
    
    return wrapper