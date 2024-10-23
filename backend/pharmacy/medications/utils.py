# utils.py

from .models import Refill

def get_refill_summary():
    """
    Utility function to calculate the dashboard data for refills.
    """
    # Get all refills
    total_refills = Refill.objects.all()

    # Count total prescriptions requested and completed
    requested_count = total_refills.count()
    completed_count = total_refills.filter(status='completed').count()

    # Count pending refills
    pending_count = total_refills.filter(status='pending').count()

    # Return the data as a dictionary
    return {
        'requested_count': requested_count,
        'completed_refills': completed_count,
        'pending_refills': pending_count
    }
