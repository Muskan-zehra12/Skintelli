"""
Interpretation Module - LLM with RAG for Natural Language Explanation
Generates plain English explanations of diagnoses using local knowledge base
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class MedicalKnowledgeBase:
    """Local medical knowledge base for RAG"""
    
    def __init__(self, kb_path: str = None):
        self.kb_path = kb_path or "./data/medical_knowledge_base.json"
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict:
        """Load knowledge base from JSON"""
        try:
            kb_file = Path(self.kb_path)
            
            if kb_file.exists():
                with open(kb_file, 'r') as f:
                    kb = json.load(f)
                logger.info(f"Knowledge base loaded: {self.kb_path}")
                return kb
            else:
                logger.warning(f"Knowledge base not found: {self.kb_path}")
                return self._create_default_knowledge_base()
                
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            return self._create_default_knowledge_base()
    
    def _create_default_knowledge_base(self) -> Dict:
        """Create default knowledge base with medical information"""
        kb = {
            "Melanoma": {
                "description": "Most serious type of skin cancer with highest mortality rate",
                "characteristics": [
                    "Irregular borders",
                    "Multiple colors (brown, black, tan, red)",
                    "Size larger than a pencil eraser",
                    "Asymmetrical shape",
                    "May be itchy or bleeding"
                ],
                "risk_factors": [
                    "Excessive sun exposure",
                    "Fair skin tone",
                    "Family history",
                    "Multiple moles"
                ],
                "recommendation": "Urgent dermatology consultation recommended. Immediate professional evaluation required."
            },
            "Basal Cell Carcinoma": {
                "description": "Most common type of skin cancer, grows slowly",
                "characteristics": [
                    "Waxy, translucent bump",
                    "Pearly appearance",
                    "Bleeding or oozing center",
                    "Brown, black, or blue patches",
                    "Usually painless"
                ],
                "risk_factors": [
                    "Chronic sun exposure",
                    "Light skin",
                    "Age over 40"
                ],
                "recommendation": "Schedule dermatology appointment. Usually treatable with high success rate."
            },
            "Squamous Cell Carcinoma": {
                "description": "Second most common skin cancer, risk of spread if untreated",
                "characteristics": [
                    "Red or pink bump",
                    "Scaly or crusted surface",
                    "Tender when touched",
                    "May be bleeding or oozing",
                    "Often on sun-exposed areas"
                ],
                "risk_factors": [
                    "Sun exposure",
                    "Immunosuppression",
                    "Age over 50"
                ],
                "recommendation": "Medical evaluation recommended. Early treatment improves outcomes."
            },
            "Benign Keratosis": {
                "description": "Common, non-cancerous skin growth, harmless",
                "characteristics": [
                    "Brown, black, or tan waxy bumps",
                    "Raised and scaly appearance",
                    "Well-defined borders",
                    "Often appear in clusters",
                    "Slow growing"
                ],
                "risk_factors": [
                    "Age",
                    "Genetics",
                    "Sun exposure"
                ],
                "recommendation": "Generally benign, no treatment necessary unless for cosmetic reasons."
            },
            "Nevus": {
                "description": "Common mole, typically benign",
                "characteristics": [
                    "Brown, tan, or flesh-colored",
                    "Round or oval shape",
                    "Flat or slightly raised",
                    "Uniform color",
                    "May have hair"
                ],
                "risk_factors": [
                    "Genetics",
                    "Sun exposure"
                ],
                "recommendation": "Regular monitoring recommended. Watch for changes in size, color, or shape."
            }
        }
        
        return kb
    
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            kb_file = Path(self.kb_path)
            kb_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(kb_file, 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
            
            logger.info(f"Knowledge base saved: {self.kb_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving knowledge base: {e}")
            return False
    
    def retrieve_info(self, diagnosis: str) -> Optional[Dict]:
        """Retrieve information for a diagnosis"""
        return self.knowledge_base.get(diagnosis, None)
    
    def get_all_diagnoses(self) -> List[str]:
        """Get all known diagnoses"""
        return list(self.knowledge_base.keys())


class ExplanationGenerator:
    """Generate natural language explanations using RAG"""
    
    def __init__(self, knowledge_base: MedicalKnowledgeBase = None):
        self.kb = knowledge_base or MedicalKnowledgeBase()
    
    def generate_explanation(self,
                            diagnosis: str,
                            confidence: float,
                            class_probabilities: Dict[str, float] = None) -> str:
        """
        Generate explanation for diagnosis using RAG
        
        Args:
            diagnosis: Predicted diagnosis
            confidence: Confidence score (0-1)
            class_probabilities: Probabilities for all classes
            
        Returns:
            Natural language explanation
        """
        try:
            # Retrieve information from knowledge base
            info = self.kb.retrieve_info(diagnosis)
            
            if not info:
                return f"The model detected {diagnosis} with {confidence:.1%} confidence."
            
            explanation_parts = []
            
            # Start with diagnosis
            explanation_parts.append(
                f"The AI model identified this lesion as {diagnosis} with {confidence:.1%} confidence."
            )
            
            explanation_parts.append(f"\n{info['description']}")
            
            # Add characteristics
            if info.get('characteristics'):
                explanation_parts.append("\nKey characteristics observed:")
                for char in info['characteristics'][:3]:  # Top 3
                    explanation_parts.append(f"  • {char}")
            
            # Add risk factors
            if info.get('risk_factors'):
                explanation_parts.append("\nRisk factors associated with this condition:")
                for factor in info['risk_factors'][:2]:  # Top 2
                    explanation_parts.append(f"  • {factor}")
            
            # Add recommendation
            if info.get('recommendation'):
                explanation_parts.append(f"\n✓ Recommendation: {info['recommendation']}")
            
            # Add confidence disclaimer
            explanation_parts.append(
                "\n⚠️ DISCLAIMER: This analysis is for informational purposes only. "
                "Please consult a qualified dermatologist for professional medical advice."
            )
            
            explanation = "\n".join(explanation_parts)
            logger.info(f"Explanation generated for {diagnosis}")
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Unable to generate explanation for {diagnosis}."
    
    def generate_short_explanation(self, diagnosis: str, confidence: float) -> str:
        """Generate a short one-line explanation"""
        info = self.kb.retrieve_info(diagnosis)
        
        if info:
            return f"{diagnosis} ({confidence:.1%} confidence): {info['description']}"
        else:
            return f"{diagnosis} ({confidence:.1%} confidence)"


class LocalLLM:
    """
    Local Language Model for text generation
    Can use various backends (transformers, ollama, etc.)
    """
    
    def __init__(self, model_type: str = "mock"):
        self.model_type = model_type
        self.model = None
        self.initialized = False
    
    def load_model(self) -> bool:
        """Load language model"""
        try:
            if self.model_type == "mock":
                self.initialized = True
                logger.info("Mock LLM initialized")
                return True
            
            # Try to load transformers-based model
            try:
                from transformers import pipeline
                self.model = pipeline("text-generation", model="gpt2")
                self.initialized = True
                logger.info("Transformers LLM loaded")
                return True
            except ImportError:
                logger.warning("Transformers not available")
                return False
                
        except Exception as e:
            logger.error(f"Error loading LLM: {e}")
            return False
    
    def generate_text(self, prompt: str, max_length: int = 100) -> str:
        """Generate text using LLM"""
        if not self.initialized:
            logger.warning("LLM not initialized")
            return ""
        
        try:
            if self.model_type == "mock":
                # Mock generation
                return f"[Generated text for: {prompt}]"
            
            if self.model:
                output = self.model(prompt, max_length=max_length, num_return_sequences=1)
                return output[0]['generated_text']
                
        except Exception as e:
            logger.error(f"Error generating text: {e}")
        
        return ""


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test knowledge base
    kb = MedicalKnowledgeBase()
    kb.save_knowledge_base()
    
    # Test explanation generator
    generator = ExplanationGenerator(kb)
    explanation = generator.generate_explanation("Melanoma", 0.92)
    print(explanation)
    print("\n" + "="*80 + "\n")
    
    # Test short explanation
    short = generator.generate_short_explanation("Nevus", 0.78)
    print(short)
