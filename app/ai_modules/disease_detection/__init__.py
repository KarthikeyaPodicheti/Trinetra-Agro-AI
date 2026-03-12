"""
Trinetra Agro AI - Crop Disease Detection Module
Uses OpenCV colour / texture heuristics (no TensorFlow required).
"""

import os
import numpy as np
import cv2


class DiseaseDetector:
    """
    Crop Disease Detection using OpenCV colour-analysis heuristics.
    Works without GPU or heavy ML frameworks.
    """

    DISEASE_CLASSES = {
        'tomato': [
            'Healthy', 'Bacterial Spot', 'Early Blight', 'Late Blight',
            'Leaf Mold', 'Septoria Leaf Spot', 'Spider Mites',
            'Target Spot', 'Mosaic Virus', 'Yellow Leaf Curl Virus'
        ],
        'potato': [
            'Healthy', 'Early Blight', 'Late Blight', 'Black Rot',
            'Bacterial Wilt', 'Mosaic Virus'
        ],
        'rice': [
            'Healthy', 'Bacterial Leaf Blight', 'Blast', 'Brown Spot',
            'Sheath Blight', 'False Smut'
        ],
        'wheat': [
            'Healthy', 'Rust', 'Powdery Mildew', 'Leaf Blight',
            'Loose Smut', 'Karnal Bunt'
        ],
        'cotton': [
            'Healthy', 'Bacterial Blight', 'Cotton Wilt', 'Leaf Curl',
            'Boll Rot', 'Anthracnose'
        ],
        'corn': [
            'Healthy', 'Northern Leaf Blight', 'Common Rust',
            'Southern Leaf Blight', 'Eye Spot', 'Gray Leaf Spot'
        ],
        'maize': [
            'Healthy', 'Northern Leaf Blight', 'Common Rust',
            'Southern Leaf Blight', 'Eye Spot', 'Gray Leaf Spot'
        ],
    }

    def __init__(self):
        self.img_size = (224, 224)

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------
    def detect_disease(self, image_path: str, crop_type: str = 'tomato') -> dict:
        """Detect disease from a leaf image on disk."""
        if not os.path.exists(image_path):
            return {'success': False, 'error': f'Image not found: {image_path}'}

        disease_classes = self.DISEASE_CLASSES.get(
            crop_type.lower(), self.DISEASE_CLASSES['tomato'])

        return self._detect(image_path, disease_classes)

    def detect_disease_bytes(self, image_bytes: bytes, crop_type: str = 'tomato') -> dict:
        """Detect disease from raw image bytes (e.g. Streamlit upload)."""
        disease_classes = self.DISEASE_CLASSES.get(
            crop_type.lower(), self.DISEASE_CLASSES['tomato'])

        arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if image is None:
            return {'success': False, 'error': 'Could not decode image'}

        return self._analyse_image(image, disease_classes)

    # ------------------------------------------------------------------
    # internal
    # ------------------------------------------------------------------
    def _detect(self, image_path, disease_classes):
        image = cv2.imread(image_path)
        if image is None:
            return {'success': False, 'error': 'Could not read image'}
        return self._analyse_image(image, disease_classes)

    def _analyse_image(self, image, disease_classes):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_bgr = np.mean(image, axis=(0, 1))

        # Yellow / brown spots
        lower_yellow = np.array([15, 40, 40])
        upper_yellow = np.array([35, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        yellow_ratio = float(np.sum(yellow_mask > 0) / yellow_mask.size)

        # Dark spots
        dark_ratio = float(np.sum(gray < 50) / gray.size)

        # White / powdery patches
        white_ratio = float(np.sum(gray > 220) / gray.size)

        # Green-ness
        green_ratio = float(mean_bgr[1] / (mean_bgr[0] + mean_bgr[2] + 1))

        # Brown patches (H 10-20)
        lower_brown = np.array([8, 50, 30])
        upper_brown = np.array([20, 255, 200])
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
        brown_ratio = float(np.sum(brown_mask > 0) / brown_mask.size)

        issues = []
        if yellow_ratio > 0.08:
            issues.append('yellowing')
        if dark_ratio > 0.04:
            issues.append('dark_spots')
        if white_ratio > 0.10:
            issues.append('powdery')
        if brown_ratio > 0.12:
            issues.append('browning')

        # Classify
        if not issues and green_ratio > 1.2:
            disease = 'Healthy'
            confidence = 0.88
        elif 'yellowing' in issues and 'dark_spots' in issues:
            disease = disease_classes[min(3, len(disease_classes) - 1)]  # e.g. Late Blight
            confidence = 0.78
        elif 'yellowing' in issues:
            disease = disease_classes[min(2, len(disease_classes) - 1)]
            confidence = 0.72
        elif 'dark_spots' in issues:
            disease = disease_classes[min(1, len(disease_classes) - 1)]
            confidence = 0.70
        elif 'powdery' in issues:
            idx = next((i for i, d in enumerate(disease_classes)
                        if 'mildew' in d.lower() or 'mold' in d.lower()), 4)
            disease = disease_classes[min(idx, len(disease_classes) - 1)]
            confidence = 0.68
        elif 'browning' in issues:
            disease = disease_classes[min(3, len(disease_classes) - 1)]
            confidence = 0.65
        else:
            disease = disease_classes[min(1, len(disease_classes) - 1)]
            confidence = 0.55

        severity = self._severity(confidence)

        return {
            'success': True,
            'disease': disease,
            'confidence': round(confidence, 2),
            'severity': severity,
            'analysis': {
                'yellow_ratio': round(yellow_ratio, 3),
                'dark_ratio': round(dark_ratio, 3),
                'brown_ratio': round(brown_ratio, 3),
                'green_ratio': round(green_ratio, 3),
                'detected_issues': issues,
            },
            'recommendation': self._get_recommendation(disease),
            'prevention_tips': self._get_prevention_tips(disease),
        }

    @staticmethod
    def _severity(conf):
        if conf > 0.85:
            return "Critical — Immediate action required!"
        elif conf > 0.70:
            return "High — Treatment recommended within 24-48 hours"
        elif conf > 0.55:
            return "Moderate — Monitor closely and treat soon"
        return "Low — Continue monitoring"

    # ------------------------------------------------------------------
    # Recommendations DB
    # ------------------------------------------------------------------
    _RECS = {
        'Healthy': "🌟 Crop looks healthy! Continue current practices and monitor regularly.",
        'Bacterial Spot': "🔴 Apply copper-based bactericide. Remove infected leaves. Improve air circulation.",
        'Early Blight': "🟠 Apply chlorothalonil or copper fungicide. Remove lower infected leaves. Mulch.",
        'Late Blight': "🔴 URGENT — Apply metalaxyl or mancozeb immediately! Remove & destroy infected plants.",
        'Leaf Mold': "🟡 Improve ventilation. Reduce humidity. Apply sulfur-based fungicide.",
        'Septoria Leaf Spot': "🟠 Remove infected leaves. Apply fungicide (chlorothalonil). Avoid overhead watering.",
        'Spider Mites': "🟡 Spray with strong water stream. Apply neem oil. Introduce predatory mites.",
        'Target Spot': "🟠 Apply fungicide. Improve drainage. Remove plant debris. Rotate crops.",
        'Mosaic Virus': "🔴 Remove infected plants. Control aphids. Use resistant varieties.",
        'Yellow Leaf Curl Virus': "🔴 Control whiteflies with yellow sticky traps. Remove infected plants.",
        'Blast': "🟠 Apply tricyclazole. Improve drainage. Avoid excess nitrogen.",
        'Brown Spot': "🟡 Apply fungicide. Ensure proper nutrition. Improve drainage.",
        'Rust': "🟡 Apply sulfur or copper fungicide. Remove infected leaves.",
        'Powdery Mildew': "🟡 Apply sulfur-based fungicide. Improve air circulation.",
        'Bacterial Leaf Blight': "🔴 Use resistant varieties. Apply copper-based sprays.",
        'Sheath Blight': "🟠 Apply validamycin. Maintain proper spacing.",
        'False Smut': "🟡 Apply propiconazole at boot stage. Use clean seeds.",
        'Leaf Blight': "🟠 Apply mancozeb. Remove infected debris. Rotate crops.",
        'Loose Smut': "🟡 Use treated certified seeds. Apply systemic fungicide.",
        'Karnal Bunt': "🟡 Use resistant varieties. Seed treatment with fungicide.",
        'Bacterial Blight': "🔴 Apply streptocycline + copper spray. Remove diseased plants.",
        'Cotton Wilt': "🔴 Use resistant varieties. Practice crop rotation.",
        'Leaf Curl': "🟠 Control whiteflies. Remove infected plants early.",
        'Boll Rot': "🟠 Improve drainage. Apply copper-based fungicide.",
        'Anthracnose': "🟡 Apply mancozeb. Remove infected debris.",
        'Northern Leaf Blight': "🟠 Use resistant hybrids. Apply fungicide.",
        'Common Rust': "🟡 Apply fungicide at early stage. Use resistant varieties.",
        'Southern Leaf Blight': "🟠 Rotate crops. Remove crop residues.",
        'Eye Spot': "🟡 Apply fungicide. Ensure proper spacing.",
        'Gray Leaf Spot': "🟡 Use resistant hybrids. Rotate crops.",
        'Black Rot': "🔴 Remove infected tubers. Apply copper fungicide.",
        'Bacterial Wilt': "🔴 Remove wilted plants. Do not plant potatoes for 3 years.",
    }

    def _get_recommendation(self, disease):
        return self._RECS.get(disease,
            "📞 Consult your local agricultural extension officer for advice.")

    _TIPS = {
        'Healthy': ['Continue regular monitoring', 'Maintain proper nutrition',
                     'Follow good agricultural practices'],
    }

    def _get_prevention_tips(self, disease):
        return self._TIPS.get(disease, [
            'Practice crop rotation',
            'Use disease-resistant varieties',
            'Maintain field sanitation',
            'Monitor crops regularly',
            'Ensure proper nutrition',
        ])


def create_disease_detector() -> DiseaseDetector:
    return DiseaseDetector()
