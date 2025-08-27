#!/bin/bash

# AI/ML Feature Integration Service - Quick Demo Script

echo "🚀 AI/ML Feature Integration Service Demo"
echo "========================================="

# Check if server is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Server not running. Please start with: python main.py"
    exit 1
fi

echo "✅ Server is running!"
echo

# Test 1: Service Info
echo "1. 📋 Service Information:"
curl -s http://localhost:8000/ | python -m json.tool
echo -e "\n"

# Test 2: Sentiment Analysis
echo "2. 😊 Sentiment Analysis:"
curl -s -X POST "http://localhost:8000/api/v1/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this amazing product! It works perfectly.", "analysis_type": "sentiment"}' | python -m json.tool
echo -e "\n"

# Test 3: Comprehensive Analysis
echo "3. 📊 Comprehensive Text Analysis:"
curl -s -X POST "http://localhost:8000/api/v1/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a comprehensive analysis of sample text. It includes multiple sentences and various words.", "analysis_type": "comprehensive"}' | python -m json.tool
echo -e "\n"

# Test 4: Batch Analysis
echo "4. 🔄 Batch Analysis:"
curl -s -X POST "http://localhost:8000/api/v1/analyze/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Excellent service!", "Poor quality product", "Average experience"], "analysis_type": "sentiment"}' | python -m json.tool
echo -e "\n"

# Test 5: Create and analyze CSV file
echo "5. 📄 CSV File Analysis:"
echo -e "name,age,city,rating\nJohn,25,NYC,5\nJane,30,LA,4\nBob,35,Chicago,3" > /tmp/demo_data.csv
curl -s -X POST "http://localhost:8000/api/v1/analyze/file" \
  -F "file=@/tmp/demo_data.csv" \
  -F "format_type=auto" \
  -F "analysis_type=data_format" | python -m json.tool
echo -e "\n"

# Test 6: JSON Analysis
echo "6. 🔗 JSON Analysis:"
echo '{"users": [{"name": "Alice", "sentiment": "positive"}, {"name": "Bob", "sentiment": "neutral"}]}' > /tmp/demo_data.json
curl -s -X POST "http://localhost:8000/api/v1/analyze/file" \
  -F "file=@/tmp/demo_data.json" \
  -F "format_type=auto" \
  -F "analysis_type=data_format" | python -m json.tool
echo -e "\n"

# Test 7: Model Information
echo "7. 🤖 Available Models:"
curl -s http://localhost:8000/api/v1/models/info | python -m json.tool
echo -e "\n"

# Cleanup
rm -f /tmp/demo_data.csv /tmp/demo_data.json

echo "✨ Demo completed successfully!"
echo "📚 For more examples, see examples/laravel_integration.md"
echo "🐳 To run with Docker: docker-compose up -d"