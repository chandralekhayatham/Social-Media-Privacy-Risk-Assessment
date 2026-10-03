import csv, random
from pathlib import Path
random.seed(42)
OUT=Path(__file__).resolve().parent/'social_media_privacy_assessments.csv'
fields=['profile_id','profile_visibility','phone_public','email_public','birthday_public','location_public','workplace_public','education_public','relationship_public','posts_public','location_tagging','travel_posts','unknown_connections','tag_review_enabled','third_party_apps_reviewed','mfa_enabled','login_alerts_enabled','password_reuse_reported','suspicious_link_awareness','old_posts_reviewed','privacy_settings_reviewed','risk_score','risk_level']
def risk(row):
    pts=0
    for k,w in [('profile_visibility',8),('phone_public',8),('email_public',4),('birthday_public',5),('location_public',10),('workplace_public',4),('education_public',3),('relationship_public',3),('posts_public',6),('location_tagging',7),('travel_posts',7),('unknown_connections',7),('tag_review_enabled',-4),('third_party_apps_reviewed',-4),('mfa_enabled',-7),('login_alerts_enabled',-3),('password_reuse_reported',7),('suspicious_link_awareness',-3),('old_posts_reviewed',-3),('privacy_settings_reviewed',-3)]:
        v=row[k]; yes=v in ('PUBLIC','YES','OFTEN','NO') if k in ['tag_review_enabled','third_party_apps_reviewed','mfa_enabled','login_alerts_enabled','old_posts_reviewed','privacy_settings_reviewed','suspicious_link_awareness'] else v in ('PUBLIC','YES','OFTEN')
        if yes: pts += w
    pts=max(0,min(100,pts)); return pts, 'LOW' if pts<=20 else 'MODERATE' if pts<=40 else 'HIGH' if pts<=70 else 'CRITICAL'
rows=[]
for i in range(1,1001):
    r={'profile_id':f'DEMO-{i:04d}'}
    r.update({k:random.choice(['PUBLIC','FRIENDS','PRIVATE']) for k in ['profile_visibility']})
    for k in ['phone_public','email_public','birthday_public','location_public','workplace_public','education_public','relationship_public','posts_public','location_tagging','travel_posts'] : r[k]=random.choice(['YES','NO'])
    r['unknown_connections']=random.choice(['OFTEN','SOMETIMES','NO']); r['tag_review_enabled']=random.choice(['YES','NO']); r['third_party_apps_reviewed']=random.choice(['YES','NO']); r['mfa_enabled']=random.choice(['YES','NO']); r['login_alerts_enabled']=random.choice(['YES','NO']); r['password_reuse_reported']=random.choice(['YES','NO']); r['suspicious_link_awareness']=random.choice(['YES','NO']); r['old_posts_reviewed']=random.choice(['YES','NO']); r['privacy_settings_reviewed']=random.choice(['YES','NO']); r['risk_score'],r['risk_level']=risk(r); rows.append(r)
with OUT.open('w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print(f'Generated {len(rows)} synthetic records at {OUT}')
