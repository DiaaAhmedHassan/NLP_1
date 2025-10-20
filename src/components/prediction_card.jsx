function Prediction_card({word, title}){
    return (
        <>
         <h2>{title}</h2>
         <div className="flex flex-row justify-center items-center bg-[#364153] w-100 h-50  rounded-xl font-bold text-3xl text-[#f9ba18]">
            {word}
         </div>
        </>
    );
}

export default Prediction_card;
