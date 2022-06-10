from flask import Flask, request
import json
import os
import shutil
import threading
mutex = threading.Lock()

app = Flask(__name__)


@app.route('/')
def home():
    return "App Works!!!"


@app.route('/api/runtests/<filename>')
def runtests(filename):
    mutex.acquire()
    expected_success = [5, 5, 5, 5, 5]

    #filename = escape(filename)
    filename_without_extension = str(filename).replace(".tar.gz", "")
    extract_path = f'../participant-files/{filename_without_extension}'

    shutil.unpack_archive(f'../participant-files/{filename}', extract_path)
    shutil.copytree('../func-contest-files/', f'{extract_path}/func-contest-files')

    result_string = ''

    for i in range(1, 6):
        shutil.copy2(f'{extract_path}/{i}.fc', f'{extract_path}/func-contest-files/task-{i}/fc/')
        os.chdir(f'{extract_path}/func-contest-files/task-{i}/')

        test_result = os.popen('toncli run_tests').read()
        how_many = test_result.count('SUCCESS')
        result_string = result_string+f'{i}. {how_many}/{expected_success[i-1]} \n'

        os.chdir('../../../../api')

    shutil.rmtree(extract_path)

    mutex.release()
    return (result_string)
