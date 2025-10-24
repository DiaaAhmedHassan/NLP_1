import Prediction_card from "../components/prediction_card";
import React , {useState} from "react";

function Log_reg(){

    const [inputText, setInputText] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const API_URL = "http://localhost:8000";

    const handlePredict = async () => {
        if (!inputText.trim()) {
            setError('Please enter some text');
            return;
        }

        setLoading(true);
        setError('');
        setPrediction(null);

        try {
            const response = await fetch(`${API_URL}/predict-next`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    sentence: inputText,
                    model_type: "logistic_regression"  // Specify Logistic Regression model
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `API error: ${response.status}`);
            }

            const data = await response.json();
            setPrediction(data.spam_prediction);
            
        } catch (err) {
            setError('Failed to get prediction: ' + err.message);
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
          
    <div className="text-5xl flex flex-row justify-center mt-10 mb-3">
        Logistic regression
    </div>
    <div className="mb-6 p-20">
    <label htmlFor="large-input" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Enter the sms to detect if it's Spam or Ham</label>
    
    <textarea
    value={inputText}
    onKeyPress={handleKeyPress}
    onChange={(e) => setInputText(e.target.value)}
    type="textarea" id="large-input" className="outline-none border-none mr-6 block w-full p-4 text-gray-900 border border-gray-300 mb-15 rounded-lg bg-gray-50 text-base focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"/>
    <button
    onClick={handlePredict}
    type='submit' className='font-bold bg-[#f9ba18] p-2 text-[#000000] rounded-md w-150 hover:bg-[#be8900] cursor-pointer w-full'>Detect</button>
    </div>
    <div className="flex flex-col justify-center items-center">
    <Prediction_card title={"Detection"} word={prediction?.classification}></Prediction_card>
    </div>
    </>
     
    );
}

export default Log_reg