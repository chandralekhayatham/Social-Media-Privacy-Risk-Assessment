CATEGORIES = [
    ('profile_visibility', 'Profile Exposure', 10),
    ('personal_info', 'Personal Information', 15),
    ('location', 'Location Privacy', 15),
    ('content', 'Posts & Content', 10),
    ('connections', 'Connections', 10),
    ('tagging', 'Tagging', 5),
    ('account_security', 'Account Security', 15),
    ('third_party', 'Third-Party Apps', 5),
    ('social_engineering', 'Social Engineering', 10),
    ('digital_footprint', 'Digital Footprint', 5),
]

QUESTIONS = [
# A Profile Visibility
('A1','Profile Visibility','Is your profile publicly visible?','yes_risk'),
('A2','Profile Visibility','Can search engines discover your profile?','yes_risk'),
('A3','Profile Visibility','Can non-friends see your follower/friends list?','yes_risk'),
('A4','Profile Visibility','Can non-connections view most of your profile information?','yes_risk'),
# B Personal Information
('B1','Personal Information','Is your phone number publicly visible?','yes_risk'),
('B2','Personal Information','Is your personal email publicly visible?','yes_risk'),
('B3','Personal Information','Is your full birth date publicly visible?','yes_risk'),
('B4','Personal Information','Is home-related information publicly visible?','yes_risk'),
('B5','Personal Information','Is your workplace publicly visible?','yes_risk'),
('B6','Personal Information','Is your education/college information publicly visible?','yes_risk'),
('B7','Personal Information','Are family or relationship details publicly visible?','yes_risk'),
# C Location
('C1','Location Privacy','Do you publicly share your current location?','yes_risk'),
('C2','Location Privacy','Do you use public geotagging/check-ins?','yes_risk'),
('C3','Location Privacy','Do you post travel plans before or during a trip?','yes_risk'),
('C4','Location Privacy','Do your posts reveal frequent location patterns?','yes_risk'),
('C5','Location Privacy','Could your home or work location be inferred from posts?','yes_risk'),
# D Content
('D1','Posts & Content','Are most of your posts visible to a broad audience?','yes_risk'),
('D2','Posts & Content','Do you regularly share photos with identifiable surroundings?','yes_risk'),
('D3','Posts & Content','Do your photos sometimes reveal badges, documents, or screens?','yes_risk'),
('D4','Posts & Content','Do you leave old public posts available without review?','yes_risk'),
# E Connections
('E1','Friends / Followers','Do you accept connection requests from people you do not know?','yes_risk'),
('E2','Friends / Followers','Can unknown users follow or interact with you freely?','yes_risk'),
('E3','Friends / Followers','Do you rarely review followers/connections?','yes_risk'),
('E4','Friends / Followers','Do you accept requests mainly because of mutual connections?','yes_risk'),
# F Tagging
('F1','Tagging & Mentions','Can anyone tag you without approval?','yes_risk'),
('F2','Tagging & Mentions','Is tag review disabled?','yes_risk'),
('F3','Tagging & Mentions','Can tagged posts appear automatically on your profile?','yes_risk'),
('F4','Tagging & Mentions','Can unknown users mention you?','yes_risk'),
# G Account Security
('G1','Authentication & Account Security','Is multi-factor authentication (MFA) disabled?','yes_risk'),
('G2','Authentication & Account Security','Are login/security alerts disabled?','yes_risk'),
('G3','Authentication & Account Security','Do you reuse a password across accounts?','yes_risk'),
('G4','Authentication & Account Security','Do you rarely review active sessions/devices?','yes_risk'),
('G5','Authentication & Account Security','Do you rarely review recovery/security information?','yes_risk'),
('G6','Authentication & Account Security','Do you avoid using a password manager when one is available?','yes_risk'),
# H Apps
('H1','Third-Party Apps','Do you rarely review connected third-party applications?','yes_risk'),
('H2','Third-Party Apps','Are there unused integrations connected to your account?','yes_risk'),
('H3','Third-Party Apps','Do you grant permissions without checking what they allow?','yes_risk'),
('H4','Third-Party Apps','Do you use old “Sign in with social account” connections?','yes_risk'),
# I Social engineering
('I1','Messaging & Social Engineering','Do you respond to suspicious direct messages?','yes_risk'),
('I2','Messaging & Social Engineering','Do you click unexpected links sent through messages?','yes_risk'),
('I3','Messaging & Social Engineering','Would you share a verification code if someone asked?','yes_risk'),
('I4','Messaging & Social Engineering','Do you share personal information through messages with unfamiliar people?','yes_risk'),
('I5','Messaging & Social Engineering','Do you trust accounts mainly because they look familiar?','yes_risk'),
# J footprint
('J1','Digital Footprint','Do you rarely review old public posts?','yes_risk'),
('J2','Digital Footprint','Do you have unused public accounts?','yes_risk'),
('J3','Digital Footprint','Do you rarely review public comments or profile history?','yes_risk'),
('J4','Digital Footprint','Have your privacy settings not been reviewed recently?','yes_risk'),
]

