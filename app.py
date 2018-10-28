# encoding:utf-8
from flask import Flask
from flask import request,render_template,jsonify
from plugins.whatweb import Whatweb
from flask_apscheduler import APScheduler
from flask import url_for
from flask import abort
job_list = []
app = Flask(__name__)
aps_scheduler = APScheduler()

def jobfromparm(**jobargs):
    id = jobargs['id']
    func = jobargs['func']
    args = eval(jobargs['args'])
    trigger = jobargs['trigger']
    seconds = jobargs['seconds']
    print('add job: ',id)
    job = aps_scheduler.add_job(func=func, id=id, args=args, trigger=trigger, seconds=seconds)
    return 'Success!'


def job2(target):
    print target


@app.route('/pause')
def pause():
    aps_scheduler.pause_job('job1')
    return "Success!"


@app.route('/resume')
def resume():
    aps_scheduler.resume_job('job1')
    return "Success!"


@app.route('/')
def fast():
    return render_template('whatweb.html')


@app.route('/api',methods=['GET'])
def api():
    query = request.args.get('query', '')
    web_api = Whatweb()
    return jsonify(web_api.api(query))


@app.route('/add',methods=['GET'])
def add():
    web = Whatweb()
    target = request.args.get('target', '')
    # time = datetime.datetime.now() + datetime.timedelta(seconds=3)
    if target == '':
        return abort(403)
    # job_id = uuid.uuid4().hex
    # job_list.append(job_id)
    # aps_scheduler.add_job(id=job_id, func=web.run, trigger='date', args=(target,), next_run_time=time)
    # app.logger.debug(aps_scheduler.get_jobs())
    return jsonify(web.add(aps_scheduler,target))


@app.route('/jobs',methods=['GET'])
def jobs():
    app.logger.debug(aps_scheduler.get_jobs())
    return render_template('jobs.html', jobs=aps_scheduler.get_jobs())


if __name__ == '__main__':
    aps_scheduler.init_app(app)
    aps_scheduler.start()
    app.run()
