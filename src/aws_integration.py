import subprocess
import exceptions as system_exceptions
class AWSConnection:
    def __init__(self, aws_profile_name: str, aws_service_type: str):
        # Check if AWS ia already connected
        try:
            subprocess.run(["aws", "sts", "get-caller-identity"], check=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.STDOUT)
            return
        except subprocess.CalledProcessError as err:
            pass

        # Connect to AWS account
        try:
            if aws_profile_name:
                # Run the AWS CLI SSO login command
                subprocess.run(["aws", "sso", "login", "--profile", aws_profile_name], check=True)
            else:
                subprocess.run(["aws", "sso", "login"], check=True)
        except subprocess.CalledProcessError as err:
            raise system_exceptions.AWSConnectionFailed(message=err)
