from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .services.prediction_service import PredictionService
from io import StringIO
import pandas as pd
import io
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'predictions', 'models', 'titanic_model.pkl')
scaler_path = os.path.join(BASE_DIR, 'predictions', 'models', 'scaler.pkl')

def swagger_docs(request):
    file_path = os.path.join(BASE_DIR, 'predictions', 'static', 'predictions', 'docs', 'index.html')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Ensure the correct encoding is used
            return HttpResponse(file.read(), content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("The file index.html was not found.", status=404)

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    prediction_service = PredictionService(model, scaler)
except FileNotFoundError as e:
    model = None
    scaler = None
    prediction_service = None
    print(f"Error loading model or scaler: {e}")

def index(request):
    return render(request, 'predictions/index.html')

def predict(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            data = prediction_service.process_file(request.FILES['file'])

            request.session['processed_data'] = data.to_json(orient='split')

            html_table = data.to_html(index=False, classes="table table-bordered")
            return render(request, 'predictions/show_table.html', {'html_table': html_table})

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': "No file was uploaded or the method is not POST."}, status=400)

def download_excel(request):
    processed_data = request.session.get('processed_data')
    if processed_data:
        processed_data_io = io.StringIO(processed_data)
        data = pd.read_json(processed_data_io, orient='split')
        
        excel_buffer = io.BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            data.to_excel(writer, index=False, sheet_name='Predictions')
        
        excel_buffer.seek(0)
        
        response = HttpResponse(
            excel_buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="predictions.xlsx"'
        
        return response

    return JsonResponse({'error': "No data available for download."}, status=400)
