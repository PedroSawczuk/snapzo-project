from django.utils import timezone

def time_since(created_at):
    now = timezone.now()
    diff = now - created_at
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)} s atrás"
    elif seconds < 3600:
        return f"{int(seconds // 60)} m atrás"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} h atrás"
    else:
        return f"{int(seconds // 86400)} d atrás"
