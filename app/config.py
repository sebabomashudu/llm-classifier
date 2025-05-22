# app/config.py
import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load and parse the YAML configuration file"""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value using dot notation
        Example: config.get('logging.level', 'INFO')
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def get_available_configs(self) -> list[str]:
        """Get list of available configuration names"""
        return list(self.config['configurations'].keys())
        
    def get_prompt_config(self, config_name: Optional[str] = None) -> Dict[str, Any]:
        """Get prompt configuration for a specific classifier"""
        config_name = config_name or self.get('classifier.active_config')
        config = self.get(f'configurations.{config_name}')
        
        if not config:
            raise ValueError(f"Configuration '{config_name}' not found")
            
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