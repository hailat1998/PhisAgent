import React, { useState, useRef, useEffect } from 'react';
import { SendHorizontal } from 'lucide-react';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatProps {
  initialMessages?: Message[];
}

function ChatApp({ initialMessages = [] }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>(
    initialMessages.length > 0
      ? initialMessages
      : [
          { id: 2, text: 'Hi there! How can I help you?', sender: 'bot', timestamp: new Date() },
        ]
  );
  const [inputText, setInputText] = useState<string>('');
  const [sliderValues, setSliderValues] = useState(Array(6).fill(0));
  const [username, setUsername] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSliderChange = (index: number, value: number) => {
    const newValues = [...sliderValues];
    newValues[index] = parseFloat((value / 10).toFixed(1));
    setSliderValues(newValues);
  };

  const handleSend = async (): Promise<void> => {
    if (!inputText.trim() || !username.trim()) {
      alert('Please enter both a message and a username.');
      return;
    }

    const newMessage: Message = {
      id: messages.length + 1,
      text: inputText.trim(),
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInputText('');

    const payload = {
      username: username.trim(),
      message: newMessage.text,
      competence: sliderValues[0] / 7,
      certainty: sliderValues[1] / 7,
      affiliation: sliderValues[2] / 7,
      arousal: sliderValues[3] / 7,
      resolution: sliderValues[4] / 7,
      selection_threshold: sliderValues[5] / 7,
    };

    try {
      const response = await fetch('http://localhost:8000/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages((prev) => [
          ...prev,
          {
            id: prev.length + 1,
            text: data.message,
            sender: 'bot',
            timestamp: new Date(),
          },
        ]);
      } else {
        alert(`Failed to send data. Status: ${response.status}`);
      }
    } catch (error) {
      alert(`Error sending request: ${error}`);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  function calculateAnger(
    competence: number,
    certainty: number,
    affiliation: number,
    arousal: number,
    resolution: number,
    selection_threshold: number
): number {
    // Normalize inputs by dividing by 7
    const normalizedCompetence = competence / 7;
    const normalizedCertainty = certainty / 7;
    const normalizedAffiliation = affiliation / 7;
    const normalizedArousal = arousal / 7;
    const normalizedResolution = resolution / 7;
    const normalSelectionThreshold = selection_threshold / 7
    
    // Calculate anger value
    let angerValue = (
        (normalizedCompetence * 0.2) +
        (normalizedCertainty * 0.2) +
        (normalizedArousal * 0.3) +
        (-normalizedAffiliation * 0.15) +
        (-normalizedResolution * 0.15) + 
        (normalSelectionThreshold * 0.5)
    ) * 5;
   return angerValue;
}

function calculateSadness(
    competence: number,
    certainty: number,
    affiliation: number,
    arousal: number,
    resolution: number,
    selection_threshold: number
): number {
    // Normalize inputs by dividing by 7
    const normalizedCompetence = competence / 7;
    const normalizedCertainty = certainty / 7;
    const normalizedAffiliation = affiliation / 7;
    const normalizedArousal = arousal / 7;
    const normalizedResolution = resolution / 7;
    const normalSelectionThreshold = selection_threshold / 7

    // Calculate sadness value
    let sadnessValue = (
        (-normalizedCompetence * 0.25) +    // Lower competence increases sadness
        (-normalizedCertainty * 0.2) +      // Lower certainty increases sadness
        (-normalizedArousal * 0.15) +       // Lower arousal increases sadness
        (-normalizedAffiliation * 0.25) +   // Lower affiliation increases sadness
        (-normalizedResolution * 0.15) +    // Lower resolution increases sadness
        (normalSelectionThreshold * 0.5)     // Higher selection threshold increases sadness
    ) * 5;

    return sadnessValue;
}

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="bg-blue-600 text-white py-4 px-6 text-center shadow-md">
        <h1 className="text-2xl font-bold">AI Chatbot with Emotion Awareness</h1>
      </div>

      <div className="flex justify-center p-4">
        <input
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Sliders Section */}
        <div className="w-64 bg-white p-4 border-r border-gray-200 overflow-y-auto">
          <div className="space-y-4">
            {['competence', 'certainty', 'affiliation', 'arousal', 'resolution', 'selection_threshold'].map(
              (label, index) => (
                <div key={label} className="flex flex-col">
                  <div className="flex justify-between items-center mb-1">
                    <label className="text-sm text-gray-600">{label}</label>
                    <span className="text-sm text-blue-600 font-medium">{sliderValues[index].toFixed(1)}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="70"
                    step="1"
                    value={sliderValues[index] * 10}
                    onChange={(e) => handleSliderChange(index, Number(e.target.value))}
                    className="accent-blue-500"
                  />
                  <div className="flex justify-between text-xs text-gray-400 px-1">
                    <span>0.0</span>
                    <span>7.0</span>
                  </div>
                </div>
              )
            )}
          </div>
        </div>

        {/* Chat Section */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="flex flex-col">
                  <div
                    className={`max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl rounded-lg px-4 py-2 ${
                      message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
                    }`}
                  >
                    {message.text}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input area */}
          <div className="border-t border-gray-200 p-4 bg-white">
            <div className="flex items-center space-x-2 max-w-4xl mx-auto">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type a message..."
                className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleSend}
                className="bg-blue-500 text-white rounded-full p-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                <SendHorizontal size={20} />
              </button>
            </div>
          </div>
        </div>

        {/* Anger and Sadness Section */}
        <div className="w-32 bg-white p-4 border-l border-gray-200">
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-lg font-medium text-gray-800">Anger</span>
              <span className="text-blue-600 font-medium">{
                calculateAnger(
                              sliderValues[0],
                              sliderValues[1],
                              sliderValues[2],
                              sliderValues[3], 
                              sliderValues[4],
                              sliderValues[5]
                              ).toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-lg font-medium text-gray-800">Sadness</span>
              <span className="text-blue-600 font-medium">{
                calculateSadness(
                              sliderValues[0],
                              sliderValues[1],
                              sliderValues[2],
                              sliderValues[3], 
                              sliderValues[4],
                              sliderValues[5]
                             ).toFixed(2)
                }</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
  
}

export default ChatApp;
