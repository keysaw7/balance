"""
Service de détection et gestion des langues
Support: Français, Anglais, Arabe
"""
from typing import Tuple, Optional
import re


def detect_language(text: str) -> str:
    """
    Détecte la langue d'un texte de manière simple.
    
    Returns:
        'fr', 'en', 'ar', ou 'unknown'
    """
    text = text.strip().lower()
    
    # Détection Arabe (caractères arabes)
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    if arabic_pattern.search(text):
        return 'ar'
    
    # Mots communs français
    french_words = ['je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles', 
                    'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du',
                    'pour', 'avec', 'dans', 'sur', 'par', 'plus', 'très',
                    'veux', 'voudrais', 'faut', 'besoin', 'avoir', 'être']
    
    # Mots communs anglais
    english_words = ['the', 'is', 'are', 'was', 'were', 'have', 'has', 'had',
                     'do', 'does', 'did', 'will', 'would', 'can', 'could',
                     'should', 'want', 'need', 'get', 'make', 'more', 'very',
                     'we', 'they', 'this', 'that', 'these', 'those']
    
    words = text.split()
    
    french_count = sum(1 for word in words if word in french_words)
    english_count = sum(1 for word in words if word in english_words)
    
    if french_count > english_count:
        return 'fr'
    elif english_count > 0:
        return 'en'
    
    return 'unknown'


def get_normalization_prompt(language: str) -> Tuple[str, str]:
    """
    Retourne le prompt système et utilisateur selon la langue.
    
    Returns:
        (system_prompt, user_prompt_template)
    """
    if language == 'ar':
        return (
            "أنت خبير في توحيد طلبات المواطنين. يجب عليك إنتاج تعبيرات قصيرة ودقيقة ومهنية.",
            """حوّل الفكرة التالية إلى تعبير موحد من 3-5 كلمات كحد أقصى.
- الشكل: "فعل + موضوع" (مثال: "بناء مسبح بلدي", "تطوير مسارات الدراجات")
- أسلوب محترف ومحايد
- كتابة الحرف الأول فقط بحرف كبير
- بدون علامات ترقيم نهائية

الفكرة: "{text}"

التعبير الموحد:"""
        )
    elif language == 'en':
        return (
            "You are an expert at normalizing citizen requests. You must produce short, precise and professional expressions.",
            """Transform the following idea into a normalized expression of 3-5 words maximum.
- Format: "Action + Subject" (ex: "Municipal pool construction", "Bike lane development")
- Professional and neutral style
- Capitalize first letter only
- No final punctuation

Idea: "{text}"

Normalized expression:"""
        )
    else:  # French (default)
        return (
            "Tu es un expert en normalisation de requêtes citoyennes. Tu dois produire des expressions courtes, précises et professionnelles.",
            """Transforme l'idée suivante en une expression normalisée de 3-5 mots maximum.
- Format: "Action + Sujet" (ex: "Construction piscine municipale", "Développement pistes cyclables")
- Style professionnel et neutre
- Capitaliser la première lettre uniquement
- Pas de ponctuation finale

Idée: "{text}"

Expression normalisée:"""
        )


def translate_ui_text(key: str, language: str) -> str:
    """
    Traduit un texte de l'interface selon la langue.
    """
    translations = {
        'ideas_grouped': {
            'fr': 'Les idées similaires sont regroupées automatiquement par l\'IA',
            'en': 'Similar ideas are automatically grouped by AI',
            'ar': 'يتم تجميع الأفكار المتشابهة تلقائياً بواسطة الذكاء الاصطناعي'
        },
        'unique_ideas': {
            'fr': 'Idées uniques',
            'en': 'Unique ideas',
            'ar': 'أفكار فريدة'
        },
        'total_contributions': {
            'fr': 'Contributions totales',
            'en': 'Total contributions',
            'ar': 'المساهمات الكلية'
        },
        'person': {
            'fr': 'personne',
            'en': 'person',
            'ar': 'شخص'
        },
        'people': {
            'fr': 'personnes',
            'en': 'people',
            'ar': 'أشخاص'
        }
    }
    
    return translations.get(key, {}).get(language, translations.get(key, {}).get('fr', ''))

