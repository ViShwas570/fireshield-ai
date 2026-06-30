"""
FireShield AI - Chatbot Service

Emergency chatbot providing comprehensive guidance for fire emergencies.
Supports English and Hindi responses with context-aware quick reply suggestions.
"""

from typing import Optional

from app.models.chat import ChatMessage, ChatResponse, EmergencyType


# ─────────────────────────────────────────────────────────────────────
# English knowledge base
# ─────────────────────────────────────────────────────────────────────

_RESPONSES_EN = {
    EmergencyType.FIRE_EVACUATION: {
        "response": (
            "🚨 **Fire Evacuation Procedures:**\n\n"
            "1. **Stay calm** and alert others immediately by shouting 'FIRE!'\n"
            "2. **Feel doors** before opening — if hot, do NOT open. Use an alternate route.\n"
            "3. **Crawl low** under smoke. Smoke rises, so cleaner air is near the floor.\n"
            "4. **Use stairs ONLY** — never use elevators during a fire.\n"
            "5. **Close doors** behind you as you leave to slow the fire's spread.\n"
            "6. **Go to the nearest assembly point** and do a headcount.\n"
            "7. **Call 101** (Fire) or **112** (Emergency) once you are safely outside.\n"
            "8. **Never go back inside** a burning building for any reason.\n\n"
            "If you are **trapped**:\n"
            "- Seal door gaps with wet cloth or towels\n"
            "- Go to a window and signal for help\n"
            "- Stay low to avoid smoke inhalation\n"
            "- Call emergency services and give your exact location"
        ),
        "suggestions": [
            "What if I'm trapped?",
            "First aid for burns",
            "How to help children evacuate?",
            "Smoke inhalation symptoms",
        ],
        "is_emergency": True,
        "emergency_number": "101",
    },
    EmergencyType.BURN_FIRST_AID: {
        "response": (
            "🏥 **First Aid for Burns:**\n\n"
            "**For Minor Burns (1st degree):**\n"
            "1. Cool the burn under cool (NOT cold/ice) running water for **at least 20 minutes**\n"
            "2. Do NOT apply ice, butter, toothpaste, or any home remedies\n"
            "3. Remove rings, watches, or tight clothing near the burn before swelling starts\n"
            "4. Apply aloe vera gel or an antibiotic ointment\n"
            "5. Cover loosely with a sterile, non-stick bandage\n"
            "6. Take over-the-counter pain relief if needed\n\n"
            "**For Severe Burns (2nd/3rd degree):**\n"
            "1. **Call 108 (Ambulance) or 112 immediately**\n"
            "2. Do NOT remove burned clothing stuck to the skin\n"
            "3. Do NOT immerse large severe burns in water — risk of hypothermia\n"
            "4. Cover the area with a clean, dry cloth or sterile bandage\n"
            "5. Elevate the burned area above heart level if possible\n"
            "6. Monitor breathing — burns can cause airway swelling\n"
            "7. Keep the person warm and comfortable until help arrives\n\n"
            "⚠️ **Seek immediate medical attention if:**\n"
            "- Burns cover a large area or are on face/hands/joints/genitals\n"
            "- The burn looks white, brown, or black (3rd degree)\n"
            "- The person is a child, elderly, or has breathing difficulties"
        ),
        "suggestions": [
            "When to go to hospital?",
            "Smoke inhalation treatment",
            "Chemical burn first aid",
            "Electrical burn first aid",
        ],
        "is_emergency": False,
        "emergency_number": "108",
    },
    EmergencyType.SMOKE_INHALATION: {
        "response": (
            "💨 **Smoke Inhalation — What To Do:**\n\n"
            "**Symptoms to watch for:**\n"
            "- Coughing, wheezing, or shortness of breath\n"
            "- Hoarse voice or difficulty speaking\n"
            "- Soot around nose or mouth\n"
            "- Headache, confusion, or dizziness\n"
            "- Nausea or vomiting\n"
            "- Burns on face, lips, or nose hairs\n\n"
            "**Immediate Actions:**\n"
            "1. **Move the person to fresh air** immediately\n"
            "2. **Call 108 (Ambulance)** — smoke inhalation can be life-threatening\n"
            "3. If the person is unconscious, check airway and breathing\n"
            "4. Begin **CPR** if the person is not breathing and you are trained\n"
            "5. Loosen tight clothing around neck and chest\n"
            "6. Keep the person sitting upright to aid breathing\n"
            "7. Do NOT give anything to eat or drink\n"
            "8. Monitor for delayed symptoms — they can appear hours later\n\n"
            "⚠️ **Carbon monoxide poisoning** from smoke is invisible and deadly. "
            "Even if someone feels fine after exposure, they should be evaluated by a doctor."
        ),
        "suggestions": [
            "CPR instructions",
            "Carbon monoxide symptoms",
            "Fire evacuation procedure",
            "When to call ambulance?",
        ],
        "is_emergency": True,
        "emergency_number": "108",
    },
    EmergencyType.ELECTRICAL_FIRE: {
        "response": (
            "⚡ **Electrical Fire Safety:**\n\n"
            "**CRITICAL: NEVER use water on an electrical fire!**\n\n"
            "**If you discover an electrical fire:**\n"
            "1. **Disconnect power** — switch off the mains/MCB if safely accessible\n"
            "2. If power cannot be cut, do NOT approach the fire\n"
            "3. Use a **CO2 or dry chemical fire extinguisher** (Class C rated)\n"
            "4. If no extinguisher is available, **evacuate immediately**\n"
            "5. **Call 101** (Fire Service) and report an electrical fire\n"
            "6. Close the door to contain the fire as you leave\n\n"
            "**Prevention Tips:**\n"
            "- Never overload electrical outlets or extension cords\n"
            "- Replace frayed or damaged wires immediately\n"
            "- Use ISI-marked electrical equipment only\n"
            "- Install MCB/RCCB circuit breakers in your home\n"
            "- Get electrical wiring inspected by a licensed electrician annually\n"
            "- Keep flammable materials away from electrical panels\n\n"
            "⚠️ **Downed power lines:** Stay at least 10 meters away and call the "
            "electricity board emergency number immediately."
        ),
        "suggestions": [
            "What fire extinguisher to use?",
            "Short circuit prevention",
            "Fire evacuation procedure",
            "First aid for electrical burns",
        ],
        "is_emergency": True,
        "emergency_number": "101",
    },
    EmergencyType.GAS_LEAK: {
        "response": (
            "⛽ **Gas Leak Emergency Procedures:**\n\n"
            "**If you smell gas (rotten egg smell):**\n\n"
            "1. **DO NOT** switch on/off any electrical switches or appliances\n"
            "2. **DO NOT** light matches, candles, or any flame\n"
            "3. **DO NOT** use mobile phones inside the area\n"
            "4. **Open all windows and doors** to ventilate\n"
            "5. **Turn off the gas supply** at the cylinder valve or main line\n"
            "6. **Evacuate everyone** from the building immediately\n"
            "7. Move to a safe distance (at least 100 meters)\n"
            "8. **Call 101 (Fire) or 112 (Emergency)** from a safe distance\n\n"
            "**For LPG Cylinder Safety:**\n"
            "- Always keep cylinders upright and in a well-ventilated area\n"
            "- Check hose/regulator for damage before each cylinder change\n"
            "- Replace rubber tubes every 2 years\n"
            "- Use ISI-marked regulators only\n"
            "- Never use a cylinder with a damaged valve\n"
            "- Apply soapy water on connections to check for leaks (bubbles = leak)\n\n"
            "⚠️ **LPG is heavier than air** — it settles on the floor. "
            "Gas can accumulate in basements and enclosed spaces creating explosion risk."
        ),
        "suggestions": [
            "LPG cylinder safety",
            "What NOT to do during gas leak?",
            "Fire evacuation procedure",
            "Explosion first aid",
        ],
        "is_emergency": True,
        "emergency_number": "101",
    },
    EmergencyType.CHILD_ELDERLY_EVACUATION: {
        "response": (
            "👶👴 **Evacuating Children and Elderly:**\n\n"
            "**For Children:**\n"
            "1. Stay calm — children will panic if they see adults panicking\n"
            "2. Pick up or carry small children if needed\n"
            "3. Hold their hand firmly and guide them to the exit\n"
            "4. Teach children to 'Stop, Drop, and Roll' if clothes catch fire\n"
            "5. Tell them to crawl under smoke\n"
            "6. Practice fire drills regularly so children know the escape route\n"
            "7. Have a designated meeting point outside\n\n"
            "**For Elderly/Persons with Disabilities:**\n"
            "1. Assist them immediately — they may need physical support\n"
            "2. If using a wheelchair, use evacuation chairs for stairs (NEVER elevators)\n"
            "3. Assign a 'buddy' for elderly residents in your building\n"
            "4. Ensure they have their essential medications if time permits\n"
            "5. For hearing-impaired: use visual signals (flash lights, wave arms)\n"
            "6. For visually impaired: guide by arm and describe the path verbally\n"
            "7. If they cannot be moved, bring them to a safe room with a window, "
            "seal the door, and signal for help\n\n"
            "**Important:** Always inform firefighters if someone is still inside the building."
        ),
        "suggestions": [
            "Fire evacuation procedure",
            "What if someone is trapped?",
            "First aid for burns",
            "Fire safety for homes",
        ],
        "is_emergency": True,
        "emergency_number": "112",
    },
    EmergencyType.PET_EVACUATION: {
        "response": (
            "🐾 **Pet Evacuation During Fire:**\n\n"
            "**Before a fire (Preparation):**\n"
            "1. Keep pet carriers, leashes, and harnesses near exits\n"
            "2. Include pet supplies in your emergency kit\n"
            "3. Know where your pets hide when scared (under beds, closets)\n"
            "4. Place 'Pets Inside' stickers on windows for firefighters\n"
            "5. Microchip your pets and keep ID tags updated\n\n"
            "**During a fire:**\n"
            "1. **Your safety comes first** — do not risk your life for a pet\n"
            "2. If safe, quickly grab the pet and their carrier\n"
            "3. Dogs: put on leash immediately; cats: put in carrier\n"
            "4. Do NOT open doors to search for hiding pets if smoke is heavy\n"
            "5. Once outside, keep pets on leash — they may try to run back inside\n"
            "6. **Inform firefighters** about any pets left inside, their type, and likely location\n\n"
            "**After evacuation:**\n"
            "- Keep pets away from fire scene (toxic fumes)\n"
            "- Check paws for burns from hot surfaces\n"
            "- Watch for smoke inhalation signs: coughing, drooling, difficulty breathing\n"
            "- Take to a vet if showing any symptoms"
        ),
        "suggestions": [
            "Fire evacuation procedure",
            "Fire safety at home",
            "First aid basics",
            "Emergency numbers",
        ],
        "is_emergency": False,
        "emergency_number": "101",
    },
    EmergencyType.FIRE_SAFETY: {
        "response": (
            "🛡️ **General Fire Safety Tips for Your Home:**\n\n"
            "**Fire Prevention:**\n"
            "1. Install **smoke detectors** on every floor and test monthly\n"
            "2. Keep a **fire extinguisher** (ABC type) in kitchen and near exit\n"
            "3. Never leave cooking unattended on the stove\n"
            "4. Keep flammable items (curtains, papers) away from heat sources\n"
            "5. Don't overload electrical sockets — use one plug per socket\n"
            "6. Get electrical wiring inspected regularly\n"
            "7. Store LPG cylinders in ventilated areas only\n"
            "8. Keep matchboxes and lighters away from children\n\n"
            "**Fire Preparedness:**\n"
            "1. Create a **fire escape plan** with 2 exits from every room\n"
            "2. Practice fire drills with your family every 6 months\n"
            "3. Know the location of the nearest fire station\n"
            "4. Save emergency numbers: **101** (Fire), **108** (Ambulance), **112** (Emergency)\n"
            "5. Keep important documents in a fireproof safe or digitally backed up\n\n"
            "**Indian Emergency Numbers:**\n"
            "- 🚒 Fire Service: **101**\n"
            "- 🚑 Ambulance: **108**\n"
            "- 🚔 Police: **100**\n"
            "- 📞 Universal Emergency: **112**\n"
            "- 🏥 Disaster Management: **1078**"
        ),
        "suggestions": [
            "Fire extinguisher types",
            "Evacuation procedure",
            "First aid for burns",
            "Electrical fire safety",
        ],
        "is_emergency": False,
        "emergency_number": "112",
    },
    EmergencyType.GENERAL: {
        "response": (
            "🤖 **Hello! I'm FireShield AI Assistant.**\n\n"
            "I can help you with fire emergency guidance. Here's what I can assist with:\n\n"
            "🔥 **Fire Evacuation** — Step-by-step evacuation procedures\n"
            "🏥 **Burn First Aid** — How to treat burn injuries\n"
            "💨 **Smoke Inhalation** — Symptoms and treatment\n"
            "⚡ **Electrical Fire** — Safety procedures for electrical fires\n"
            "⛽ **Gas Leak** — What to do during a gas leak\n"
            "👶 **Child/Elderly Evacuation** — Special evacuation procedures\n"
            "🐾 **Pet Evacuation** — How to safely evacuate pets\n"
            "🛡️ **Fire Safety** — Prevention tips and emergency numbers\n\n"
            "**In a real emergency, always call:**\n"
            "- 🚒 **101** — Fire Service\n"
            "- 🚑 **108** — Ambulance\n"
            "- 📞 **112** — Universal Emergency Number\n\n"
            "Type your question or select a topic below!"
        ),
        "suggestions": [
            "Fire evacuation procedure",
            "First aid for burns",
            "Electrical fire safety",
            "Gas leak emergency",
            "Fire safety tips",
            "Smoke inhalation help",
        ],
        "is_emergency": False,
        "emergency_number": "112",
    },
}


