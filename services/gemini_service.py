import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import logging
import json
import requests
import time
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from config.settings import GEMINI_MODEL

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

def initialize_gemini(api_key: str) -> bool:
    """
    Validates that the API key is not empty.
    REST transport configuration requires no SDK initialization.
    """
    return bool(api_key)

def clean_json_text(text: str) -> str:
    """
    Extracts the raw JSON substring from markdown backticks or text wrapper.
    Prevents formatting garbage from breaking json.loads.
    """
    text = text.strip()
    
    # Strip markdown headers if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
        
    if text.endswith("```"):
        text = text[:-3]
        
    text = text.strip()
    
    # Locate first { and last } to isolate JSON if any conversational text slipped in
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    
    if first_brace != -1 and last_brace != -1:
        text = text[first_brace:last_brace + 1]
        
    return text

def generate_structured_data(
    prompt: str, 
    schema: Type[T], 
    api_key: str, 
    system_instruction: Optional[str] = None
) -> T:
    """
    Sends a prompt to Gemini 2.5 Flash (or fallback model) using raw HTTP REST calls and returns a parsed Pydantic schema object.
    Includes retry backoff logic and automatic model fallback for 503/429 temporary server errors.
    """
    if not api_key:
        raise ValueError("Gemini API key is missing. Please set it in config/settings.py or the sidebar.")
        
    model_name = GEMINI_MODEL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    # Generate JSON Schema from Pydantic model
    schema_json = json.dumps(schema.model_json_schema())
    
    enhanced_prompt = f"""
    You must output your response in JSON format.
    Your output MUST strictly conform to the following JSON Schema:
    {schema_json}
    
    Do NOT include any conversational introduction, explanation, or markdown wrappers. Only output the raw JSON object.
    
    Prompt details:
    {prompt}
    """
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": enhanced_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7
        }
    }
    
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [
                {"text": system_instruction}
            ]
        }
        
    # Retry loop for resilience
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, verify=False)
            
            if response.status_code == 200:
                res_data = response.json()
                # Extract text from response structure
                try:
                    text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError) as err:
                    logger.error(f"Failed to parse Gemini response structure: {res_data}")
                    raise Exception("Invalid response structure received from Gemini API.")
                    
                # Clean markdown codeblocks and parse JSON
                cleaned_text = clean_json_text(text)
                data = json.loads(cleaned_text)
                return schema.model_validate(data)
                
            elif response.status_code in [429, 503] and attempt < max_retries - 1:
                # Dynamic model fallback: if 2.5 flash is overloaded, switch to gemini-flash-latest immediately
                if "2.5" in model_name:
                    logger.warning(f"Gemini {model_name} overloaded. Falling back to gemini-flash-latest...")
                    model_name = "gemini-flash-latest"
                elif model_name == "gemini-flash-latest":
                    # If flash is also overloaded (rare), try gemini-pro-latest
                    logger.warning(f"Gemini flash overloaded. Falling back to gemini-pro-latest...")
                    model_name = "gemini-pro-latest"
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                wait_time = 2 * (attempt + 1)
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Gemini REST error {response.status_code}: {response.text}")
                raise Exception(f"Gemini API returned status code {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as req_err:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise req_err
        except Exception as e:
            logger.error(f"Gemini REST Structured Output generation failed: {e}")
            raise e

def generate_text(
    prompt: str, 
    api_key: str, 
    system_instruction: Optional[str] = None
) -> str:
    """
    Generates plain text response using raw HTTP REST calls with retry/fallback.
    """
    if not api_key:
        raise ValueError("Gemini API key is missing. Please set it in config/settings.py or the sidebar.")
        
    model_name = GEMINI_MODEL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7
        }
    }
    
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [
                {"text": system_instruction}
            ]
        }
        
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, verify=False)
            
            if response.status_code == 200:
                res_data = response.json()
                try:
                    text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    return text
                except (KeyError, IndexError):
                    logger.error(f"Failed to parse Gemini response structure: {res_data}")
                    raise Exception("Invalid response structure received from Gemini API.")
                    
            elif response.status_code in [429, 503] and attempt < max_retries - 1:
                if "2.5" in model_name:
                    model_name = "gemini-flash-latest"
                elif model_name == "gemini-flash-latest":
                    model_name = "gemini-pro-latest"
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                wait_time = 2 * (attempt + 1)
                time.sleep(wait_time)
                continue
            else:
                logger.error(f"Gemini REST error {response.status_code}: {response.text}")
                raise Exception(f"Gemini API returned status code {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as req_err:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise req_err
        except Exception as e:
            logger.error(f"Gemini REST Plain Text generation failed: {e}")
            raise e
