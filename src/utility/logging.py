import logging

class Logger:
    
    @staticmethod
    def create_logger():
        # create logger
        logging.basicConfig(filename='skincli.log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logger = logging.getLogger('skincli')
        logger.debug("created log")

    @staticmethod 
    def debug(data):
        logger = logging.getLogger('skincli')
        logger.debug(data)