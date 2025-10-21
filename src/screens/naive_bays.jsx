import Prediction_card from "../components/prediction_card";

function Naive_bays(){
    return (
    <>
    <div className="text-5xl flex flex-row justify-center mt-10 mb-3">
        Naive bays
    </div>
    <div className="mb-6 p-20">
    <label htmlFor="large-input" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Enter the sms to detect if it's Spam or Ham</label>
    
    <textarea type="textarea" id="large-input" className="outline-none border-none mr-6 block w-full p-4 text-gray-900 border border-gray-300 mb-15 rounded-lg bg-gray-50 text-base focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"/>
    
    <button type='submit' className='font-bold bg-[#f9ba18] p-2 text-[#000000] rounded-md w-150 hover:bg-[#be8900] cursor-pointer w-full'>Detect</button>
    </div>
    <div className="flex flex-col justify-center items-center">

    <Prediction_card title={"Detection"}></Prediction_card>
    </div>
    </>
    );
}

export default Naive_bays