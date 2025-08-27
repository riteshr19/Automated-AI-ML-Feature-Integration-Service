# AI/ML Feature Integration Service

A scalable Python microservice that uses AI/ML models to analyze unstructured data and provides a RESTful API for integration with other applications, including Laravel.

## Features

- **AI/ML Analysis**: Sentiment analysis, text statistics, and comprehensive data analysis
- **Multiple Data Formats**: Support for text, JSON, and CSV data
- **RESTful API**: Well-documented endpoints with OpenAPI/Swagger documentation
- **Scalable Architecture**: Built with FastAPI and Docker for high performance
- **Laravel Integration**: Ready-to-use examples for Laravel applications
- **Batch Processing**: Efficient batch analysis for multiple items
- **Error Handling**: Robust error handling and logging
- **Health Monitoring**: Health check endpoints for monitoring

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/riteshr19/Automated-AI-ML-Feature-Integration-Service.git
cd Automated-AI-ML-Feature-Integration-Service
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

3. Access the service:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Service Info: http://localhost:8000/

### Local Development

1. Install Python 3.11+ and create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
python main.py
```

## API Endpoints

### Text Analysis
- `POST /api/v1/analyze/text` - Analyze text content
- `POST /api/v1/analyze/file` - Analyze uploaded files
- `POST /api/v1/analyze/batch` - Batch analysis of multiple texts

### Service Information
- `GET /` - Service information and available endpoints
- `GET /health` - Health check
- `GET /api/v1/models/info` - Available models and capabilities

## Usage Examples

### Sentiment Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I love this product! It works great.",
    "analysis_type": "sentiment"
  }'
```

### Comprehensive Text Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a sample text for analysis.",
    "analysis_type": "comprehensive"
  }'
```

### File Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/file" \
  -F "file=@data.csv" \
  -F "format_type=csv" \
  -F "analysis_type=data_format"
```

### Batch Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Great product!", "Terrible service", "Average quality"],
    "analysis_type": "sentiment"
  }'
```

## Laravel Integration

The service is designed to integrate seamlessly with Laravel applications. See the [Laravel Integration Guide](examples/laravel_integration.md) for detailed examples including:

- PHP client service
- Laravel controllers
- Frontend JavaScript examples
- Configuration setup

## Supported Analysis Types

1. **Sentiment Analysis**: Determines emotional tone (positive, negative, neutral)
2. **Text Analysis**: Comprehensive text statistics and readability metrics
3. **Data Format Analysis**: Analyzes and processes CSV, JSON, and text data
4. **Comprehensive**: Combines multiple analysis types

## Supported Data Formats

- **Text**: Plain text content
- **JSON**: Structured JSON data
- **CSV**: Comma-separated values
- **Auto**: Automatic format detection

## Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Key configuration options:
- `API_HOST`: Service host (default: 0.0.0.0)
- `API_PORT`: Service port (default: 8000)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)
- `CORS_ORIGINS`: Allowed CORS origins for web integration

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
pytest tests/ -v
```

## Development

### Project Structure
```
├── app/
│   ├── api/          # API routes and models
│   ├── core/         # Core configuration
│   ├── ml/           # ML models and analyzers
│   └── utils/        # Utility functions
├── tests/            # Test suite
├── examples/         # Integration examples
├── main.py           # Application entry point
├── Dockerfile        # Docker configuration
└── docker-compose.yml
```

### Adding New Analyzers

1. Create a new analyzer class inheriting from `BaseAnalyzer`
2. Implement the `analyze()` method
3. Add the analyzer to the API routes
4. Update the model info endpoint

## Performance

The service is optimized for:
- **Scalability**: Async/await patterns and efficient resource usage
- **Reliability**: Comprehensive error handling and logging
- **Performance**: Caching and batch processing capabilities

## Docker Deployment

### Build and Run
```bash
# Build the image
docker build -t ai-ml-service .

# Run the container
docker run -p 8000:8000 ai-ml-service
```

### Production Deployment
```bash
# Use docker-compose for production
docker-compose -f docker-compose.yml up -d
```

## Monitoring and Logging

- Health check endpoint: `/health`
- Structured logging with Loguru
- Request/response logging
- Error tracking and reporting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions and support:
- Check the API documentation at `/docs`
- Review the examples in the `examples/` directory
- Create an issue for bugs or feature requests