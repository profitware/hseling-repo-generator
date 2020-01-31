import os
from base64 import b64decode, b64encode
from flask import Flask, jsonify, request
from logging import getLogger


from jsonrpc.backend.flask import api
from jsonrpc.exceptions import JSONRPCDispatchException


from hseling_api_generator import boilerplate

from hseling_lib_generator.process import process_data
from hseling_lib_generator.query import query_data


app = Flask(__name__)
app.config['DEBUG'] = False
app.config['LOG_DIR'] = '/tmp/'
app.config.from_envvar('HSELING_API_GENERATOR_SETTINGS')


if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'hseling_api_generator.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

log = getLogger(__name__)

app.register_blueprint(api.as_blueprint(), url_prefix="/rpc")


ALLOWED_EXTENSIONS = ['txt']


def do_process_task(file_ids_list):
    files_to_process = boilerplate.list_files(recursive=True,
                                              prefix=boilerplate.UPLOAD_PREFIX)
    if file_ids_list:
        files_to_process = [boilerplate.UPLOAD_PREFIX + file_id
                            for file_id in file_ids_list
                            if (boilerplate.UPLOAD_PREFIX + file_id)
                            in files_to_process]
    data_to_process = {file_id[len(boilerplate.UPLOAD_PREFIX):]:
                       boilerplate.get_file(file_id)
                       for file_id in files_to_process}
    processed_file_ids = list()
    for processed_file_id, contents in process_data(data_to_process):
        processed_file_ids.append(
            boilerplate.add_processed_file(
                processed_file_id,
                contents,
                extension='txt'
            ))
    return processed_file_ids

@app.route('/healthz')
def healthz():
    app.logger.info('Health checked')
    return jsonify({"status": "ok", "message": "Application Generator"})



@api.dispatcher.add_method
def upload_file(file_name, file_contents_base64):
    if not file_name:
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NO_SELECTED_FILE_CODE, message=boilerplate.ERROR_NO_SELECTED_FILE)
    if not file_contents_base64:
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NO_FILE_PART_CODE, message=boilerplate.ERROR_NO_FILE_PART)
    if not boilerplate.allowed_file(file_name, allowed_extensions=ALLOWED_EXTENSIONS):
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NOT_ALLOWED_CODE, message=boilerplate.ERROR_NOT_ALLOWED)
    try:
        file_contents = b64decode(file_contents_base64)
        file_size = len(file_contents)
    except TypeError:
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NO_FILE_PART_CODE, message=boilerplate.ERROR_NO_FILE_PART)
    return boilerplate.save_file_simple(file_name, file_contents, file_size)



@api.dispatcher.add_method
def get_file(file_id):
    if file_id not in boilerplate.list_files(recursive=True):
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NO_SUCH_FILE_CODE, message=boilerplate.ERROR_NO_SUCH_FILE)
    file_contents_base64 = None
    try:
        file_contents_base64 = b64encode(boilerplate.get_file(file_id)).decode("utf-8")
    except TypeError:
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NO_FILE_PART_CODE, message=boilerplate.ERROR_NO_FILE_PART)
    return {"file_id": file_id,
            "file_contents_base64": file_contents_base64}



@api.dispatcher.add_method
def list_files():
    return {'file_ids': boilerplate.list_files(recursive=True)}

def do_process(file_ids):
    file_ids_list = file_ids and file_ids.split(",")
    result = do_process_task(file_ids_list)
    return {"result": result}



@api.dispatcher.add_method
def process_files(file_ids):
    if not file_ids:
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NO_FILE_PART_CODE, message=boilerplate.ERROR_NO_FILE_PART)
    if isinstance(file_ids, list):
        file_ids = ",".join(file_ids)
    return do_process(file_ids)


def do_query(file_id, query_type):
    if not query_type:
        return {"error": boilerplate.ERROR_NO_QUERY_TYPE_SPECIFIED}
    processed_file_id = boilerplate.PROCESSED_PREFIX + file_id
    if processed_file_id in boilerplate.list_files(recursive=True):
        return {
            "result": query_data({
                processed_file_id: boilerplate.get_file(processed_file_id)
            }, query_type=query_type)
        }
    return {"error": boilerplate.ERROR_NO_SUCH_FILE}



@api.dispatcher.add_method
def query_file(file_id, query_type):
    result = do_query(file_id, query_type)
    if result.get("error") == boilerplate.ERROR_NO_QUERY_TYPE_SPECIFIED:
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NO_QUERY_TYPE_SPECIFIED_CODE, message=result.get("error"))
    elif result.get("error") == boilerplate.ERROR_NO_SUCH_FILE:
        raise JSONRPCDispatchException(code=boilerplate.ERROR_NO_SUCH_FILE_CODE, message=result.get("error"))
    return result



@api.dispatcher.add_method
def get_task_status(task_id):
    return boilerplate.get_task_status(task_id)





if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)


__all__ = [app]
