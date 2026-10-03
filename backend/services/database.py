import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / 'privacy_assessment.db'

def get_conn():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    conn=get_conn(); c=conn.cursor()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS assessments(
      assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
      overall_score REAL NOT NULL,
      risk_level TEXT NOT NULL,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS category_scores(
      category_score_id INTEGER PRIMARY KEY AUTOINCREMENT,
      assessment_id INTEGER NOT NULL,
      category TEXT NOT NULL,
      score REAL NOT NULL,
      FOREIGN KEY(assessment_id) REFERENCES assessments(assessment_id)
    );
    CREATE TABLE IF NOT EXISTS findings(
      finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
      assessment_id INTEGER NOT NULL,
      category TEXT NOT NULL,
      finding_type TEXT NOT NULL,
      severity TEXT NOT NULL,
      description TEXT NOT NULL,
      FOREIGN KEY(assessment_id) REFERENCES assessments(assessment_id)
    );
    CREATE TABLE IF NOT EXISTS recommendations(
      recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
      finding_type TEXT NOT NULL,
      recommendation TEXT NOT NULL,
      priority TEXT NOT NULL
    );''')
    conn.commit(); conn.close()

def save_assessment(result):
    conn=get_conn(); c=conn.cursor()
    c.execute('INSERT INTO assessments(overall_score,risk_level) VALUES (?,?)',(result['score'],result['risk_level']))
    aid=c.lastrowid
    for cat,score in result['category_scores'].items():
        c.execute('INSERT INTO category_scores(assessment_id,category,score) VALUES (?,?,?)',(aid,cat,score))
    for f in result['findings']:
        c.execute('INSERT INTO findings(assessment_id,category,finding_type,severity,description) VALUES (?,?,?,?,?)',(aid,f['category'],f['finding_type'],f['severity'],f['description']))
    for r in result['recommendations']:
        c.execute('INSERT INTO recommendations(finding_type,recommendation,priority) VALUES (?,?,?)',(r['finding_type'],r['recommendation'],r['priority']))
    conn.commit(); conn.close(); return aid

def get_assessment(aid):
    conn=get_conn(); c=conn.cursor()
    row=c.execute('SELECT * FROM assessments WHERE assessment_id=?',(aid,)).fetchone()
    if not row: conn.close(); return None
    cats=[dict(x) for x in c.execute('SELECT category,score FROM category_scores WHERE assessment_id=?',(aid,)).fetchall()]
    findings=[dict(x) for x in c.execute('SELECT category,finding_type,severity,description FROM findings WHERE assessment_id=?',(aid,)).fetchall()]
    conn.close(); return {'assessment':dict(row),'category_scores':cats,'findings':findings}

def stats():
    conn=get_conn(); c=conn.cursor()
    total,avg=c.execute('SELECT COUNT(*),COALESCE(AVG(overall_score),0) FROM assessments').fetchone()
    levels={r['risk_level']:r['count'] for r in c.execute('SELECT risk_level,COUNT(*) count FROM assessments GROUP BY risk_level')}
    weak=[dict(r) for r in c.execute('SELECT finding_type,COUNT(*) count FROM findings GROUP BY finding_type ORDER BY count DESC LIMIT 8').fetchall()]
    recent=[dict(r) for r in c.execute('SELECT assessment_id,overall_score,risk_level,created_at FROM assessments ORDER BY assessment_id DESC LIMIT 10').fetchall()]
    conn.close(); return {'total':total,'average_score':round(avg,1),'risk_distribution':levels,'top_weaknesses':weak,'recent':recent}
