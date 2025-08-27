# Laravel Integration Examples

This directory contains examples of how to integrate the AI/ML microservice with a Laravel application.

## PHP Client Example

```php
<?php

namespace App\Services;

use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

class AIMLServiceClient
{
    private $client;
    private $baseUrl;

    public function __construct()
    {
        $this->baseUrl = config('services.aiml.url', 'http://localhost:8000');
        $this->client = new Client([
            'base_uri' => $this->baseUrl,
            'timeout' => 30,
            'headers' => [
                'Content-Type' => 'application/json',
                'Accept' => 'application/json',
            ]
        ]);
    }

    /**
     * Analyze text sentiment
     */
    public function analyzeSentiment(string $text): array
    {
        try {
            $response = $this->client->post('/api/v1/analyze/text', [
                'json' => [
                    'text' => $text,
                    'analysis_type' => 'sentiment'
                ]
            ]);

            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * Perform comprehensive text analysis
     */
    public function analyzeText(string $text): array
    {
        try {
            $response = $this->client->post('/api/v1/analyze/text', [
                'json' => [
                    'text' => $text,
                    'analysis_type' => 'comprehensive'
                ]
            ]);

            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * Analyze multiple texts in batch
     */
    public function batchAnalyze(array $texts, string $analysisType = 'comprehensive'): array
    {
        try {
            $response = $this->client->post('/api/v1/analyze/batch', [
                'json' => [
                    'texts' => $texts,
                    'analysis_type' => $analysisType
                ]
            ]);

            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }

    /**
     * Analyze uploaded file
     */
    public function analyzeFile($filePath, string $formatType = 'auto'): array
    {
        try {
            $response = $this->client->post('/api/v1/analyze/file', [
                'multipart' => [
                    [
                        'name' => 'file',
                        'contents' => fopen($filePath, 'r'),
                        'filename' => basename($filePath)
                    ],
                    [
                        'name' => 'format_type',
                        'contents' => $formatType
                    ],
                    [
                        'name' => 'analysis_type',
                        'contents' => 'comprehensive'
                    ]
                ]
            ]);

            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
}
```

## Laravel Controller Example

```php
<?php

namespace App\Http\Controllers;

use App\Services\AIMLServiceClient;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class TextAnalysisController extends Controller
{
    private $aimlClient;

    public function __construct(AIMLServiceClient $aimlClient)
    {
        $this->aimlClient = $aimlClient;
    }

    /**
     * Analyze text sentiment
     */
    public function analyzeSentiment(Request $request): JsonResponse
    {
        $request->validate([
            'text' => 'required|string|max:10000'
        ]);

        $result = $this->aimlClient->analyzeSentiment($request->text);

        return response()->json($result);
    }

    /**
     * Analyze uploaded file
     */
    public function analyzeFile(Request $request): JsonResponse
    {
        $request->validate([
            'file' => 'required|file|max:10240', // 10MB max
            'format_type' => 'sometimes|string|in:text,json,csv,auto'
        ]);

        $file = $request->file('file');
        $formatType = $request->input('format_type', 'auto');
        
        $result = $this->aimlClient->analyzeFile($file->getPathname(), $formatType);

        return response()->json($result);
    }

    /**
     * Batch analyze multiple texts
     */
    public function batchAnalyze(Request $request): JsonResponse
    {
        $request->validate([
            'texts' => 'required|array|min:1|max:100',
            'texts.*' => 'string|max:10000',
            'analysis_type' => 'sometimes|string|in:sentiment,text,comprehensive'
        ]);

        $analysisType = $request->input('analysis_type', 'comprehensive');
        $result = $this->aimlClient->batchAnalyze($request->texts, $analysisType);

        return response()->json($result);
    }
}
```

## Configuration

Add to your `config/services.php`:

```php
'aiml' => [
    'url' => env('AIML_SERVICE_URL', 'http://localhost:8000'),
    'timeout' => env('AIML_SERVICE_TIMEOUT', 30),
],
```

Add to your `.env`:

```
AIML_SERVICE_URL=http://localhost:8000
AIML_SERVICE_TIMEOUT=30
```

## Routes

Add to your `routes/api.php`:

```php
Route::prefix('analysis')->group(function () {
    Route::post('sentiment', [TextAnalysisController::class, 'analyzeSentiment']);
    Route::post('file', [TextAnalysisController::class, 'analyzeFile']);
    Route::post('batch', [TextAnalysisController::class, 'batchAnalyze']);
});
```

## Usage Examples

### Frontend JavaScript

```javascript
// Analyze text sentiment
async function analyzeSentiment(text) {
    try {
        const response = await fetch('/api/analysis/sentiment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({ text })
        });
        
        return await response.json();
    } catch (error) {
        console.error('Error analyzing sentiment:', error);
        return { success: false, error: error.message };
    }
}

// Analyze file
async function analyzeFile(file, formatType = 'auto') {
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('format_type', formatType);
        
        const response = await fetch('/api/analysis/file', {
            method: 'POST',
            headers: {
                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content
            },
            body: formData
        });
        
        return await response.json();
    } catch (error) {
        console.error('Error analyzing file:', error);
        return { success: false, error: error.message };
    }
}
```