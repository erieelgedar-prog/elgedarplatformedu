import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# إعداد الاتصال بـ Firebase
if not firebase_admin._apps:
    # البيانات دي جاية من الـ JSON اللي بعتهولي
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

# تصميم واجهة منصة الجعدار
st.set_page_config(page_title="منصة الجعدار التعليمية", page_icon="🚀")

st.title("🚀 منصة الجعدار - Elgedar")# نظام الدخول بالكود
code_input = st.text_input("أدخل كود الحصة الخاص بك:", type="password", help="الكود صالح لجهاز واحد فقط")

if st.button("تحقق ودخول"):
    if code_input:
        ref = db.reference(f'codes/{code_input}')
        data = ref.get()
        
        if data:
            st.success(f"أهلاً بك يا بطل! تم تفعيل الكود.")
            # هنا رابط الفيديو من يوتيوب (غير مدرج)
            st.video("https://www.youtube.com/watch?v=تحط_رابط_الفيديو_هنا")
        else:
            st.error("الكود غير صحيح أو انتهت صلاحيته!")
    else:
        st.warning("من فضلك أدخل الكود أولاً")

# كود النطق (JavaScript) اللي عملناه سوا
st.components.v1.html("""
    <script>
    function speak(text) {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'ar-SA';
        u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    // يمكن إضافة أزرار نطق هنا لو حبيت
    </script>
""", height=0)
