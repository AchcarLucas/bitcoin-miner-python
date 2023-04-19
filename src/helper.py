from config import DEBUG

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def _print(title : str, content : str, ignoreDebug : bool=False):
    if(DEBUG or ignoreDebug):
        print(f"{bcolors.BOLD} {bcolors.OKCYAN} [{title}] - {bcolors.OKGREEN} {content} {bcolors.ENDC}")
    
def _empty(content : str):
    return content is None or content == ""