# ─────────────────────────────────────────────────────────────────────
# Hindi knowledge base
# ─────────────────────────────────────────────────────────────────────

_RESPONSES_HI = {
    EmergencyType.FIRE_EVACUATION: {
        "response": (
            "🚨 **आग से निकासी प्रक्रिया:**\n\n"
            "1. **शांत रहें** और तुरंत 'आग! आग!' चिल्लाकर सभी को सूचित करें\n"
            "2. **दरवाज़ा खोलने से पहले छुएं** — अगर गर्म है तो न खोलें, दूसरा रास्ता अपनाएं\n"
            "3. **धुएं के नीचे रेंगकर चलें** — साफ हवा ज़मीन के पास होती है\n"
            "4. **केवल सीढ़ियों का उपयोग करें** — लिफ्ट का उपयोग कभी न करें\n"
            "5. **दरवाज़े बंद करें** जब आप निकलें, इससे आग की गति धीमी होगी\n"
            "6. **निकटतम सभा स्थल पर जाएं** और गिनती करें\n"
            "7. सुरक्षित बाहर आने के बाद **101** (फायर) या **112** (इमरजेंसी) पर कॉल करें\n"
            "8. **कभी वापस अंदर न जाएं** जलती इमारत में\n\n"
            "अगर आप **फंसे** हैं:\n"
            "- दरवाज़े के नीचे गीला कपड़ा लगाएं\n"
            "- खिड़की पर जाएं और मदद के लिए संकेत करें\n"
            "- **101 या 112** पर कॉल करें और अपना सटीक स्थान बताएं"
        ),
        "suggestions": [
            "अगर फंस जाऊं तो?",
            "जलने पर प्राथमिक उपचार",
            "बच्चों को कैसे निकालें?",
            "धुआं सांस में जाने पर क्या करें?",
        ],
        "is_emergency": True,
        "emergency_number": "101",
    },
    EmergencyType.BURN_FIRST_AID: {
        "response": (
            "🏥 **जलने पर प्राथमिक उपचार:**\n\n"
            "**हल्के जलने पर:**\n"
            "1. **20 मिनट तक ठंडे पानी** में रखें (बर्फ नहीं!)\n"
            "2. मक्खन, टूथपेस्ट या घरेलू नुस्खे न लगाएं\n"
            "3. अंगूठी, घड़ी या तंग कपड़े तुरंत हटाएं\n"
            "4. एलोवेरा जेल या एंटीबायोटिक मलहम लगाएं\n"
            "5. साफ पट्टी से ढकें\n\n"
            "**गंभीर जलने पर:**\n"
            "1. **तुरंत 108 (एम्बुलेंस) कॉल करें**\n"
            "2. चिपके हुए कपड़े न हटाएं\n"
            "3. साफ सूखे कपड़े से ढकें\n"
            "4. जले हुए हिस्से को दिल से ऊपर रखें\n"
            "5. सांस पर नज़र रखें\n\n"
            "⚠️ **तुरंत डॉक्टर को दिखाएं अगर:**\n"
            "- जलन चेहरे, हाथों या जोड़ों पर हो\n"
            "- त्वचा सफेद, भूरी या काली दिखे\n"
            "- बच्चे या बुज़ुर्ग जले हों"
        ),
        "suggestions": [
            "अस्पताल कब जाएं?",
            "धुआं सांस में जाने पर उपचार",
            "बिजली से जलने पर क्या करें?",
            "आग से निकासी प्रक्रिया",
        ],
        "is_emergency": False,
        "emergency_number": "108",
    },
    EmergencyType.GENERAL: {
        "response": (
            "🤖 **नमस्ते! मैं FireShield AI सहायक हूँ।**\n\n"
            "मैं आग की आपातकालीन स्थितियों में आपकी मदद कर सकता हूँ:\n\n"
            "🔥 **आग से निकासी** — कदम दर कदम निकासी प्रक्रिया\n"
            "🏥 **जलने पर प्राथमिक उपचार** — जलने का इलाज कैसे करें\n"
            "💨 **धुआं सांस में जाना** — लक्षण और उपचार\n"
            "⚡ **बिजली की आग** — सुरक्षा प्रक्रियाएं\n"
            "⛽ **गैस लीक** — गैस लीक होने पर क्या करें\n"
            "🛡️ **आग सुरक्षा** — रोकथाम के उपाय\n\n"
            "**आपातकालीन नंबर:**\n"
            "- 🚒 **101** — फायर सर्विस\n"
            "- 🚑 **108** — एम्बुलेंस\n"
            "- 📞 **112** — यूनिवर्सल इमरजेंसी\n\n"
            "अपना सवाल टाइप करें या नीचे विषय चुनें!"
        ),
        "suggestions": [
            "आग से निकासी प्रक्रिया",
            "जलने पर प्राथमिक उपचार",
            "बिजली की आग में सुरक्षा",
            "गैस लीक इमरजेंसी",
            "आग सुरक्षा टिप्स",
        ],
        "is_emergency": False,
        "emergency_number": "112",
    },
}


