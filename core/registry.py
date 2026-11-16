from core.effects import Delay, Echo

EFFECTS = {

    "delay": {
        "class": Delay,

        "params": {

            "delay_samples": {"min": 0, "max": 20000, "default": 300, "type": "int"},
            "feedback": {"min": 0.0, "max": 0.95, "default": 0.5, "type": "float"},
            "mix": {"min": 0.0, "max": 1.0, "default": 1.0, "type": "float"},
        
        },
    },

    "echo": {

        "class": Echo,
        "params": {

            "delay_samples": {"min": 1, "max": 20000, "default": 3000, "type": "int"},
            "decay": {"min": 0.0, "max": 0.95, "default": 0.3, "type": "float"},
            "num_echoes": {"min": 1, "max": 20, "default": 10, "type": "int"},
            "mix": {"min": 0.0, "max": 1.0, "default": 1.0, "type": "float"},
        
        },
    },
}