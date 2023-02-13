import openai
from flask import Flask, request, render_template, redirect
import logging
from datetime import datetime

server = Flask(__name__)

def get_completion(question):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{question}\n",
            temperature=0.9,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=None
        )
    except Exception as e:

        print(e)
        return e
    return response["choices"][0].text

@server.route('/chat', methods=['GET', 'POST'])
def get_request_json():
    
    if request.method == 'POST':
        if len(request.form['question']) < 1:
            return render_template(
                'chat.html', question="null", res="问题不能为空")
        question = request.form['question']
        print("======================================")
        print("接到请求:", question)
        res = get_completion(question)
        print("问题：\n", question)
        print("答案：\n", res)
        time_now = get_time()
        logging.info(f"{time_now}|{question}|{res}")

        return render_template('chat.html', question=question, res=str(res))
    return render_template('chat.html', question=0)


def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


logging.basicConfig(filename = './record.log',level=logging.INFO)


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=80)
