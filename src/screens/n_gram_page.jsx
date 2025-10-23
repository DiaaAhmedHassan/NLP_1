import React, { useState } from 'react'
import Prediction_card from '../components/prediction_card'

function N_gram_page() {

  const [sentence, setSentence] = useState('');
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = "http://localhost:8000";

  const handlePredict = async () => {
    if (!sentence.trim()) {
      setError('Please enter a sentence');
      return;
    }

    setLoading(true);
    setError('');
    setPredictions([]);

    try {
      const response = await fetch(`${API_URL}/predict-next`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sentence: sentence,
          top_k: 5,
          // model_name: 'bigram'
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setPredictions(data.predictions);
    } catch (err) {
      setError('Failed to get predictions: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handlePredict();
    }
  };


  return (
    <>
      <div className="mb-2 p-20 flex flex-col">
        <h1 className='flex flex-col items-center text-5xl mb-10 font-bold'>
          N-gram Model
        </h1>
        <label htmlFor="default-input" className="block mb-2 mt-15 text-xl outline-amber font-medium text-gray-900 dark:text-white">Enter sentence to predict next word</label>
        <div className='flex flex-row'>
          <input 
          value={sentence} 
          onKeyPress={handleKeyPress}
          onChange={(e) => setSentence(e.target.value)}
          type="text" id="default-input" className="outline-none border-none mr-10 bg-gray-50 border border-gray-300 text-gray-900 text-md rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" />
          <button
          onClick={handlePredict}
          type='submit' className='font-bold bg-[#f9ba18] p-2 text-[#000000] rounded-md w-150 hover:bg-[#be8900] cursor-pointer'>Predict</button>
        </div>
        <div className='flex flex-col justify-center items-center mt-10'>

          <Prediction_card title={"Predicted word"} word={predictions[0]?.word}/>
        </div>
      </div>
    </>
  )
}

export default N_gram_page
