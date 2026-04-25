import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from groq import Groq
import streamlit as st
from enum import Enum
import logging
import time

logger = logging.getLogger(__name__)

class ModelTier(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary" 
    TERTIARY = "tertiary"
    FALLBACK = "fallback"

class ModelManager:
    """
    Manages AI model selection, fallback, and rate limits.
    Implements an agent-based approach for model management.
    """
    
    MODEL_CONFIG = {
        ModelTier.PRIMARY: {
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 2000,
            "temperature": 0.7
        },
        ModelTier.SECONDARY: {
            "model": "llama-3.1-8b-instant",
            "max_tokens": 2000,
            "temperature": 0.7
        },
        ModelTier.TERTIARY: {
            "model": "gemma2-9b-it",
            "max_tokens": 2000,
            "temperature": 0.7
        },
        ModelTier.FALLBACK: {
            "model": "llama-3.1-8b-instant",
            "max_tokens": 2000,
            "temperature": 0.7
        }
    }
    
    def __init__(self):
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Groq API client."""
        try:
            api_key = st.secrets["GROQ_API_KEY"]
            self.client = Groq(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")

    def generate_analysis(self, data, system_prompt, retry_count=0):
        """
        Generate analysis using the best available model with automatic fallback.
        Implements agent-based decision making for model selection.
        """
        if retry_count > 3:
            return {"success": False, "error": "All models failed after multiple retries"}

        if retry_count == 0:
            tier = ModelTier.PRIMARY
        elif retry_count == 1:
            tier = ModelTier.SECONDARY
        elif retry_count == 2:
            tier = ModelTier.TERTIARY
        else:
            tier = ModelTier.FALLBACK
            
        model_config = self.MODEL_CONFIG[tier]
        model = model_config["model"]
        
        if self.client is None:
            logger.error("No Groq client available")
            return self.generate_analysis(data, system_prompt, retry_count + 1)
            
        try:
            logger.info(f"Attempting generation with Groq model: {model}")
            
            full_prompt = f"{system_prompt}\n\nData:\n{str(data)}"
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": str(data)}
                ],
                temperature=model_config["temperature"],
                max_tokens=model_config["max_tokens"]
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model_used": f"groq/{model}"
            }
            
        except Exception as e:
            error_message = str(e).lower()
            logger.warning(f"Model {model} failed: {error_message}")
            
            if "rate limit" in error_message or "quota" in error_message:
                time.sleep(2)
            
            return self.generate_analysis(data, system_prompt, retry_count + 1)
            
        return {"success": False, "error": "Analysis failed with all available models"}
