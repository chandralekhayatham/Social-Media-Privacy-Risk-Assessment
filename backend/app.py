from flask import Flask, jsonify, render_template, request, abort, make_response
from services.assessment_engine import QUESTIONS, CHECKLIST, assess, simulate_improvement
from services.database import init_db, save_assessment, get_assessment, stats
from datetime import datetime

app=Flask(__name__,template_folder='../frontend',static_folder='../frontend',static_url_path='/static')
init_db()

@app.get('/')
def home(): return render_template('index.html', questions=QUESTIONS)

@app.post('/api/assessment')
def create_assessment():
    data=request.get_json(silent=True) or {}
    answers=data.get('answers')
    if not isinstance(answers,dict): return jsonify({'error':'answers must be an object'}),400
    result=assess(answers); aid=save_assessment(result); result['assessment_id']=aid
    return jsonify(result)

@app.get('/api/assessment/<int:aid>')
def assessment(aid):
    row=get_assessment(aid)
    if not row: abort(404)
    return jsonify(row)

@app.get('/api/assessment/<int:aid>/recommendations')
def recommendations(aid):
    row=get_assessment(aid)
    if not row: abort(404)
    from services.assessment_engine import generate_recommendations
    # recommendations are derived from stored finding types/descriptions; no sensitive inputs are needed.
    findings=[{'finding_type':f['finding_type'],'severity':f['severity'],'recommendation':f['description']} for f in row['findings']]
    return jsonify({'assessment_id':aid,'recommendations':findings})

@app.post('/api/assessment/simulate-improvement')
def improvement():
    data=request.get_json(silent=True) or {}
    answers=data.get('answers',{}); changes=data.get('changes',{})
    if not isinstance(answers,dict) or not isinstance(changes,dict): return jsonify({'error':'answers and changes must be objects'}),400
    return jsonify(simulate_improvement(answers,changes))

@app.get('/api/dashboard/stats')
def dashboard_stats(): return jsonify(stats())

@app.get('/api/privacy-checklist')
def checklist(): return jsonify({'checklist':CHECKLIST})

@app.get('/api/report/<int:aid>')
def report(aid):
    row=get_assessment(aid)
    if not row: abort(404)
    html=render_template('report.html', row=row, generated=datetime.now().strftime('%Y-%m-%d %H:%M'))
    resp=make_response(html); resp.headers['Content-Type']='text/html; charset=utf-8'; return resp

@app.get('/dashboard')
def dashboard(): return render_template('dashboard.html')

if __name__=='__main__': app.run(host='127.0.0.1',port=5000,debug=False)
