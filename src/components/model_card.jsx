


function Model_card({ model_name , model_description, destination, icon}) {
    return (
        <>
         <a href={destination} class="block max-w-sm px-6 py-0 bg-white border border-gray-200 rounded-lg shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700 py-20">
            <img src={icon} alt="" width={100} height={100} className="pt-0"/>
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{model_name}</h5>
            <p class="font-normal text-gray-700 dark:text-gray-400">{model_description}</p>
         </a>
        </>
    );
}

export default Model_card