# ─────────────────────────────────────────────────────────────────────
# Keyword -> EmergencyType detection
# ─────────────────────────────────────────────────────────────────────

_KEYWORD_MAP_EN = {
    EmergencyType.FIRE_EVACUATION: [
        "evacuate", "evacuation", "escape", "get out", "exit", "trapped",
        "stuck", "building on fire", "how to escape", "leave building",
        "fire drill", "assembly point",
    ],
    EmergencyType.BURN_FIRST_AID: [
        "burn", "burns", "burned", "scalded", "first aid", "skin burn",
        "treatment", "blister", "wound", "injury",
    ],
    EmergencyType.SMOKE_INHALATION: [
        "smoke", "inhale", "inhalation", "breathing", "cough", "fumes",
        "can't breathe", "difficulty breathing", "choking", "carbon monoxide",
    ],
    EmergencyType.ELECTRICAL_FIRE: [
        "electrical", "electric", "short circuit", "wiring", "wire",
        "outlet", "socket", "power", "transformer", "switch",
    ],
    EmergencyType.GAS_LEAK: [
        "gas leak", "gas", "lpg", "cylinder", "propane", "smell gas",
        "gas pipeline", "leaking gas", "explosion",
    ],
    EmergencyType.CHILD_ELDERLY_EVACUATION: [
        "child", "children", "baby", "kid", "elderly", "old person",
        "disabled", "wheelchair", "handicapped", "senior citizen",
    ],
    EmergencyType.PET_EVACUATION: [
        "pet", "dog", "cat", "animal", "bird", "pets",
    ],
    EmergencyType.FIRE_SAFETY: [
        "safety", "prevention", "prevent", "tips", "precaution",
        "fire extinguisher", "smoke detector", "fire alarm", "prepare",
        "emergency number", "emergency contact",
    ],
}

