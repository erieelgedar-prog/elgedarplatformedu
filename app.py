import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import random
import string

# إعداد الاتصال بـ Firebase
if not firebase_admin._apps:
    fb_creds = {
        "type": "service_account",
        "project_id": "elgedarplatformedu",
        "private_key_id": "6328802fb7cf14054d87a4f65739b665fa9cb469",
        "private_key": st.secrets["private_key"].replace('\\n', '\n'),
        "client_email": "firebase-adminsdk-fbsvc@elgedarplatformedu.iam.gserviceaccount.com",
        "client_id": "111575475617878327020",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40elgedarplatformedu.iam.gserviceaccount.com"
    }
    cred = credentials.Certificate(fb_creds)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://elgedarplatformedu-default-rtdb.firebaseio.com/'
    })

# إعدادات الصفحة
st.set_page_config(page_title="منصة الجعدار التعليمية", page_icon="🚀")

# --- كلمة سر الأدمن (غيرها براحتك من هنا) ---
ADMIN_KEY = "hesham123" 

st.title("🚀 منصة الجعدار - Elgedar")

# نظام الدخول
code_input = st.text_input("أدخل كود الحصة الخاص بك:", type="password")

if st.button("تحقق ودخول"):
    if code_input == ADMIN_KEY:
        st.session_state['role'] = 'admin'
        st.success("تم الدخول بصلاحيات الأدمن يا مستر هشام!")
    elif code_input:
        ref = db.reference(f'codes/{code_input}')
        data = ref.get()
        if data:
            if data.get('used', False):
                st.error("عفواً، هذا الكود تم استخدامه مسبقاً على جهاز آخر!")
            else:
                # تحديث الكود ليصبح مستخدم
                ref.update({'used': True})
                st.success("أهلاً بك يا بطل! تم تفعيل الحصة.")
                video_url = db.reference('settings/video_url').get() or "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                st.video(video_url)
        else:
            st.error("الكود غير صحيح!")

# --- لوحة تحكم المدير (تظهر فقط للأدمن) ---
if st.session_state.get('role') == 'admin':
    st.divider()
    st.header("🛠️ لوحة تحكم منصة الجعدار")
    
    tab1, tab2 = st.tabs(["توليد أكواد", "إعدادات الفيديو"])
    
    with tab1:
        num_codes = st.number_input("عدد الأكواد المطلوب توليدها:", min_value=1, max_value=100, value=10)
        if st.button("توليد وحفظ الأكواد"):
            new_codes = []
            for _ in range(num_codes):
                c = 'GEDAR-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                db.reference(f'codes/{c}').set({'used': False})
                new_codes.append(c)
            st.write("تم توليد الأكواد بنجاح:")
            st.code("\n".join(new_codes))
            
    with tab2:
        new_url = st.text_input("رابط فيديو الحصة الجديد:")
        if st.button("تحديث الرابط"):
            db.reference('settings/video_url').set(new_url)
            st.success("تم تحديث رابط الفيديو بنجاح!")
