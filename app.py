from flask import Flask, request, render_template, redirect, url_for, jsonify, send_from_directory
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from threading import Thread
import os
import time
import uuid
import requests
from job_store import jobs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        webhook_url = request.form.get('webhook_url')

        if not url.startswith('http'):
            url = 'https://' + url

        job_id = str(uuid.uuid4())
        jobs[job_id] = 'processing'

        def background_capture(job_id, url, webhook_url):
            try:
                count = 0
                options = Options()
                options.headless = True
                service = Service('geckodriver.exe')
                driver = webdriver.Firefox(service=service, options=options)
                driver.set_window_size(1280, 720)

                driver.get(url)
                time.sleep(10)

                while True:
                    filename = f'screenshots/ss_{job_id}_{count}.png'
                    driver.save_screenshot(filename)
                    current_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
                    driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(2)
                    new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
                    if new_height == current_height:
                        break
                    count += 1

                driver.quit()
                jobs[job_id] = 'completed'

                if webhook_url:
                    try:
                        requests.post(webhook_url, json={
                            'job_id': job_id,
                            'status': 'completed',
                            'screenshots': [f"http://localhost:5000/screenshots/ss_{job_id}_{i}.png" for i in range(0, count+1)]
                        })
                    except:
                        pass
            except Exception as e:
                jobs[job_id] = 'failed'

        Thread(target=background_capture, args=(job_id, url, webhook_url)).start()
        return redirect(url_for('show_results', job_id=job_id))

    return render_template('home.html')


@app.route('/results/<job_id>')
def show_results(job_id):
    status = jobs.get(job_id, 'unknown')
    if status != 'completed':
        # Still processing or failed
        return render_template('results.html', job_id=job_id, total=0)

    # Only when completed
    total = 0
    while os.path.exists(f'screenshots/ss_{job_id}_{total}.png'):
        total += 1
    return render_template('results.html', job_id=job_id, total=total)


@app.route('/screenshots/<filename>')
def serve_screenshot(filename):
    return send_from_directory('screenshots', filename)


@app.route('/status/<job_id>')
def check_status(job_id):
    status = jobs.get(job_id)
    if status:
        return jsonify({'job_id': job_id, 'status': status})
    else:
        return jsonify({'error': 'Job ID not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