WEIGHTS = {k:w for k,_,w in CATEGORIES}
LABELS = {k:l for k,l,_ in CATEGORIES}

CHECKLIST = [
'Review profile visibility', 'Hide unnecessary contact information', 'Review birth-date visibility',
'Review location sharing', 'Avoid unnecessary real-time location posts', 'Review tagging permissions',
'Review followers/friends', 'Verify unfamiliar requests', 'Enable MFA', 'Enable login alerts where available',
'Review active sessions', 'Review connected apps', 'Remove unused integrations', 'Review old public posts',
'Review photo privacy', 'Be cautious with unexpected links', 'Never share verification codes',
'Review privacy settings periodically'
]

CATEGORY_QUESTION_MAP = {
'profile_visibility':['A1','A2','A3','A4'], 'personal_info':['B1','B2','B3','B4','B5','B6','B7'],
'location':['C1','C2','C3','C4','C5'], 'content':['D1','D2','D3','D4'],
'connections':['E1','E2','E3','E4'], 'tagging':['F1','F2','F3','F4'],
'account_security':['G1','G2','G3','G4','G5','G6'], 'third_party':['H1','H2','H3','H4'],
'social_engineering':['I1','I2','I3','I4','I5'], 'digital_footprint':['J1','J2','J3','J4']
}

SEVERITY = {'critical':'CRITICAL','high':'HIGH','medium':'MEDIUM','low':'LOW'}

def risk_level(score):
    if score <= 20: return 'LOW'
    if score <= 40: return 'MODERATE'
    if score <= 70: return 'HIGH'
    return 'CRITICAL'

def _is_risky(v):
    return str(v).strip().lower() in {'yes','often','public','true','sometimes'}

def extract_privacy_features(answers):
    return {qid: _is_risky(answers.get(qid, 'no')) for qid, *_ in QUESTIONS}

def calculate_category_scores(answers):
    features = extract_privacy_features(answers)
    scores = {}
    for key, qids in CATEGORY_QUESTION_MAP.items():
        risky = sum(features[q] for q in qids)
        scores[key] = round((risky / len(qids)) * 100, 1)
    return scores

def calculate_privacy_risk(category_scores):
    total = sum(category_scores[k] * WEIGHTS[k] / 100 for k in WEIGHTS)
    return round(max(0, min(100, total)), 1)

