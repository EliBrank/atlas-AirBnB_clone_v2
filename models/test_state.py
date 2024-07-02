# Test querying the State class directly

from models import storage
from models.state import State

# Ensure session is initialized
storage.reload()

# Print session details
print(f"Session: {storage._DBStorage__session}")

# Test querying the State class directly
try:
    session = storage._DBStorage__session
    print("Querying State class directly:")
    for state in session.query(State):
        print(f"Found state: {state}")
except Exception as e:
    print(f"Error querying State class: {e}")
