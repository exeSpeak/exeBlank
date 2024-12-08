import handler_vars

# NOTE: THE FOLLOWING IS SPECIFIC TO VERY LARGE GAMES AND CAN BE DELETED BY USERS OF SMALLER TITLES
# MULTIPLE REQUEST THREADING

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, List, Optional
import queue
import threading
import time

class VarChangeType(Enum):
    SET = auto()      # Direct value set
    ADD = auto()      # Add to current value
    FLAG = auto()     # Boolean flag set
    CUSTOM = auto()   # Custom operation

class Priority(Enum):
    CRITICAL = 0    # Immediate processing (e.g., player health, game state)
    HIGH = 1        # Very important (e.g., enemy damage)
    MEDIUM = 2      # Standard importance (e.g., resource collection)
    LOW = 3         # Can be delayed (e.g., background updates)
    BACKGROUND = 4  # Lowest priority (e.g., statistics)

@dataclass
class VarChangeRequest:
    var_name: str                    # Name of variable to change
    change_type: VarChangeType       # Type of change
    value: Any                       # New value or amount to add
    priority: Priority               # Request priority
    callback: Optional[Callable]     # Optional callback after change
    timestamp: float                 # When the request was made
    
    def __lt__(self, other):
        # First compare by priority, then by timestamp
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.timestamp < other.timestamp

class ThreadedVarHandler:
    def __init__(self):
        self.request_queue = queue.PriorityQueue()
        self.processing_lock = threading.Lock()
        self.is_running = True
        self.processor_thread = threading.Thread(target=self._process_requests, daemon=True)
        self.processor_thread.start()
    
    def request_change(self, var_name: str, value: Any, 
                      change_type: VarChangeType = VarChangeType.SET,
                      priority: Priority = Priority.MEDIUM,
                      callback: Optional[Callable] = None) -> None:
        """
        Request a variable change
        :param var_name: Name of the variable to change
        :param value: New value or amount to add
        :param change_type: Type of change (SET, ADD, FLAG, CUSTOM)
        :param priority: Priority level for this change
        :param callback: Optional callback to execute after change
        """
        request = VarChangeRequest(
            var_name=var_name,
            change_type=change_type,
            value=value,
            priority=priority,
            callback=callback,
            timestamp=time.time()
        )
        self.request_queue.put(request)
    
    def _process_requests(self) -> None:
        """Process variable change requests in priority order"""
        while self.is_running:
            try:
                # Get the highest priority request
                request = self.request_queue.get(timeout=0.1)
                
                # Acquire lock for thread-safe variable modification
                with self.processing_lock:
                    self._apply_change(request)
                
                # Execute callback if provided
                if request.callback:
                    try:
                        request.callback()
                    except Exception as e:
                        print(f"Error in callback for {request.var_name}: {e}")
                
                self.request_queue.task_done()
                
            except queue.Empty:
                # No requests to process
                continue
            except Exception as e:
                print(f"Error processing variable change request: {e}")
    
    def _apply_change(self, request: VarChangeRequest) -> None:
        """Apply the requested variable change"""
        try:
            if request.change_type == VarChangeType.SET:
                handler_vars.vars_setMe(request.var_name, request.value)
            
            elif request.change_type == VarChangeType.ADD:
                handler_vars.vars_addMe(request.var_name, request.value)
            
            elif request.change_type == VarChangeType.FLAG:
                handler_vars.vars_setFlag(request.var_name, bool(request.value))
            
            elif request.change_type == VarChangeType.CUSTOM:
                # Custom operations should be provided as callable values
                if callable(request.value):
                    current_value = handler_vars.vars_getMe(request.var_name)
                    new_value = request.value(current_value)
                    handler_vars.vars_setMe(request.var_name, new_value)
        
        except Exception as e:
            print(f"Error applying change to {request.var_name}: {e}")
    
    def stop(self) -> None:
        """Stop the request processor thread"""
        self.is_running = False
        self.processor_thread.join()
    
    def get_queue_size(self) -> int:
        """Get the current size of the request queue"""
        return self.request_queue.qsize()
    
    def clear_queue(self) -> None:
        """Clear all pending requests"""
        while not self.request_queue.empty():
            try:
                self.request_queue.get_nowait()
                self.request_queue.task_done()
            except queue.Empty:
                break

# Global threaded var handler instance
var_handler = None

def get_var_handler() -> ThreadedVarHandler:
    """Get the global threaded var handler instance"""
    global var_handler
    if var_handler is None:
        var_handler = ThreadedVarHandler()
    return var_handler
