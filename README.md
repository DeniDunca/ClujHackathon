![image](https://github.com/user-attachments/assets/feb0e848-b395-4991-b310-177acfe0a08c)

OncoGuide is a 24/7 virtual assistant designed to support cancer patients by offering early symptom screening, document analysis, educational resources, and personalized guidance. It does not provide diagnosis or treatment, but helps users understand medical terms, ask questions about their reports, and know when to consult a doctor. Built for both patients and clinics, OncoGuide bridges the gap between overwhelmed medical systems and people in need of clear, compassionate support.


##  Key Features

- **Symptom Screening Chatbot**  
  A structured AI conversation that asks users 5 clinically relevant questions to identify early warning signs of cancer.

- **PDF Document Analysis**  
  Users can upload medical documents (e.g., histopathology reports). The AI interprets the content using NLP and a context-aware prompt system (RAG pipeline).

- **Patient Education**  
  Offers clear, accessible information about cancer symptoms, next steps, screening importance, and more.

- **Appointment Recommendation**  
  At the end of the flow, the bot asks users if they’d like to request an appointment. Optionally logs request in Google Sheets for clinic follow-up.
  
##  Authentication

- Secure user authentication is implemented using **JWT (JSON Web Tokens)** for session handling.
- **Passwords are hashed** before being stored in the database to ensure user data protection.
- This enables safe user access and account-based personalization within clinics or patient flows.

##  Tech Stack

| Layer        | Technology                    |
|--------------|-------------------------------|
| **Frontend** | Vue.js                        |
| **Backend**  | FastAPI (Python)              |
| **AI Layer** | ASI ONE mini                  |
| **Storage**  | Supabase                      |
| **Database** | PostgreSQL                    |

---
## DEMO

https://github.com/user-attachments/assets/2eda08b3-40e6-4479-a146-d6a3617b07c8


![image](https://github.com/user-attachments/assets/75f493eb-cf4a-4b93-b2ac-a6317283b0df)
