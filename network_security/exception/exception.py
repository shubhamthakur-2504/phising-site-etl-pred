import sys
from network_security.logging import logger
def error_message_details(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in python script name [{filename}] line number [{exc_tb.tb_lineno}] error message [{str(error)}]"
    return error_message

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        logger.logging.info("Enter in exception module try block")
        a = 1/0
    except Exception as e:
        logger.logging.info("Divide by zero")
        raise NetworkSecurityException(e, sys)