def generate_privacy_findings(answers, category_scores):
    findings=[]
    rules = {
      'B1':('PERSONAL_INFO','Phone number reported as publicly visible','high','Limit phone-number visibility where possible.'),
      'B2':('PERSONAL_INFO','Personal email reported as publicly visible','medium','Use privacy controls or a dedicated public contact method.'),
      'B3':('PERSONAL_INFO','Full birth date reported as publicly visible','high','Limit birth-date visibility to the minimum needed.'),
      'B4':('PERSONAL_INFO','Home-related information reported as public','high','Remove unnecessary home-related details from public profiles.'),
      'C1':('LOCATION','Current location sharing is enabled','high','Avoid publicly broadcasting real-time location unless intentionally needed.'),
      'C2':('LOCATION','Public geotagging/check-ins are enabled','high','Review geotagging and remove sensitive location history.'),
      'C3':('LOCATION','Travel plans are publicly shared','high','Consider posting travel updates after leaving a location.'),
      'C4':('LOCATION','Frequent location patterns may be exposed','high','Avoid repeating predictable time/place patterns publicly.'),
      'C5':('LOCATION','Home/work location may be inferred','high','Avoid details that make routine locations easy to infer.'),
      'D3':('CONTENT','Photos may reveal badges, documents, or screens','medium','Review images before posting and crop/blur sensitive details.'),
      'D4':('CONTENT','Old public posts are not regularly reviewed','medium','Periodically review and restrict older public content.'),
      'E1':('CONNECTIONS','Unknown connection requests are accepted','high','Verify unfamiliar profiles before accepting connections.'),
      'E3':('CONNECTIONS','Followers/connections are rarely reviewed','medium','Review followers and remove unfamiliar or unnecessary connections.'),
      'F1':('TAGGING','Anyone can tag the account without approval','medium','Enable tag review where the platform supports it.'),
      'F2':('TAGGING','Tag review is disabled','medium','Enable tag review before content appears on the profile.'),
      'G1':('ACCOUNT_SECURITY','MFA is disabled','high','Enable multi-factor authentication using the strongest supported method available.'),
      'G2':('ACCOUNT_SECURITY','Login/security alerts are disabled','high','Enable login and security alerts where available.'),
      'G3':('ACCOUNT_SECURITY','Password reuse is reported','critical','Use unique passwords and a password manager.'),
      'H1':('THIRD_PARTY','Connected applications are not regularly reviewed','medium','Review connected applications and revoke unnecessary access.'),
      'H2':('THIRD_PARTY','Unused third-party integrations may remain connected','medium','Remove unused integrations following least privilege.'),
      'I1':('SOCIAL_ENGINEERING','Suspicious direct messages may receive responses','high','Verify unexpected requests through a trusted channel.'),
      'I2':('SOCIAL_ENGINEERING','Unexpected links may be clicked','high','Avoid unexpected links and verify the sender independently.'),
      'I3':('SOCIAL_ENGINEERING','Verification codes may be shared','critical','Never share verification codes with anyone.'),
      'I4':('SOCIAL_ENGINEERING','Personal information may be shared with unfamiliar people','high','Do not share sensitive information through unsolicited messages.'),
      'J1':('DIGITAL_FOOTPRINT','Old public posts are rarely reviewed','medium','Schedule periodic digital-footprint reviews.'),
      'J2':('DIGITAL_FOOTPRINT','Unused public accounts may remain active','medium','Close or privatize accounts you no longer use.'),
      'J4':('DIGITAL_FOOTPRINT','Privacy settings have not been reviewed recently','medium','Review privacy settings periodically after platform changes.'),
    }
    for qid,(cat,item,severity,fix) in rules.items():
        if _is_risky(answers.get(qid,'no')):
            findings.append({'category':cat,'finding_type':qid,'severity':SEVERITY[severity], 'description':item,'recommendation':fix})
    # Add category-level findings for any high category even if no rule above matched.
    for key,label,_ in CATEGORIES:
        if category_scores[key] >= 70 and not any(f['category']==key.upper() for f in findings):
            findings.append({'category':key.upper(),'finding_type':'CATEGORY_HIGH','severity':'HIGH','description':f'{label} assessed risk is {category_scores[key]:.0f}/100.','recommendation':f'Review the {label.lower()} controls in the checklist.'})
    return findings

def generate_recommendations(findings):
    seen=set(); recs=[]
    priority_order={'CRITICAL':0,'HIGH':1,'MEDIUM':2,'LOW':3}
    for f in sorted(findings,key=lambda x: priority_order.get(x['severity'],9)):
        key=f['recommendation']
        if key not in seen:
            seen.add(key); recs.append({'priority':f['severity'],'finding_type':f['finding_type'],'recommendation':key})
    return recs

def assess(answers):
    category_scores=calculate_category_scores(answers)
    score=calculate_privacy_risk(category_scores)
    findings=generate_privacy_findings(answers,category_scores)
    recs=generate_recommendations(findings)
    return {'score':score,'risk_level':risk_level(score),'category_scores':category_scores,'findings':findings,'recommendations':recs}

def simulate_improvement(answers, changes):
    before=assess(answers)
    improved=dict(answers)
    improved.update(changes)
    after=assess(improved)
    return {'before':before,'after':after,'risk_reduction':round(max(0,before['score']-after['score']),1)}