_KEYWORD_MAP_HI = {
    EmergencyType.FIRE_EVACUATION: [
        "निकासी", "बाहर निकलो", "भागो", "फंसा", "बाहर", "आग लगी",
        "कैसे निकलें", "इमारत", "escape",
    ],
    EmergencyType.BURN_FIRST_AID: [
        "जलना", "जल गया", "जलने", "प्राथमिक उपचार", "फफोला", "चोट",
        "जलन", "burn",
    ],
    EmergencyType.GENERAL: [
        "नमस्ते", "हेलो", "हाय", "मदद", "सहायता", "help",
    ],
}


def _detect_emergency_type(message: str, lang: str = "en") -> EmergencyType:
    """
    Detect the emergency type from a user's message using keyword matching.

    Args:
        message: The user's chat message.
        lang: Language code ('en' or 'hi').

    Returns:
        The detected EmergencyType.
    """
    msg_lower = message.lower()

    keyword_map = _KEYWORD_MAP_HI if lang == "hi" else _KEYWORD_MAP_EN

    scores = {}
    for etype, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in msg_lower)
        if score > 0:
            scores[etype] = score

    if scores:
        return max(scores, key=scores.get)
    return EmergencyType.GENERAL


def get_chat_response(chat_message: ChatMessage) -> ChatResponse:
    """
    Process a chat message and return an appropriate emergency guidance response.

    Detects the emergency type from keywords in the message, selects the
    appropriate response from the knowledge base (English or Hindi), and
    returns it with quick reply suggestions.

    Args:
        chat_message: The incoming chat message with text and language preference.

    Returns:
        ChatResponse with guidance text, suggestions, and emergency metadata.
    """
    emergency_type = _detect_emergency_type(chat_message.message, chat_message.lang)

    # Select language-specific responses
    if chat_message.lang == "hi":
        responses = _RESPONSES_HI
    else:
        responses = _RESPONSES_EN

    # Fallback to English if Hindi response not available for this type
    if emergency_type not in responses:
        responses = _RESPONSES_EN

    # Fallback to GENERAL if type still not found
    response_data = responses.get(emergency_type, responses.get(EmergencyType.GENERAL, _RESPONSES_EN[EmergencyType.GENERAL]))

    return ChatResponse(
        response=response_data["response"],
        suggestions=response_data["suggestions"],
        emergency_type=emergency_type,
        is_emergency=response_data.get("is_emergency", False),
        emergency_number=response_data.get("emergency_number", "112"),
    )
