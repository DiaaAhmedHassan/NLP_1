import React from 'react'
import Prediction_card from '../components/prediction_card'

function N_gram_page (){
  return (
    <>
    <div className="mb-2 p-20 flex flex-col">
    <h1 className='flex flex-col items-center text-5xl mb-10 font-bold'>
        N-gram Model
    </h1>
    <label htmlFor="default-input" className="block mb-2 mt-15 text-xl outline-amber font-medium text-gray-900 dark:text-white">Enter sentence to predict next word</label>
    <div className='flex flex-row'>
    <input type="text" id="default-input" className="outline-none border-none mr-10 bg-gray-50 border border-gray-300 text-gray-900 text-md rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"/>
    <button type='submit' className='font-bold bg-[#f9ba18] p-2 text-[#000000] rounded-md w-150 hover:bg-[#be8900] cursor-pointer'>Predict</button>
    </div>
    <div className='flex flex-col justify-center items-center mt-10'>
   
    <Prediction_card title={"Predicted word"} />
    </div>
    </div>
    </>
  )
}

export default N_gram_page
