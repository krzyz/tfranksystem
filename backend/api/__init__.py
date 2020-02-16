import os
if os.environ.get('STAGE') is None:
    raise Exception('STAGE environment variable is not set!')