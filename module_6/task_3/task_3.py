import logging
import json


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = json.dumps(msg)
        return msg, kwargs


logger = JsonAdapter(logging.getLogger("json_log"))


if __name__ == "__main__":
    logging.basicConfig(filename=r"./skillbox_json_messages.log",
                        level=logging.DEBUG,
                        datefmt="%H:%M:%S",
                        format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
    logger.info("Started sort server")
    logger.warning("\"")
    logger.debug("12")
