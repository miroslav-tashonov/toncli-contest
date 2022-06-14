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
    result_string = ''
    try:
        task_names = ['Greatest common divisor', 'Message validation', '(De)Serialize to Cell', 'Merge hashmaps', 'Address encoder']
        #filename = escape(filename)
        filename_without_extension = str(filename).replace(".tar.gz", "")
        extract_path = f'../participant-files/{filename_without_extension}'

        exist = os.path.exists(extract_path)
        if not exist:
            os.makedirs(extract_path)

        shutil.copytree('../func-contest-files/', f'{extract_path}/func-contest-files')
        shutil.unpack_archive(f'../participant-files/{filename}', f'{extract_path}/func-contest-files/func')

        os.chdir(f'{extract_path}/func-contest-files')
        for i in range(1, 6):
            test_result = os.popen(f'toncli run_tests -c contest-{i}').read()
            index = test_result.find('Test result:')
            score = test_result[index+20:index+24]
            score = score.replace("]","")
            score = score.replace(" ","")
            result_string += f'TASK {i} - {task_names[i-1]} score is : {score}/100 \n'
        
        os.chdir('../../../api')

        shutil.rmtree(extract_path)

        mutex.release()
    except BaseException as err:
        mutex.release()
        if(os.getcwd().find('api') == -1):
            os.chdir('../../../api')
        result_string = err

    return (result_string)
