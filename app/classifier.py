import yaml
import os
from typing import Dict, Any, Optional

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load the YAML configuration file"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_available_configs(self) -> list:
        """Return list of available configuration names"""
        return list(self.config['configurations'].keys())
    
    def validate_config_name(self, config_name: str) -> bool:
        """Validate if config_name exists"""
        return config_name in self.get_available_configs()
    
    def get_prompt_config(self, config_name: Optional[str] = None) -> Dict[str, Any]:
        """Get prompt configuration with basic validation"""
        config_name = config_name or self.config['classifier']['active_config']
        
        if not self.validate_config_name(config_name):
            available = self.get_available_configs()
            raise ValueError(
                f"Invalid config_name '{config_name}'. "
                f"Must be one of: {', '.join(available)}"
            )
            
        config = self.config['configurations'][config_name]
        prompt_path = os.path.join(
            os.path.dirname(self.config_path),
            config['prompt_file']
        )
        
        with open(prompt_path, 'r') as f:
            prompt_config = yaml.safe_load(f)
        
        return {
            'system': prompt_config['system'],
            'user_template': prompt_config['user'],
            'classes': config['classes']
        }