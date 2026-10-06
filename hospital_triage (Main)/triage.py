# =========================================================
# TRIAGE PRIORITY SYSTEM
# =========================================================

# =========================================================
# CRITICAL CONDITIONS (Priority 1 - Immediate)
# =========================================================
CRITICAL = {
    # Cardiac
    "chest pain", "heart attack", "cardiac arrest", "cardiac arrhythmia",
    "aortic dissection", "heart failure",

    # Neurological
    "stroke", "seizure", "unconscious", "unconsciousness",
    "brain hemorrhage", "severe head injury", "coma", "meningitis",

    # Respiratory
    "difficulty breathing", "not breathing", "respiratory failure",
    "airway obstruction", "choking", "pulmonary embolism",

    # Trauma / Bleeding
    "severe bleeding", "internal bleeding", "severe burns",
    "spinal injury", "severe trauma", "amputation",

    # Other
    "anaphylaxis", "anaphylactic shock", "septic shock",
    "diabetic coma", "overdose", "poisoning", "eclampsia"
}

# =========================================================
# URGENT CONDITIONS (Priority 2 - Within 15 minutes)
# =========================================================
URGENT = {
    # Cardiac / Respiratory
    "moderate chest pain", "asthma attack", "shortness of breath",
    "irregular heartbeat", "palpitations",

    # Neurological
    "dizziness", "sudden confusion", "severe headache",
    "fainting", "numbness", "vision loss", "sudden weakness",

    # Gastrointestinal
    "vomiting", "vomiting blood", "severe abdominal pain",
    "appendicitis", "bowel obstruction",

    # Injury / Bleeding
    "fracture", "moderate bleeding", "dislocated joint",
    "eye injury", "deep laceration", "head injury",

    # Infection / Fever
    "high fever", "severe infection", "urinary tract infection",
    "kidney infection", "cellulitis",

    # Other
    "dehydration", "severe allergic reaction", "panic attack",
    "suicidal thoughts", "drug reaction", "electrolyte imbalance"
}

# =========================================================
# MODERATE CONDITIONS (Priority 3 - Within 30 minutes)
# =========================================================
MODERATE = {
    # Pain
    "mild chest pain", "stomach pain", "back pain",
    "abdominal cramps", "joint pain", "ear pain", "toothache",

    # Injury
    "minor fracture", "minor bleeding", "sprain",
    "bruising", "minor head bump", "muscle strain",

    # Neurological / Mental
    "migraine", "moderate dizziness", "anxiety attack",
    "depression episode", "memory confusion",

    # Infection / Illness
    "infection", "urinary infection", "skin rash",
    "moderate fever", "nausea", "food poisoning",

    # Other
    "body weakness", "fatigue", "swelling",
    "mild allergic reaction", "hyperventilation"
}

# =========================================================
# MINOR CONDITIONS (Priority 4 - Non-urgent)
# =========================================================
MINOR = {
    # Injury
    "minor cuts", "small wound", "bruise",
    "blister", "insect bite", "splinter",

    # Illness
    "cold", "cough", "sore throat", "runny nose",
    "sneezing", "mild fever", "flu symptoms",

    # Pain
    "headache", "light pain", "mild back pain",
    "mild stomach ache", "muscle ache",

    # Skin
    "skin irritation", "rash", "sunburn",
    "dry skin", "acne", "minor swelling",

    # Other
    "constipation", "mild diarrhea", "bloating",
    "eye irritation", "earache", "dizziness when standing"
}


# =========================================================
# CALCULATE PRIORITY
# =========================================================
def calculate_priority(patient):

    # =====================================================
    # SAFE VALUES
    # =====================================================
    symptoms = str(
        patient.symptoms
    ).lower().strip()

    pain = int(
        patient.pain_level
    )

    # =====================================================
    # SMART MATCH FUNCTION
    # =====================================================
    def match(group):

        return any(
            symptom in symptoms
            for symptom in group
        )

    # =====================================================
    # CRITICAL PRIORITY
    # =====================================================
    if match(CRITICAL):

        patient.status = "CRITICAL 🔴"

        return 1

    # =====================================================
    # URGENT PRIORITY
    # =====================================================
    elif match(URGENT):

        patient.status = "URGENT 🟠"

        return 3

    # =====================================================
    # MODERATE PRIORITY
    # =====================================================
    elif match(MODERATE):

        patient.status = "MODERATE 🟡"

        return 6

    # =====================================================
    # MINOR PRIORITY
    # =====================================================
    elif match(MINOR):

        patient.status = "MINOR 🟢"

        return 9

    # =====================================================
    # FALLBACK: PAIN LEVEL
    # =====================================================
    if pain >= 8:

        patient.status = "CRITICAL 🔴"

        return 1

    elif pain >= 6:

        patient.status = "URGENT 🟠"

        return 3

    elif pain >= 4:

        patient.status = "MODERATE 🟡"

        return 6

    else:

        patient.status = "MINOR 🟢"

        return 9