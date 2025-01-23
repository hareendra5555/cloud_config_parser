import json
import sys
from datetime import datetime

class CloudConfigParser:
    def __init__(self, config_file):
        """Initialize the config parser with a file path."""
        self.config_file = config_file
        self.config_data = None
        
    def read_config(self):
        """Read and parse the JSON configuration file."""
        try:
            with open(self.config_file, 'r') as file:
                self.config_data = json.load(file)
            return True
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_file}' not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{self.config_file}'.")
            return False
        
    def validate_config(self):
        """Validate the required configuration fields."""
        required_fields = ['app_name', 'environment', 'resources']
        
        if not self.config_data:
            print("Error: No configuration data loaded.")
            return False
            
        for field in required_fields:
            if field not in self.config_data:
                print(f"Error: Required field '{field}' missing in configuration.")
                return False
                
        # Validate resources structure
        if not isinstance(self.config_data['resources'], dict):
            print("Error: 'resources' must be an object.")
            return False
            
        return True
        
    def get_resource_summary(self):
        """Generate a summary of configured resources."""
        if not self.config_data:
            return None
            
        summary = {
            'total_resources': len(self.config_data['resources']),
            'resource_types': list(self.config_data['resources'].keys()),
            'environment': self.config_data['environment']
        }
        return summary
        
    def log_config_access(self):
        """Log the configuration access with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Accessed configuration for {self.config_data['app_name']}\n"
        
        with open('config_access.log', 'a') as log_file:
            log_file.write(log_entry)

def main():
    # Check if config file is provided as command line argument
    if len(sys.argv) != 2:
        print("Usage: python config_parser.py <config_file>")
        sys.exit(1)
        
    config_file = sys.argv[1]
    parser = CloudConfigParser(config_file)
    
    # Read and validate configuration
    if not parser.read_config():
        sys.exit(1)
        
    if not parser.validate_config():
        sys.exit(1)
        
    # Get and display resource summary
    summary = parser.get_resource_summary()
    print("\nConfiguration Summary:")
    print(f"Application: {parser.config_data['app_name']}")
    print(f"Environment: {summary['environment']}")
    print(f"Total Resources: {summary['total_resources']}")
    print("Resource Types:", ", ".join(summary['resource_types']))
    
    # Log the access
    parser.log_config_access()

if __name__ == "__main__":
    main()