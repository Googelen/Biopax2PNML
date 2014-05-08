import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# create file handler
fh = logging.FileHandler('biopax2pnml.log')
fh.setLevel(logging.INFO)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.WARN)

# display time and thread name in log entries
formatter = logging.Formatter('%(asctime)s: %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

log.addHandler(ch)
log.addHandler(fh)