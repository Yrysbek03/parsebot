import logging

logging.basicConfig(format=u'%(filename)s   %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    # [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]
                    )
