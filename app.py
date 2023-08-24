import chardet
from flask import Flask, request, render_template
import logging
from request import scan_query

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


app = Flask(__name__)


def detect_file_encoding(file_bytes):
    return chardet.detect(file_bytes)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    import re

    sys_event_match = re.compile(
        '==== System EventLog ====[\s\S]+?==== Application EventLog ====')
    app_event_match = re.compile(
        '==== Application EventLog ====[\s\S]+?==== End ====')

    log_file = request.files['logFile']
    # print(log_file, type(log_file))

    file_contents = log_file.read()
    # print(type(file_contents))

    encoding = detect_file_encoding(file_contents)

    decoded_text = file_contents.decode(encoding['encoding'])

    log_file.close()

    # sections of logfile
    try:
        sys_event = sys_event_match.search(decoded_text)
        app_event = app_event_match.search(decoded_text)
        if sys_event is not None or app_event is not None:

            result = scan_query(f"{sys_event} + {app_event}")

            if result is not None:
                return result

    except Exception as ex:
        return f"Error has occured while parsing log file error:{ex}"


if __name__ == '__main__':
    app.run(debug=True)
