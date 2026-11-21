import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import RiskCheck


def get_risk_level(score, attendance):
    """Same rule as the Streamlit app, now calculated in the backend."""
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"


@csrf_exempt
def check_risk(request):
    """POST: validate input, calculate risk level, save it, return the result."""
    if request.method != "POST":
        return JsonResponse({"error": "Use POST."}, status=405)

    try:
        data = json.loads(request.body)
        name = str(data["student_name"]).strip()
        score = int(data["score"])
        attendance = int(data["attendance"])
    except (KeyError, TypeError, ValueError):
        return JsonResponse({"error": "Invalid input."}, status=400)

    if name == "" or not (0 <= score <= 100) or not (0 <= attendance <= 100):
        return JsonResponse(
            {"error": "Name required; score and attendance must be 0-100."},
            status=400,
        )

    level = get_risk_level(score, attendance)

    RiskCheck.objects.create(
        student_name=name,
        score=score,
        attendance=attendance,
        risk_level=level,
    )

    return JsonResponse({
        "student_name": name,
        "score": score,
        "attendance": attendance,
        "risk_level": level,
    })


def history(request):
    """GET: return the 10 most recent risk checks (newest first)."""
    rows = RiskCheck.objects.order_by("-created_at")[:10]
    return JsonResponse({"history": [
        {
            "Student Name": r.student_name,
            "Score": r.score,
            "Attendance": r.attendance,
            "Risk Level": r.risk_level,
        }
        for r in rows
    ]})


@csrf_exempt
def clear_history(request):
    """POST: delete all saved risk checks."""
    if request.method != "POST":
        return JsonResponse({"error": "Use POST."}, status=405)

    deleted_count, _ = RiskCheck.objects.all().delete()
    return JsonResponse({"deleted": deleted_count})