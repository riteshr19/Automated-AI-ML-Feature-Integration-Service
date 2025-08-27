# Quick Demo Commands

# 1. Start the service
python main.py

# 2. Test sentiment analysis
curl -X POST "http://localhost:8000/api/v1/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product! It works great.", "analysis_type": "sentiment"}'

# 3. Test comprehensive text analysis
curl -X POST "http://localhost:8000/api/v1/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a comprehensive analysis of a sample text.", "analysis_type": "comprehensive"}'

# 4. Test batch analysis
curl -X POST "http://localhost:8000/api/v1/analyze/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great product!", "Terrible service", "Average quality"], "analysis_type": "sentiment"}'

# 5. Test file upload (create a test file first)
echo "This is test content for analysis" > test.txt
curl -X POST "http://localhost:8000/api/v1/analyze/file" \
  -F "file=@test.txt" \
  -F "format_type=text" \
  -F "analysis_type=comprehensive"

# 6. Test CSV analysis
echo -e "name,age,city\nJohn,25,NYC\nJane,30,LA" > data.csv
curl -X POST "http://localhost:8000/api/v1/analyze/file" \
  -F "file=@data.csv" \
  -F "format_type=csv" \
  -F "analysis_type=data_format"

# 7. Test JSON analysis
echo '{"name": "John", "age": 30}' > data.json
curl -X POST "http://localhost:8000/api/v1/analyze/file" \
  -F "file=@data.json" \
  -F "format_type=auto" \
  -F "analysis_type=data_format"

# 8. Get model information
curl -X GET "http://localhost:8000/api/v1/models/info"

# 9. Health check
curl -X GET "http://localhost:8000/health"

# 10. Run with Docker
docker-compose up -d
