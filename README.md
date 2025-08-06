# 🌍 Ecosync AI – Multi-Agent Sustainability & Wildlife Health Assistant

**Ecosync AI** is an intelligent, multi-agent web application designed to align with the United Nations Sustainable Development Goals (UN SDGs), primarily focusing on:

- 🐠 Goal 14: Life Below Water  
- 🌳 Goal 15: Life on Land  
- ❤️ Goal 3: Good Health and Well-being

This project was developed as a **group collaboration** led by **Gautam Vaishnav**, with team members **Nishtha Kalra**, **Dimple Sharma**, and **Khushi Tanwar**. The project delivers advanced AI functionalities with a clean, accessible, and responsive interface using free and open technologies.

---

## 🚀 Live Features

- ✅ Multi-Agent System with clean agent routing  
- ✅ AI-powered Chatbot on Environmental and Sustainability topics  
- ✅ Marine Animal Health Analyzer (Image + Text Input)  
- ✅ Land Animal Health Analyzer (Reuses marine logic)  
- ✅ **Location-based clinic and vet finder** (Delhi, Noida, etc.)  
- ✅ OpenRouter API integration for **lightweight AI models**  
- ✅ Clean UI using Streamlit with LangGraph for agent flow  

---

## 🧠 AI Models Used

| Agent                | Model Name                                 | Type              |
|---------------------|---------------------------------------------|-------------------|
| Eco Chatbot Agent   | `mistralai/mistral-small-3.2-24b-instruct`  | Text-only         |
| Marine Health Agent | `moonshotai/kimi-vl-a3b-thinking`           | Vision + Text     |
| Land Health Agent   | Reuses above (Marine Health logic)          | Vision + Text     |

All models are called via the **OpenRouter API**, ensuring free-tier compatibility and fast response.

---

## 🔄 Multi-Agent Architecture

The app uses **LangGraph** for agent routing based on the input type and content:

- **Eco Chatbot** → For general Q&A around sustainability and UN SDGs.
- **Marine Health Agent** → For ocean animal analysis using image + prompt.
- **Land Health Agent** → For land animal diagnosis (uses same model as marine).

Agents are routed using natural keywords (e.g., “fish”, “dog”, “hurt”, “injury”) and input content type.

---

## 📍 Location-Based Clinic Finder

Both the **Marine** and **Land Health Agents** include a smart **clinic finder feature**.

### ➤ How it works:
- If the user inputs a prompt like:  
  `"My dog is badly hurt, and provide location in location tab."`
- The system detects the **location** ("Delhi") and the **need for medical attention**, and returns:
  - Nearby **veterinary hospitals**
  - **Animal care clinics**
  - Contact **phone numbers**
  - **Location info**

This uses predefined keyword-based mapping with future scope for Google Maps or Places API integration.

---

## 🛠️ Technologies Used

- 🐍 **Python 3.10+**
- 🌐 **Streamlit** (Frontend)
- 🧠 **OpenRouter API** (AI model backend)
- 📦 **LangGraph** (Routing logic)
- 📡 **RESTful APIs** (for future extensibility)
- 🗂️ **Modular architecture** with separate agents and utilities

---

## 📈 Future Enhancements (Planned)

- 🌐 **Multilingual support** (via Google Translate or DeepL API)
- 🧾 **NGO Dashboard** to connect animal/health organizations
- 💳 **Donation and Payment Integration**
- 📍 **Real-time maps integration** for clinic routing

---

## 👨‍💻 Team Credits

This project is a **group effort** developed with dedication and efficiency by:

- 👑 **Gautam Vaishnav** *(Team Leader)*
- 👩‍💻 **Nishtha Kalra**
- 👩‍💻 **Dimple Sharma**
- 👩‍💻 **Khushi Tanwar**

Together, we designed and implemented Ecosync AI to help users care for the environment and wildlife, while exploring the potential of AI in sustainability.

---

## 📄 License

This project is open-source and freely available for educational and non-commercial use.

---


