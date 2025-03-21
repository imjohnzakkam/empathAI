'use client';

import { useState, useEffect } from 'react';
import Header from '../../components/ui/Header';

interface LLMConfig {
  current_provider: string | null;
  current_model: string | null;
  available_providers: Record<string, string>;
  is_using_llm: boolean;
}

interface TestResponse {
  detected_emotions: Record<string, number>;
  response_text: string;
}

export default function SettingsPage() {
  const [config, setConfig] = useState<LLMConfig | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [testMessage, setTestMessage] = useState<string>('');
  const [testResponse, setTestResponse] = useState<TestResponse | null>(null);
  const [isTesting, setIsTesting] = useState<boolean>(false);

  useEffect(() => {
    fetchLLMConfig();
  }, []);

  const fetchLLMConfig = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/llm/config');
      
      if (!response.ok) {
        throw new Error(`Error fetching LLM config: ${response.statusText}`);
      }
      
      const data = await response.json();
      setConfig(data);
    } catch (err) {
      setError(`Failed to load LLM configuration: ${err instanceof Error ? err.message : 'Unknown error'}`);
      console.error('Error fetching LLM config:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestLLM = async () => {
    if (!testMessage.trim()) {
      return;
    }
    
    setIsTesting(true);
    setTestResponse(null);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/analyze/text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: testMessage
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Error testing LLM: ${response.statusText}`);
      }
      
      const data = await response.json();
      setTestResponse(data);
    } catch (err) {
      setError(`Failed to test LLM: ${err instanceof Error ? err.message : 'Unknown error'}`);
      console.error('Error testing LLM:', err);
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-grow px-4 py-10 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">LLM Integration Settings</h1>
          
          {isLoading ? (
            <div className="card">
              <p className="text-center">Loading configuration...</p>
            </div>
          ) : error ? (
            <div className="card bg-red-50 border border-red-200 mb-6">
              <p className="text-red-700">{error}</p>
              <button 
                className="btn-primary mt-4" 
                onClick={fetchLLMConfig}
              >
                Retry
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="card">
                <h2 className="text-xl font-semibold mb-4">Current Configuration</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-gray-500 mb-1">LLM Provider</p>
                    <p className="font-medium">
                      {config?.current_provider || 'None (Using template-based responses)'}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-500 mb-1">Active Model</p>
                    <p className="font-medium">{config?.current_model || 'None'}</p>
                  </div>
                  <div>
                    <p className="text-gray-500 mb-1">Status</p>
                    <p className="font-medium">
                      {config?.is_using_llm 
                        ? <span className="text-green-600">Using LLM for responses</span>
                        : <span className="text-amber-600">Using static templates (No LLM)</span>
                      }
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="card">
                <h2 className="text-xl font-semibold mb-4">Available LLM Providers</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {config?.available_providers && Object.entries(config.available_providers).map(([id, name]) => (
                    <div key={id} className="p-3 border rounded-md">
                      <p className="font-medium">{name}</p>
                      <p className="text-sm text-gray-500">ID: {id}</p>
                    </div>
                  ))}
                </div>
                <div className="mt-4 p-4 bg-amber-50 rounded-md">
                  <p className="text-amber-800 text-sm">
                    <span className="font-medium">Note:</span> To change the LLM provider or model, edit the <code className="bg-amber-100 px-1 rounded">.env</code> file 
                    in the backend directory and restart the server.
                  </p>
                </div>
              </div>
              
              <div className="card">
                <h2 className="text-xl font-semibold mb-4">Test LLM Response</h2>
                <div className="mb-4">
                  <label htmlFor="test-message" className="block text-sm font-medium text-gray-700 mb-1">
                    Enter a message to test
                  </label>
                  <textarea 
                    id="test-message"
                    className="input-field min-h-[100px]"
                    value={testMessage}
                    onChange={(e) => setTestMessage(e.target.value)}
                    placeholder="Type a message to test the current LLM configuration..."
                  />
                </div>
                <div className="flex justify-end">
                  <button 
                    className="btn-primary"
                    onClick={handleTestLLM}
                    disabled={isTesting || !testMessage.trim()}
                  >
                    {isTesting ? 'Testing...' : 'Test Response'}
                  </button>
                </div>
                
                {testResponse && (
                  <div className="mt-6 border-t pt-4">
                    <h3 className="font-medium text-lg mb-3">Response</h3>
                    
                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Detected Emotions</h4>
                      <div className="flex flex-wrap gap-2">
                        {Object.entries(testResponse.detected_emotions).map(([emotion, score]) => (
                          <div 
                            key={emotion} 
                            className="px-2 py-1 bg-gray-100 rounded-full text-sm"
                          >
                            {emotion}: {typeof score === 'number' ? score.toFixed(2) : score}
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-2">AI Response</h4>
                      <div className="p-4 bg-indigo-50 rounded-md">
                        <p className="text-gray-800 whitespace-pre-line">{testResponse.response_text}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
} 